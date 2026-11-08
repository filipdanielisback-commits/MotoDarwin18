# Device Unknowns — Moto G60 XT2135-2

**Status:** Open research register with provisional source-tree findings  
**Scope:** Hardware and platform facts not yet established for the exact target model.  
**Last reviewed:** 2026-11-08

## Purpose

Track unknowns that affect a future Darwin/XNU compatibility assessment. An unknown must remain unknown until supported by reliable evidence. Do not infer handset implementation from a SoC feature list or from a shared device-tree family without checking its board revision.

## Evidence update

A public LineageOS kernel device tree and Android device configuration exist for the shared Motorola Moto G40 Fusion / Moto G60 family, codename `hanoip`. They provide useful platform clues, but they are not an official board schematic and do not identify which board-revision overlay matches every XT2135-2 unit.

See [HANOIP_PLATFORM_EVIDENCE.md](../research/soc/HANOIP_PLATFORM_EVIDENCE.md) for source links, confidence levels, and detailed limitations.

## Open questions and provisional findings

| Area | Current finding | Evidence needed / remaining unknown | Status |
|---|---|---|---|
| Board | Shared `hanoip` device tree has DVT1 and DVT2 overlays | Map exact XT2135-2 hardware revision to the correct overlay | Open |
| Boot | Motorola kernel-source publication trail exists for named XT2135-2 Android builds; this is Android/Linux kernel source, not boot-firmware or handoff documentation | Exact firmware-to-OS ABI, boot firmware interface, entry state, memory ownership and exact board revision remain undocumented | Open |
| CPU | Shared SDMMAGPIE tree describes eight CPU nodes | Confirm exact target topology and exposed firmware description | Probable platform-family evidence |
| Memory | Kernel tree defines several reserved-memory carveouts | Complete physical RAM map, banks, and exact revision reservations | Open |
| Interrupts | Shared SoC tree describes GICv3 and Qualcomm PDC | Exact XT2135-2 routing and firmware ownership | Probable platform-family evidence |
| Timers | Armv8 generic timer listed at 19.2 MHz; memory-mapped timer block described | Exact enabled timer sources and target behavior | Probable platform-family evidence |
| Storage | UFS host path and SD-card controller appear in source tree | Exact flash component; confirm final active controller configuration | Probable platform-family evidence |
| Display | Tianma ILI7807S 678-class MIPI-DSI panel included in Hanoi panel file | Confirm exact panel in XT2135-2 and physical display pipeline | Probable platform-family evidence |
| Touch | Ilitek touchscreen node appears on SPI in Hanoi touchscreen file | Confirm exact controller on target board revision | Probable platform-family evidence |
| Wireless | WCN3990 Bluetooth node; CLD3 WLAN module listed | Exact combo-chip, firmware, calibration, and variant mapping | Open |
| Audio | WCD937x and AW882xx components appear in shared audio overlay | Confirm exact codec/amplifier population on target unit | Probable platform-family evidence |
| Power | PM6150/PM6150L nodes and MC50 battery profiles appear in Hanoi overlays | Exact PMIC population and battery supplier for target unit | Probable platform-family evidence |
| Sensors | Shared sensor overlays exist | Confirm exact sensor models and bus connections | Open |
| USB | Qualcomm USB/PHY nodes exist in shared SoC tree | Exact enabled role/configuration for target board | Open |
| Thermal | PMIC ADC and thermal-zone configuration exists | Exact sensor population and final board policy | Probable platform-family evidence |

## Evidence record template

For every resolved item, record:

- **Claim:**
- **Exact model/revision scope:**
- **Source title and URL:**
- **Source date or access date:**
- **Evidence excerpt or summary:**
- **Confidence:** Confirmed / Probable / Unverified
- **Limitations:**

## Evidence rules

1. Prefer Motorola, Qualcomm, Arm, Android Open Source Project, and component-vendor documentation.
2. Treat community kernel/device trees as valuable secondary engineering evidence, not as official schematics.
3. Distinguish SoC capability from what Motorola implemented in this handset.
4. Do not copy specifications from XT2135-1 or Moto G40 Fusion to XT2135-2 without evidence that they match.
5. Check board-ID and revision overlays before attributing a component to a particular unit.
6. Do not treat forum posts or device-tree guesses as confirmed hardware facts.
7. Keep proprietary firmware and undocumented interfaces clearly marked.
8. Do not claim that resolving a hardware unknown establishes XNU compatibility.

## Current conclusion

The shared hanoip / SDMMAGPIE source tree narrows several research questions, but does not establish a complete exact-model hardware inventory. The full XT2135-2 memory map, board revision, exact wireless chip, and complete peripheral bill of materials remain open.

*Project: MotoDarwin18*


## Public source provenance update — 2026-11-08

Motorola's public kernel-source tracker links two XT2135-2 European Android firmware build identifiers to published `kernel-msm` source release tags. This confirms a source-publication trail for the Android/Linux kernel side only. It does not establish a firmware-to-XNU handoff, UEFI availability, XNU `boot_args` producer semantics, SecureDT format, or exact board-revision mapping. See [XT2135-2 Public Firmware and Source Evidence Register](../research/firmware/XT2135_2_PUBLIC_SOURCE_EVIDENCE.md).


## Board-revision evidence update — 2026-11-08

Motorola confirms XT2135-2 / MC38C / moto g60 vision. The public shared hanoip Android device tree confirms the software-family identity but does not identify a physical PCB revision or map XT2135-2 to DVT1 or DVT2. A third-party broad XT2135-X service-document listing is unverified and not sufficient to resolve the mapping. Keep board revision and overlay selection open. See [XT2135-2 Board-Revision Evidence Audit](../research/firmware/XT2135_2_BOARD_REVISION_AUDIT.md).


## Confirmed-versus-inferred reconciliation — 2026-11-08

See [XT2135-2 Confirmed Platform Facts and XNU Compatibility Review](../research/firmware/XT2135_2_CONFIRMED_PLATFORM_FACTS.md) for the consolidated evidence matrix.

Key distinction: Motorola confirms XT2135-2 / MC38C identity and regulatory radio capabilities, and its public tracker links named XT2135-2 Android builds to Android/Linux kernel source releases. Neither establishes the board revision, installed component population, firmware-to-XNU ABI, memory ownership, SecureDT handoff or pre-OS service availability. Detailed Hanoip/SDMMAGPIE hardware descriptions remain family-level clues.


## Public firmware / board-revision documentation follow-up — 2026-11-08

The additional public-source review found Motorola's official Right to Repair documentation channel, but the linked partner portal could not be inspected and no XT2135-2-specific board assembly or revision was verified. Third-party listings describe broad XT2135-X / G60 / G40 service-document packages but do not authenticate MC38C-specific board population or map the phone to DVT1/DVT2.

Motorola issue #574 confirms an Android kernel-source publication trail for a named XT2135-2 firmware build, not the firmware-to-XNU entry contract. Keep PCB revision, DVT overlay, exact BOM, firmware entry state, memory ownership and device-tree handoff unknown. See [XT2135-2 Firmware and Board-Revision Documentation Follow-up](../research/firmware/XT2135_2_FIRMWARE_BOARD_REVISION_FOLLOWUP.md).
