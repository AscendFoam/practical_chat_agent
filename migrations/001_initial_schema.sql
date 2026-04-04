CREATE DATABASE IF NOT EXISTS `practical_chat_agent`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `practical_chat_agent`;

CREATE TABLE IF NOT EXISTS agents (
  agent_id VARCHAR(64) NOT NULL PRIMARY KEY,
  display_name VARCHAR(255) NOT NULL,
  persona_type VARCHAR(32) NOT NULL,
  system_identity VARCHAR(64) NOT NULL,
  public_disclosure TEXT NULL,
  relationship_mode VARCHAR(64) NOT NULL,
  safety_mode VARCHAR(32) NOT NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS agent_profiles (
  agent_id VARCHAR(64) NOT NULL PRIMARY KEY,
  core_traits JSON NOT NULL,
  speech_style JSON NOT NULL,
  interests JSON NOT NULL,
  do_not_do JSON NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS events (
  event_id VARCHAR(64) NOT NULL PRIMARY KEY,
  tenant_id VARCHAR(64) NOT NULL,
  source_type VARCHAR(32) NOT NULL,
  platform VARCHAR(32) NOT NULL,
  channel_id VARCHAR(128) NOT NULL,
  channel_type VARCHAR(32) NOT NULL,
  account_id VARCHAR(128) NOT NULL,
  actor_id VARCHAR(128) NOT NULL,
  actor_name VARCHAR(255) NULL,
  direction VARCHAR(16) NOT NULL,
  content_type VARCHAR(32) NOT NULL,
  occurred_at DATETIME(6) NOT NULL,
  text_body TEXT NULL,
  attachments JSON NOT NULL,
  raw_payload JSON NOT NULL,
  created_at DATETIME(6) NOT NULL,
  INDEX idx_events_channel_occurred_at (channel_id, occurred_at),
  INDEX idx_events_actor (actor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS memories (
  memory_id VARCHAR(64) NOT NULL PRIMARY KEY,
  agent_id VARCHAR(64) NOT NULL,
  user_id VARCHAR(128) NOT NULL,
  memory_type VARCHAR(32) NOT NULL,
  scope VARCHAR(32) NOT NULL,
  salience DOUBLE NOT NULL,
  confidence DOUBLE NOT NULL,
  fact TEXT NOT NULL,
  evidence_refs JSON NOT NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  INDEX idx_memories_agent_user (agent_id, user_id),
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_logs (
  audit_id VARCHAR(64) NOT NULL PRIMARY KEY,
  agent_id VARCHAR(64) NULL,
  action VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  details JSON NOT NULL,
  created_at DATETIME(6) NOT NULL,
  INDEX idx_audit_agent_created_at (agent_id, created_at),
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
