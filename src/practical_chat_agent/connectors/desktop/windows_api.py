from __future__ import annotations

import ctypes
from ctypes import wintypes
from pathlib import Path

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
MAX_CLASS_NAME = 256
MAX_PATH = 32768

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def list_visible_windows() -> list[dict[str, object]]:
    """Return metadata for visible top-level windows on Windows."""

    results: list[dict[str, object]] = []

    @WNDENUMPROC
    def _enum_proc(hwnd: int, _lparam: int) -> bool:
        if not user32.IsWindowVisible(hwnd):
            return True

        window = get_window_metadata(hwnd)
        if not window["title"] and not window["process_name"]:
            return True

        results.append(window)
        return True

    user32.EnumWindows(_enum_proc, 0)
    return results


def get_window_metadata(hwnd: int) -> dict[str, object]:
    process_id = _get_window_process_id(hwnd)
    return {
        "hwnd": int(hwnd),
        "parent_hwnd": _get_parent_handle(hwnd),
        "title": _get_window_text(hwnd),
        "class_name": _get_class_name(hwnd),
        "process_id": process_id,
        "process_name": _get_process_name(process_id),
        "visible": bool(user32.IsWindowVisible(hwnd)),
        "enabled": bool(user32.IsWindowEnabled(hwnd)),
        "rect": _get_window_rect(hwnd),
    }


def list_child_windows(hwnd: int, *, max_depth: int = 3) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    def _walk(parent_hwnd: int, depth: int) -> None:
        if depth > max_depth:
            return

        for child_hwnd in _list_direct_child_handles(parent_hwnd):
            metadata = get_window_metadata(child_hwnd)
            metadata["depth"] = depth
            results.append(metadata)
            _walk(child_hwnd, depth + 1)

    _walk(int(hwnd), 1)
    return results


def get_foreground_window_handle() -> int | None:
    foreground = int(user32.GetForegroundWindow())
    return foreground or None


def _get_window_text(hwnd: int) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value.strip()


def _get_class_name(hwnd: int) -> str:
    buffer = ctypes.create_unicode_buffer(MAX_CLASS_NAME)
    user32.GetClassNameW(hwnd, buffer, MAX_CLASS_NAME)
    return buffer.value.strip()


def _get_window_process_id(hwnd: int) -> int:
    process_id = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
    return int(process_id.value)


def _get_parent_handle(hwnd: int) -> int | None:
    parent = int(user32.GetParent(hwnd))
    return parent or None


def _get_window_rect(hwnd: int) -> dict[str, int]:
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return {
        "left": int(rect.left),
        "top": int(rect.top),
        "right": int(rect.right),
        "bottom": int(rect.bottom),
    }


def _list_direct_child_handles(parent_hwnd: int) -> list[int]:
    descendants: list[int] = []

    @WNDENUMPROC
    def _enum_proc(hwnd: int, _lparam: int) -> bool:
        descendants.append(int(hwnd))
        return True

    user32.EnumChildWindows(parent_hwnd, _enum_proc, 0)
    return [hwnd for hwnd in descendants if int(user32.GetParent(hwnd)) == int(parent_hwnd)]


def _get_process_name(process_id: int) -> str:
    if process_id <= 0:
        return ""

    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, process_id)
    if not handle:
        return ""

    try:
        size = wintypes.DWORD(MAX_PATH)
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        ok = kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size))
        if not ok:
            return ""
        return Path(buffer.value).name
    finally:
        kernel32.CloseHandle(handle)
