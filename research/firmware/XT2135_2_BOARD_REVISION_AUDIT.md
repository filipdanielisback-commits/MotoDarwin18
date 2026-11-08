# XT2135-2 Board-Revision Evidence Audit

**Target:** Motorola XT2135-2 / MC38C / moto g60 vision  
**Review date:** 2026-11-08  
**Status:** Exact commercial model confirmed; physical board revision and DVT overlay mapping unresolved.

## 1. Question

Can public evidence map the exact XT2135-2 model to a specific motherboard revision or to a specific DVT1/DVT2 overlay in the shared hanoip Android/Linux source tree?

## 2. Evidence that is confirmed

### 2.1 Motorola model identity

Motorola's declarations-of-conformity index lists XT2135-2 as MC38C / moto g60 vision, and separately lists XT2135-1 as MC38B / moto g60.

Source: [Motorola — Declarations of Conformity](https://fr-fr.support.motorola.com/app/answers/detail/a_id/167829).

**Conclusion:** XT2135-2 is the exact regulatory model identifier for this project. This is not a motherboard revision identifier.

### 2.2 Shared hanoip Android device-tree identity

The public community repository [motorola-sm6150-devs/device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/tree/lineage-20) describes itself as the Android device tree for Motorola Moto G40 Fusion / Moto G60 (hanoip).

Reviewed files on branch lineage-20:

- [README.md](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/README.md) explicitly names the shared G40 Fusion / G60 family.
- [BoardConfig.mk](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/BoardConfig.mk) sets TARGET_OTA_ASSERT_DEVICE := hanoip and TARGET_BOOTLOADER_BOARD_NAME := hanoip; it also selects a shared kernel configuration including moto-sdmmagpie-hanoip.config.
- [board-info.txt](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/board-info.txt) contains require board=hanoip.

**Conclusion:** these Android build files establish a shared software device identity named hanoip. They do not identify a physical PCB revision or select DVT1 versus DVT2 for an XT2135-2 unit.

### 2.3 Shared family source and DVT overlay leads

The previously reviewed shared Hanoip kernel source contains DVT1 and DVT2 overlay material. This is evidence that the source family models more than one design/variant. The reviewed public Android device-tree files above do not map XT2135-2 / MC38C to either overlay.

Source context and limitations are recorded in [HANOIP_PLATFORM_EVIDENCE.md](../soc/HANOIP_PLATFORM_EVIDENCE.md).

**Conclusion:** existence of DVT1 and DVT2 is not a mapping rule. Do not choose one based only on the XT2135-2 suffix, regional firmware channel, or shared hanoip codename.

## 3. Secondary lead — not confirmed

A third-party repair-document listing advertises a service manual/schematic package described broadly as “XT2135-X, G60 and G40” / “Hanoi (XT2135-x)”. The listing does not establish that the package is an official Motorola publication, does not identify the exact XT2135-2 PCB revision, and its underlying documents have not been independently authenticated or reviewed for revision mapping.

Reference: [EletrônicaBR — XT2135-X / G60 / G40 service-manual listing](https://eletronicabr.com/en/files/file/42034-service-manual-for-motherboard-xt2135-x-g60-and-g40-schematic/).

**Evidence classification:** unverified secondary lead only. It must not be used to mark any component, board revision, or DVT mapping as confirmed.

## 4. Evidence matrix

| Claim | Evidence | Confidence | What remains unresolved |
|---|---|---|---|
| XT2135-2 is MC38C / moto g60 vision | Motorola conformity index | Confirmed model identity | No PCB revision given |
| XT2135-1 is separately listed as MC38B / moto g60 | Motorola conformity index | Confirmed model distinction | Does not establish internal board differences |
| Moto G40 Fusion / Moto G60 share a public hanoip Android device tree | Community repository README | Confirmed repository scope | Does not prove identical hardware population |
| Android build identity is hanoip | BoardConfig and board-info | Confirmed software build label | Not a physical revision ID |
| Shared Hanoip kernel source contains DVT1 and DVT2 overlay material | Prior source-tree review | Family-level source fact | No exact XT2135-2 overlay mapping |
| A service-document package is advertised for XT2135-X family | Third-party listing metadata | Unverified lead | Authenticity, content and exact model/revision applicability unknown |
| Exact XT2135-2 board revision | No authoritative exact-model mapping located | Unknown | Requires reliable Motorola or independently authenticated board-level evidence |
| XT2135-2 maps to DVT1 or DVT2 | No mapping evidence located | Unknown | Must remain unselected |

## 5. Confirmed platform facts versus family clues

### Confirmed for the exact model
- Regulatory identifier: XT2135-2.
- Motorola type name: MC38C.
- Motorola product name: moto g60 vision.

### Confirmed only for the shared software source family
- Android device-tree codename: hanoip.
- Android BoardConfig uses hanoip as OTA assertion and bootloader board-name string.
- Shared source tree includes platform-family DTS and DVT overlay material.

### Still unconfirmed for an individual XT2135-2 unit
- PCB assembly number and revision.
- DVT1 versus DVT2 mapping.
- Exact display and touch component variants.
- Exact PMIC, battery supplier, storage component, wireless combo-chip, and sensor population.
- Full physical memory map and reserved-region ownership.
- Firmware handoff format and producer-side contract.

## 6. Decision

**Do not select a DVT overlay for XT2135-2 yet.** The evidence currently confirms the model identity and shared software family, not the physical board revision.

No hardware-specific kernel source change is justified by this audit. In particular, do not hard-code DVT-specific memory, interrupt, display, touch, PMIC, or peripheral assumptions based on family-level files.

## 7. Next evidence milestone

Seek a trustworthy source that explicitly links XT2135-2 / MC38C to a board assembly identifier or PCB revision, and then a source that maps that identifier to the DVT overlay used by the relevant kernel DTS. If no public source makes that link, keep the mapping explicitly unknown.

This milestone is documentation and public-source review only. It does not involve device modification, firmware extraction, boot configuration changes, or boot payload work.

## 8. References
- [Motorola conformity declarations](https://fr-fr.support.motorola.com/app/answers/detail/a_id/167829)
- [Hanoip Android device-tree README](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/README.md)
- [Hanoip BoardConfig.mk](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/BoardConfig.mk)
- [Hanoip board-info.txt](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/board-info.txt)
- [Third-party XT2135-X service-document listing — unverified lead](https://eletronicabr.com/en/files/file/42034-service-manual-for-motherboard-xt2135-x-g60-and-g40-schematic/)
- [Hanoip platform evidence](../soc/HANOIP_PLATFORM_EVIDENCE.md)
- [XT2135-2 public source evidence register](XT2135_2_PUBLIC_SOURCE_EVIDENCE.md)

*Project: MotoDarwin18*