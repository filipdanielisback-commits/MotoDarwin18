# Architecture Research Notes

**Status:** introductory model; not a device implementation.

This document provides a vocabulary for discussing a possible Darwin/XNU compatibility effort. It does not describe a working Moto G60 port.

## Conceptual layers

| Layer | Research question | Current status |
|---|---|---|
| Hardware platform | What CPU, memory, and peripheral blocks are present in XT2135-2? | To verify |
| Firmware and boot environment | What platform interfaces are available and documented? | Not investigated |
| Kernel | Which kernel interfaces and platform assumptions would need to be understood? | Research only |
| Drivers | What hardware-specific support would be required? | Unknown |
| User space | Which user-space components are open source, proprietary, or third-party? | Must be assessed per component |
| Applications and services | Which features depend on proprietary services or unsupported interfaces? | Unknown |

## Important distinctions

- **XNU** is the kernel; it is not the entirety of iOS.
- **Darwin** includes more than the kernel.
- **iOS** includes proprietary components and services that are not made open source merely because XNU has published source.
- A kernel starting successfully would not prove that the full operating system, hardware features, or applications work.

## Evidence labels

Use these labels in notes and issue reports:

- **Verified:** supported by a primary source or a repeatable test.
- **Observed:** directly observed, but not independently reproduced.
- **Inferred:** a reasoned conclusion based on cited evidence.
- **Unknown:** insufficient evidence.
- **Blocked:** investigation cannot proceed without additional information or permissions.

## Compatibility matrix template

| Subsystem | Evidence / source | Status | Notes |
|---|---|---|---|
| CPU and ARM64 | TBD | Unknown | Confirm exact SoC and CPU configuration |
| Memory | TBD | Unknown | Record only documented facts |
| Display / graphics | TBD | Unknown | Separate display output from GPU acceleration |
| Storage | TBD | Unknown | No assumptions about controller support |
| Touch / input | TBD | Unknown | |
| Audio | TBD | Unknown | |
| Wi-Fi / Bluetooth | TBD | Unknown | |
| Power / battery | TBD | Unknown | |
| Sensors / cameras | TBD | Unknown | |

## Research principles

1. Prefer primary documentation and upstream source code.
2. Cite every non-obvious technical claim.
3. Do not copy proprietary binaries, firmware, keys, or restore images into this repository.
4. Preserve upstream license notices and provenance.
5. Do not label a subsystem as supported until there is evidence.
