# Project Architecture

## Purpose

This document describes the high-level architecture of the project, the responsibility of each module, and the design principles that should guide future development.

It is intentionally focused on architecture rather than implementation details.

---

# Design Goals

The project should remain:

- Simple
- Predictable
- Easy to extend
- Easy to test
- Platform-focused (Windows-first)
- Safe for forensic and audit scenarios

New functionality should be added with minimal impact on existing components.

---

# Core Principles

## Single Responsibility

Each module should have one clear responsibility.

Examples:

- collecting information
- writing logs
- sending notifications
- loading configuration

Modules should not perform unrelated tasks.

---

## Separation of Concerns

Collecting data, storing data, and reacting to changes are separate responsibilities.

Example:

A network collector should never send Telegram notifications.

A notification provider should never collect network information.

---

## Extensibility

The project should support adding new data sources and notification backends without modifying existing components whenever possible.

Future additions should primarily consist of new modules rather than changes to existing ones.

---

## Predictable Behaviour

One execution of the application should produce one consistent audit snapshot.

Providers should avoid repeated collection of the same information unless explicitly required.

Collectors should fail independently. A failure in one collector must not prevent the application from producing a valid snapshot using the remaining collectors.

---

# High-Level Architecture

    Application

    ├── Configuration
    ├── Data Sources
    ├── Storage
    ├── Notifications
    └── Scheduler

---

# Components

## Configuration

Responsibilities:

- load configuration
- validate configuration
- expose configuration to the application

Configuration should not contain business logic.

---

## Data Sources

Responsible for collecting information from the operating system, network, or external systems.

Examples:

- Public IPv4
- Public IPv6
- Router WAN
- Local interfaces
- System information

Every data source should expose a consistent interface.

Example:

collect()

returns

- collected value(s)
- metadata
- collection timestamp

Data sources should never:

- write logs
- send notifications
- modify configuration

---

## Storage

Responsible for persistent storage.

Examples:

- JSONL logs
- archive creation
- hash chain
- integrity verification

Storage modules should never collect information directly.

---

## Notifications

Responsible for informing the user about important events.

Examples:

- Telegram
- Email
- Future providers

Notification modules receive events.

They never decide whether an event occurred.

---

## Scheduler

Responsible only for deciding when the application executes.

Scheduling logic should remain independent from business logic.

---

# Future Provider Architecture

The project should evolve toward a provider-based architecture.

Example:

    Data Source

    ├── Public IP
    ├── Router WAN
    ├── IPv6
    └── Future Sources

Each provider should be self-contained.

Adding a new provider should require creating a new module instead of modifying unrelated code.

---

# Router Integrations

Router-specific implementations should remain isolated.

Example:

auditlogger/collector/router/

base.py       # RouterProvider - abstract interface every provider implements

connection.py # RouterConnection - connection/credential parameters

client.py     # RouterClient - shared HTTP session handling (requests-based)

detection.py  # AutoDetectionProvider - current default, returns {} (not yet implemented)

__init__.py   # collect_router_info() - orchestrator; selects a provider from config["router"]["detection"]["type"] and delegates to it

tplink.py     # future vendor providers follow the same RouterProvider interface
mikrotik.py
asus.py
keenetic.py

The application should communicate only with the common interface.

It should not contain vendor-specific logic.

---

# Configuration Philosophy

The application should automatically discover as much information as reasonably possible.

Users should only provide information that cannot be discovered automatically.

Examples:

✓ Telegram token

✓ Router credentials

✓ Optional router address

Examples of information that should preferably be discovered automatically:

- local interfaces
- gateway
- router address
- public IP
- available capabilities

---

# Capability Detection

Whenever practical, the application should detect supported features automatically.

Example:

Detected capabilities:

✓ Public IP lookup

✓ Router detected

✓ Router vendor identified

✓ WAN IP supported

Capability detection should improve usability while remaining optional.

---

# Testing Philosophy

Every new feature should be testable independently.

Data sources should be testable without notification modules.

Notification modules should be testable without storage.

---

# Documentation

Code should explain how.

Comments should explain why.

Architecture documents should explain responsibilities.

---

# Long-Term Vision

The project should grow by adding new providers instead of increasing complexity inside existing modules.

The preferred direction is:

small independent modules

over

large centralized logic.