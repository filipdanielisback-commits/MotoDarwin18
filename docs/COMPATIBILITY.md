# Compatibility assessment

This matrix tracks the questions that must be answered before any claim of Darwin/XNU compatibility can be made for Moto G60 XT2135-2.

**Current overall status: Research only. No working Darwin/XNU port is claimed.**

## Status definitions

- **Unknown** — not investigated or no reliable evidence.
- **Researching** — sources are being collected.
- **Partially understood** — architecture or interfaces are documented, but device support is not demonstrated.
- **Demonstrated** — evidence exists for a narrowly defined, repeatable result.
- **Blocked** — a known missing prerequisite prevents progress.

## Compatibility matrix

| Area | What must be established | Status |
|---|---|---|
| CPU architecture | Exact execution environment and required ARM64 platform features | Researching |
| Exception levels | Required privilege-level and exception handling model | Unknown |
| Boot chain | A documented, legitimate route to load a research kernel in a controlled environment | Unknown |
| Memory map | RAM layout, reserved regions, and memory attributes | Unknown |
| Interrupt controller | Controller model, topology, and interrupt routing | Unknown |
| Timers and clocks | Architectural and platform timer support | Unknown |
| Device description | Reliable hardware description for the target board | Unknown |
| Storage | Controller support and a safe, documented storage path | Unknown |
| Console / display | A minimal observable output path | Unknown |
| Input | Touchscreen and button interfaces | Unknown |
| Power management | Safe clock, reset, thermal and power-control model | Unknown |
| Wi-Fi / Bluetooth | Required firmware and driver interfaces | Unknown |
| Audio | Codec and audio subsystem integration | Unknown |
| Cellular | Modem control and vendor interface requirements | Unknown |
| Userland | Compatibility between the chosen Darwin userland and kernel/platform services | Unknown |
| Licensing / provenance | Rights and provenance for every source, binary, firmware and image used | Researching |

## Key distinction

A CPU that supports ARM64 instructions is not automatically a supported Darwin platform. XNU needs platform-specific integration for boot, memory, interrupts, timers, drivers, and system services. Likewise, successfully building a kernel does not prove that it can boot on the target hardware or run a useful userland.

## Evidence required for status changes

A status should change only when a note or report records:
- the exact claim being tested;
- the target hardware and software versions;
- the source or reproducible evidence;
- limitations and unresolved dependencies;
- whether the result is device-specific or merely inferred from the SoC family.

## Scope and safety

This project is documentation-first. Do not treat this matrix as a guide to changing boot settings, flashing partitions, bypassing device protections, or modifying a daily-use phone. Any future experiments should be separately reviewed for safety, legality, recoverability, and device-owner authorization.
