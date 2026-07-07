# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `auditlogger/collector/router/` provider package: `RouterProvider` abstract interface, `RouterConnection` connection parameters, `RouterClient` shared HTTP session handling, and `AutoDetectionProvider` (current default, not yet implemented).
- Added a router orchestrator (`collect_router_info`) that selects a provider from `config["router"]["detection"]["type"]` and delegates collection to it.
- Added an optional `network.router` field to audit events, populated only when the router collector returns data.
- Added regression tests for the router orchestrator and for the config loader's nested-section parsing.

### Changed

- Changed the fallback YAML parser in `config/loader.py` to support arbitrary nesting depth, required by the new `router.connection.*` config fields.
- Renamed `collect_network_info`'s parameter from `config` to `router_config` for clarity (it only ever received the router section).

### Security

- No change - router credentials remain part of the gitignored local config, same as the Telegram token.

### Known Limitations

- `AutoDetectionProvider` is a stub and returns no data yet; WAN/DNS/gateway collection is still pending (Phase 2 of `docs/refactoring-roadmap.md`).

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
