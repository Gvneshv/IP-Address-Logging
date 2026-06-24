# AuditLogger

AuditLogger is a Windows-focused Python project for collecting network and system audit data, writing tamper-evident JSON logs, and notifying a Telegram channel when the external IP address changes.

## Version plan

### v1

- Run at Windows startup
- Record external IP
- Record local IP
- Record MAC address
- Record hostname
- Record system boot time
- Store events in JSONL
- Calculate SHA256 event hashes
- Send Telegram notification when the external IP changes

### v2

- Hash chain across events
- Daily archive
- Report export
- Log integrity verification
- Backups

### v3

- Digital signatures for logs
- Multiple independent hash storage locations
- Web interface for event browsing

## Project layout

```text
auditlogger/
├── collector/
│   ├── network.py
│   ├── system.py
│   └── timecheck.py
├── storage/
│   ├── json_logger.py
│   ├── hashchain.py
│   └── archive.py
├── notifications/
│   ├── telegram.py
│   └── email.py
├── scheduler/
│   └── tasks.py
├── config/
│   └── config.yaml
└── main.py
```

## Quick start

1. Copy `auditlogger/config/config.example.yaml` to `auditlogger/config/config.yaml`.
2. Fill Telegram settings if notifications are needed.
3. Run:

```powershell
python -m auditlogger.main
```

Logs are written to `logs/audit.jsonl` by default.
