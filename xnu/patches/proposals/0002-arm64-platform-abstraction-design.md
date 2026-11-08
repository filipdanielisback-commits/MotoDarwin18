# Proposal 0002 — ARM64 Platform Abstraction Boundary

> **Status:** Architecture proposal; no executable kernel patch or platform adapter.
> **Target baseline:** Apple XNU `xnu-11215.1.10`
> **Pinned commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`

## Goal

Describe a reviewable boundary between architecture-generic ARM64 kernel services and board-specific platform facts. The goal is to prevent MotoDarwin18 research from treating SoC-family clues as universal ARM64 behavior or hard-coding unverified XT2135-2 details into generic code.

Apple's XNU source tree describes `pexpert/` as containing platform-specific code, including interrupt handling and atomics. Its source guidance also recommends feature/configuration-based conditionals where appropriate rather than broad platform-name checks. See the [pinned XNU source baseline](../../UPSTREAM.md) and [upstream XNU README](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/README.md).

## Proposed conceptual layers

| Layer | Responsibility | Example information | Evidence needed |
|---|---|---|---|
| ARM64 architecture | CPU execution assumptions and architecture-defined mechanisms | Exception levels, generic architectural features | Architecture specification and CPU evidence |
| XNU platform boundary | Platform Expert-owned service contracts | Machine identity, early console/debug capability, interrupt/time services | Pinned XNU source contract |
| SoC description | SoC-specific controller inventory and integration facts | Candidate GIC/PDC, timer, storage controller | Qualcomm or source-tree evidence |
| Board profile | Exact handset/revision facts | Memory reservations, panel, PMIC, touch controller | Exact XT2135-2 board/revision evidence |
| Capability report | Explicitly state available, unavailable, or unknown | Display service unknown; exact interrupt routing unknown | Direct source or independent validation |

This is a documentation model, not a proposed ABI or an implementation-ready C interface.

## Design rules

1. Generic ARM64 code must not depend on a Moto G60 model string to infer hardware capabilities.
2. Board-specific facts must remain outside generic architecture assumptions.
3. Every capability must carry an evidence scope: generic architecture, SoC family, hanoip family, or exact XT2135-2 revision.
4. Unknown values must remain unknown; no guessed defaults for memory maps, interrupt routing, timers, panel identity, or firmware services.
5. Optional services must be represented as unavailable or unknown rather than silently assumed.
6. Platform-specific source reuse requires file-level provenance and license review.
7. A host-side capability model is not evidence that the physical platform exposes the capability.

## Candidate service categories for research

- Machine/platform identity.
- Physical memory and reserved-region description.
- Interrupt-controller and routing description.
- Clock and timer description.
- Early console/debug availability.
- Display and input service availability.
- Storage and peripheral controller inventory.
- Power and thermal dependencies.

No register map, hardware initialization sequence, firmware call, boot handoff code, or driver implementation is specified.

## Relationship to existing project work

- [Early platform dependencies](../../../docs/XNU_EARLY_PLATFORM_DEPENDENCIES.md)
- [Platform requirements](../../../docs/PLATFORM_REQUIREMENTS.md)
- [SoC platform requirements](../../../docs/SOC_PLATFORM_REQUIREMENTS.md)
- [XNU compatibility matrix](../../COMPATIBILITY_MATRIX.md)
- [Platform services specification](../../../xnuloader/PLATFORM_SERVICES.md)

## Acceptance criteria for a future implementation proposal

A future implementation proposal must first identify the exact service contract in the pinned XNU source, establish which layer owns it, provide authoritative evidence for the target capability, and show how unsupported or unknown services are handled. It must not be described as a driver or port until implementation and validation evidence exist.

## Conclusion

This proposal establishes a separation-of-concerns model for future source review. It does not add an XNU platform abstraction to the kernel and does not establish Moto G60 compatibility.

*Project: MotoDarwin18*
