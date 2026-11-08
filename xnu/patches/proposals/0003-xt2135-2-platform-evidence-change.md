# Proposal 0003 — XT2135-2 Platform Evidence Record

> **Status:** Documentation-only target change; no executable kernel patch.
> **Exact target:** Motorola XT2135-2 / MC38C / moto g60 vision
> **Related source family:** `hanoip` / SDMMAGPIE
> **Board revision mapping:** Unresolved

## Purpose

Record which Moto G60-family platform clues may guide XNU research while preventing those clues from being promoted into exact-device implementation assumptions.

## Exact-model identity

Motorola's declaration of conformity identifies XT2135-2 as MC38C / moto g60 vision and distinguishes it from XT2135-1 / MC38B. See [XT2135-2 identity evidence](../../../research/soc/XT2135_2_IDENTITY.md).

This confirms the regulatory model identity. It does not identify the exact board revision or DVT overlay.

## Family-level platform evidence

The shared hanoip / SDMMAGPIE Android/Linux source tree provides research clues, including:

| Area | Family-level clue | Exact XT2135-2 status |
|---|---|---|
| Interrupts | GICv3 and Qualcomm PDC nodes in shared SoC description | Exact routing unverified |
| Timers | Arm generic timer description with 19.2 MHz frequency | Exact enabled source/configuration unverified |
| Memory | Reserved-memory carveouts in shared device tree | Complete exact memory map unknown |
| Storage | UFS host and SD-card controller descriptions | Exact component and target configuration unknown |
| Display | Tianma ILI7807S 678-class 1080×2460 MIPI-DSI panel include | Candidate family evidence; exact panel unconfirmed |
| Touch | Ilitek SPI touchscreen node in family source | Exact controller/revision and pre-OS service unknown |
| Power | PM6150/PM6150L descriptions and MC50 battery profiles | Exact populated components unknown |

Source detail and caveats are recorded in [Hanoip platform evidence](../../../research/soc/HANOIP_PLATFORM_EVIDENCE.md). That source tree covers a device family and multiple board overlays; it is not an official XT2135-2 schematic or a verified per-unit bill of materials.

## Proposed target-specific change

For now, the only justified target-specific change is a documentation and evidence-register update:

- retain XT2135-2 / MC38C as the exact project target;
- retain hanoip / SDMMAGPIE as a family-level research lead;
- keep DVT1/DVT2 mapping unresolved;
- keep exact memory map, interrupt routing, timer enablement, display panel, touch controller, PMIC population, and storage component unresolved;
- do not add a board-specific XNU source implementation based only on shared-family Linux descriptions.

## Why no kernel source diff is proposed

A Moto-specific kernel change requires evidence that a concrete hardware fact or service contract applies to the exact target revision. The current family-level sources do not establish that. Hard-coding candidate values into XNU would convert uncertainty into an unsupported compatibility claim.

## Evidence needed to reconsider

1. Authoritative mapping from XT2135-2 / MC38C to a board identifier and hardware revision.
2. Source-backed DVT overlay selection for that exact revision.
3. Exact-model evidence for the relevant controller or service.
4. A pinned XNU consumer contract for the proposed subsystem.
5. File-level provenance and license review for any source considered for reuse.

## Conclusion

This is a Moto G60-specific evidence change, not a hardware driver. It deliberately leaves unresolved fields unresolved and prevents family clues from becoming unsupported XNU assumptions.

*Project: MotoDarwin18*
