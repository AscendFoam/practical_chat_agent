# migrations

数据库 schema 迁移脚本。按序号递增执行。

## 文件说明

| 文件 | 说明 |
|------|------|
| `001_initial_schema.sql` | 初始 schema，创建 `practical_chat_agent` 数据库及核心表 |

### 初始 Schema 包含的表

| 表名 | 说明 |
|------|------|
| `agents` | Agent 定义（ID、显示名、人格类型、安全模式等） |
| `agent_profiles` | Agent 详细档案（性格特征、说话风格、兴趣、禁止行为，JSON 字段） |
| `events` | 交互事件日志（平台、频道、参与者、内容、时间戳） |
| `memories` | Agent 记忆系统（记忆类型、显著度、置信度、事实、证据引用） |
| `audit_logs` | 系统审计日志（操作、状态、详情） |

## 执行方式

```bash
mysql -u root -p < migrations/001_initial_schema.sql
```

## 约定

- 文件名前缀为三位序号（`001_`, `002_`, ...），确保执行顺序
- 每个迁移文件应幂等或包含 `IF NOT EXISTS` 保护
- 字符集统一使用 `utf8mb4` / `utf8mb4_unicode_ci`
