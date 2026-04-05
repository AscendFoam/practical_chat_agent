from __future__ import annotations

import ctypes
import struct
import zlib
from ctypes import wintypes
from pathlib import Path

gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)

BI_RGB = 0
DIB_RGB_COLORS = 0
HGDI_ERROR = ctypes.c_void_p(-1).value
SRCCOPY = 0x00CC0020


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ("rgbBlue", ctypes.c_ubyte),
        ("rgbGreen", ctypes.c_ubyte),
        ("rgbRed", ctypes.c_ubyte),
        ("rgbReserved", ctypes.c_ubyte),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 1),
    ]


def capture_screen_region_png(region: dict[str, int]) -> bytes:
    """Capture a visible on-screen region and return PNG bytes."""

    left = int(region["left"])
    top = int(region["top"])
    width = max(int(region["right"]) - left, 1)
    height = max(int(region["bottom"]) - top, 1)

    screen_dc = user32.GetDC(0)
    if not screen_dc:
        raise OSError("GetDC failed while capturing the screen region")

    memory_dc = gdi32.CreateCompatibleDC(screen_dc)
    if not memory_dc:
        user32.ReleaseDC(0, screen_dc)
        raise OSError("CreateCompatibleDC failed while capturing the screen region")

    bitmap = gdi32.CreateCompatibleBitmap(screen_dc, width, height)
    if not bitmap:
        gdi32.DeleteDC(memory_dc)
        user32.ReleaseDC(0, screen_dc)
        raise OSError("CreateCompatibleBitmap failed while capturing the screen region")

    old_object = gdi32.SelectObject(memory_dc, bitmap)
    if old_object in (None, HGDI_ERROR):
        gdi32.DeleteObject(bitmap)
        gdi32.DeleteDC(memory_dc)
        user32.ReleaseDC(0, screen_dc)
        raise OSError("SelectObject failed while capturing the screen region")

    try:
        if not gdi32.BitBlt(memory_dc, 0, 0, width, height, screen_dc, left, top, SRCCOPY):
            raise OSError("BitBlt failed while capturing the screen region")

        bitmap_info = BITMAPINFO()
        bitmap_info.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bitmap_info.bmiHeader.biWidth = width
        bitmap_info.bmiHeader.biHeight = -height
        bitmap_info.bmiHeader.biPlanes = 1
        bitmap_info.bmiHeader.biBitCount = 32
        bitmap_info.bmiHeader.biCompression = BI_RGB

        raw_buffer = ctypes.create_string_buffer(width * height * 4)
        lines = gdi32.GetDIBits(
            memory_dc,
            bitmap,
            0,
            height,
            raw_buffer,
            ctypes.byref(bitmap_info),
            DIB_RGB_COLORS,
        )
        if lines != height:
            raise OSError("GetDIBits failed while reading the screen region")

        rgba_bytes = _bgra_to_rgba(raw_buffer.raw)
        return _encode_png_rgba(width=width, height=height, rgba_bytes=rgba_bytes)
    finally:
        gdi32.SelectObject(memory_dc, old_object)
        gdi32.DeleteObject(bitmap)
        gdi32.DeleteDC(memory_dc)
        user32.ReleaseDC(0, screen_dc)


def save_png_bytes(*, png_bytes: bytes, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(png_bytes)
    return output_path


def _bgra_to_rgba(raw_bytes: bytes) -> bytes:
    converted = bytearray(len(raw_bytes))
    for index in range(0, len(raw_bytes), 4):
        blue = raw_bytes[index]
        green = raw_bytes[index + 1]
        red = raw_bytes[index + 2]
        alpha = raw_bytes[index + 3]
        converted[index:index + 4] = bytes((red, green, blue, alpha))
    return bytes(converted)


def _encode_png_rgba(*, width: int, height: int, rgba_bytes: bytes) -> bytes:
    stride = width * 4
    raw_rows = bytearray()
    for row_index in range(height):
        start = row_index * stride
        raw_rows.append(0)
        raw_rows.extend(rgba_bytes[start:start + stride])

    ihdr = struct.pack("!IIBBBBB", width, height, 8, 6, 0, 0, 0)
    idat = zlib.compress(bytes(raw_rows), level=9)
    return b"".join(
        (
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(b"IHDR", ihdr),
            _png_chunk(b"IDAT", idat),
            _png_chunk(b"IEND", b""),
        ),
    )


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    return b"".join(
        (
            struct.pack("!I", len(payload)),
            chunk_type,
            payload,
            struct.pack("!I", zlib.crc32(chunk_type + payload) & 0xFFFFFFFF),
        ),
    )
