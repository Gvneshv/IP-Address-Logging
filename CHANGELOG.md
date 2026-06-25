# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-25

### Added

- Added the initial Windows-focused AuditLogger application.
- Added manual execution through `python -m auditlogger.main`.
- Added Windows Task Scheduler helper for running AuditLogger at user logon.
- Added external IP collection with fallback endpoints.
- Added local IP detection based on the outbound route selected by Windows.
- Added adapter-specific MAC address collection using the adapter section associated with the selected local IP.
- Added adapter name collection.
- Added hostname, platform, and boot time collection.
- Added UTC timestamps and local timestamps with timezone offsets.
- Added JSONL audit log storage.
- Added SHA256 event hashing and previous-hash linking.
- Added Telegram notification support for external IP changes.
- Added local configuration loading from `auditlogger/config/config.yaml`.
- Added a small fallback YAML parser for the bundled config shape.
- Added unit tests for event shape, local timestamp offset, and adapter parsing.
- Added maintenance-oriented module, class, and function docstrings.

### Security

- Ignored local logs, local config, Python caches, and local agent metadata.
- Kept Telegram tokens and chat IDs out of version control by ignoring `auditlogger/config/config.yaml`.

### Known Limitations

- AuditLogger currently runs once per manual execution or user logon.
- It is not a continuous background service.
- Full chain-wide integrity verification is planned for a later version.
- Email notifications and daily archives are placeholders for future work.
