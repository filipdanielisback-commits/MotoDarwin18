# XNU Loader Research Area

This directory tracks the design questions for a possible independently developed XNU loader component within MotoDarwin18.

**Documentation and research only**

**Current status:** no loader implementation, firmware integration, boot protocol implementation, or Moto G60 boot support exists here.

## Directory map

| Path | Purpose | Current status |
|---|---|---|
| [src/](src/README.md) | Original implementation, if a safe and validated design is ever approved | No implementation |
| [include/](include/README.md) | Project-owned interface declarations | No interfaces |
| [scripts/](scripts/README.md) | Source-only validation helpers | No scripts |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Conceptual component responsibilities and boundaries | Initial research |
| [HANDOFF_REQUIREMENTS.md](HANDOFF_REQUIREMENTS.md) | High-level information categories a kernel handoff must describe | Research checklist |
| [HAKIOS_ARCHITECTURE_COMPARISON.md](HAKIOS_ARCHITECTURE_COMPARISON.md) | Comparison of HakiOS's public loader architecture with MotoDarwin18 research | Source analysis |
| [INTERFACE_DESIGN.md](INTERFACE_DESIGN.md) | On-device interface, touchscreen, display, fallback input, and evidence gates | Design specification only |
| [Pre-Android display and touch research](../research/display-touch/MOTO_G60_PREANDROID_DISPLAY_TOUCH.md) | Moto G60 family evidence and UEFI display/touch service requirements | Research only |
| [PLATFORM_SERVICES.md](PLATFORM_SERVICES.md) | Pre-OS display and pointer service contracts, lifecycle, and capability evidence | Specification only |
| [platform-services.example.json](platform-services.example.json) | Unknown-by-default descriptive service capability manifest | Host-test fixture |
| [UI_CORE_DESIGN.md](UI_CORE_DESIGN.md) | Platform-neutral menu layout, input contract, and UI state requirements | Design specification only |
| [DISPLAY_RENDERING_DESIGN.md](DISPLAY_RENDERING_DESIGN.md) | Display mode metadata, pixel-format boundaries, responsive layout, and render-backend requirements | Design specification and host model only |
| [COMPATIBILITY.md](COMPATIBILITY.md) | Platform and loader assumptions that remain unverified | Initial unknowns |

## What a loader is responsible for, conceptually

A loader is a component in a larger operating-system startup architecture. At a high level, loader research concerns:

- identifying the execution environment and documented firmware contract;
- understanding how a kernel image is represented and described;
- understanding what platform information the kernel expects to receive;
- documenting memory ownership and the boundary between firmware, loader, and kernel;
- reporting errors clearly and preserving the integrity of source artifacts.

These are topics for architecture study only. This repository does not provide a device boot procedure, executable handoff implementation, or instructions for changing device boot configuration.

## Relationship to XNU

Apple's XNU source tree identifies `libsa` as kernel bootstrap code and `pexpert` as platform-specific code. Those source areas are not interchangeable with an external loader, and their presence does not define a complete third-party boot contract.

See [Apple's XNU README](https://github.com/apple-oss-distributions/xnu/blob/main/README.md).

## Project boundaries

- Keep generic loader concepts separate from Moto G60-specific assumptions.
- Do not infer the phone's firmware interface from a different Snapdragon device.
- Do not claim that a loader can compensate for missing kernel platform support or drivers.
- Do not include proprietary firmware, operating-system images, keys, credentials, or personal data.
- Review provenance and licensing for every external source or dependency.
- Limit future automated checks to source files and test artifacts; do not interact with a connected phone.

## Research sequence

1. Document loader terminology and component boundaries.
2. Identify the kernel-side information requirements from public source documentation.
3. Record the target device's unknown firmware and platform details.
4. Review licensing and feasibility before considering any implementation.
5. Keep any later validation isolated from a personal or essential device.

## Current assessment

MotoDarwin18 remains a documentation and feasibility project. No working loader or Moto G60 boot support is claimed.
