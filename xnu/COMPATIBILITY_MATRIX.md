# XNU Subsystem Compatibility Matrix

**Target:** Motorola Moto G60 XT2135-2  
**Platform:** Qualcomm Snapdragon 732G  
**Status:** Initial research register; all target-specific support remains unverified.

This matrix separates general XNU source areas from evidence about the target handset. A subsystem appearing in upstream XNU does not mean that it supports this phone.

## Status definitions

- **Unknown:** no adequate target-specific evidence.
- **Researching:** sources are being collected; no implementation claim.
- **Documented:** a requirement or interface is supported by reliable documentation.
- **Implemented:** project-authored code exists and has been reviewed.
- **Validated:** a defined test passed; the test scope must be stated.
- **Not supported:** evidence shows the required capability is absent or unavailable.

## Initial matrix

| Area | Relevant XNU area | Evidence required for XT2135-2 | Status |
|---|---|---|---|
| ARM64 execution | `osfmk/`, architecture support | CPU features and execution assumptions | Unknown |
| Early platform setup | `libsa/`, `pexpert/` | Documented firmware handoff and platform description | Unknown |
| Memory management | `osfmk/`, `pexpert/` | Physical memory map and reserved regions | Unknown |
| Interrupt handling | `pexpert/`, `osfmk/` | Interrupt-controller model and routing | Unknown |
| Timers and clocks | `osfmk/`, `pexpert/` | Timer interfaces, frequencies, and clock dependencies | Unknown |
| Storage | `bsd/`, `iokit/` | Exact controller, bus, and required dependencies | Unknown |
| Display | `iokit/`, `pexpert/` | Panel, display controller, and documented initialization interfaces | Unknown |
| Graphics | `iokit/` and related components | GPU support and permitted software/firmware dependencies | Unknown |
| USB | `iokit/`, `pexpert/` | Controller identity and supported interfaces | Unknown |
| Audio | `iokit/` | Codec, amplifier, routing, and dependencies | Unknown |
| Wireless | `iokit/` and related components | Wi-Fi/Bluetooth components and firmware requirements | Unknown |
| Power and thermal | `pexpert/`, `iokit/` | PMIC, clocks, regulators, thermal interfaces | Unknown |
| Sensors and cameras | `iokit/` | Exact components, buses, and interfaces | Unknown |
| User space | Outside XNU kernel scope | Separate assessment of open-source and proprietary components | Unknown |

## Evidence record

For every status change, add a dated entry containing:

- **Subsystem:**
- **Claim:**
- **Target scope:** exact XT2135-2, Snapdragon 732G family, or generic architecture.
- **Source:** title, publisher, URL, version/date.
- **Evidence summary:**
- **Confidence:** confirmed, probable, or unverified.
- **Implementation:** none, proposed, or linked project file.
- **Validation:** test name, environment, result, and limitations.
- **Reviewer / date:**

## Rules

1. Never promote a generic SoC capability into a handset-specific fact without evidence.
2. Do not mark a subsystem implemented merely because a file or placeholder exists.
3. Do not equate a successful source build with a successful device boot.
4. Do not equate kernel startup with complete Darwin or iOS compatibility.
5. Keep proprietary firmware and restricted artifacts out of the repository unless redistribution rights are clear and reviewed.

## Related project records

- [Device inventory](../docs/DEVICE_INVENTORY.md)
- [Device unknowns](../docs/DEVICE_UNKNOWNS.md)
- [Snapdragon 732G platform requirements](../docs/SOC_PLATFORM_REQUIREMENTS.md)
- [General platform integration requirements](../docs/PLATFORM_REQUIREMENTS.md)
- [Upstream source record](UPSTREAM.md)
