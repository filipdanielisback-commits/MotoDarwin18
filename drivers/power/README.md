# Power

**Status: research only — no Moto G60 power-driver implementation.**

Scope: battery-state reporting, charging and power-source abstractions, thermal monitoring, and the boundary to platform power management.

The exact XT2135-2 PMIC configuration, battery-management path, thermal sensors, charging controller and board revision are not yet established. Hanoip-family source references are leads, not confirmation of the target's component population.

No power-control sequence, register map, voltage/current setting, charging override or thermal-limit modification is specified here. Any future work must begin with authoritative exact-model evidence and a safety review.

See [driver research rules](../README.md).
