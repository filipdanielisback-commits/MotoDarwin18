# Wi-Fi

**Status: research only — no Moto G60 driver implementation.**

This subsystem is reserved for the wireless LAN controller and the boundary to the operating-system networking stack.

Research questions:
- What exact WLAN controller and board-level variant are present in XT2135-2 / MC38C?
- Which facts are confirmed by exact-model sources versus shared Hanoip-family sources?
- What firmware, regulatory, calibration and licensing constraints apply?
- Which upstream XNU networking interfaces are relevant?

Do not infer the controller from a family-level module name or copy another device's firmware assumptions. No radio initialization, firmware-loading procedure, register map or device modification is specified here.

Evidence must identify the exact target or be labelled family-level. See [driver research rules](../README.md).
