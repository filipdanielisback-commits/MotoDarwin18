# Network

**Status: research only — no Moto G60 network-driver implementation.**

Scope: the generic network-interface boundary used by operating-system networking, independent of the specific Wi-Fi or cellular hardware drivers.

Keep link-specific hardware work in [wifi](../wifi/README.md) or [modem](../modem/README.md). This directory is for shared networking abstractions and evidence that is not tied to one radio.

No packet-path implementation or device configuration is included. See [driver research rules](../README.md).
