# Core Platform Support

**Status: research only — no Moto G60 core-driver implementation.**

Scope: shared abstractions used by multiple driver subsystems, platform capability reporting, common diagnostics, and boundaries to generic XNU services.

Keep device-specific facts out of generic interfaces. Exact board identity, memory ownership, interrupt topology, timer contract, and firmware-provided services must be supported by exact-target evidence before being represented as available capabilities.

The existing platform inventory and host-side validators are not hardware drivers. This directory does not implement firmware handoff, boot services, register access, or device initialization.

See [driver research rules](../README.md).
