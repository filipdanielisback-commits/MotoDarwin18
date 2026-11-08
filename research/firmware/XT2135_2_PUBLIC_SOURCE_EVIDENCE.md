# XT2135-2 Public Firmware and Source Evidence Register

**Project:** MotoDarwin18  
**Target:** Motorola XT2135-2 / MC38C / moto g60 vision  
**Review date:** 2026-11-08  
**Status:** Public-source provenance review; firmware handoff contract remains unknown.

## 1. Purpose

Record publicly accessible manufacturer and community source references relevant to identifying the exact XT2135-2 target and locating source material. Distinguish evidence that identifies the model or documents Android kernel source publication from evidence that would actually establish a firmware-to-XNU handoff.

This is a source-provenance exercise only. It does not require downloading or modifying firmware, changing device configuration, or interacting with a handset.

## 2. Exact-model identity — manufacturer evidence

Motorola's EU product-compliance index lists:

| Model | Type name | Product name |
|---|---|---|
| XT2135-2 | MC38C | moto g60 vision |
| XT2135-1 | MC38B | moto g60 |

Source: [Motorola — EU Product Compliance Statements / Declarations of Conformity](https://en-gb.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity), 2021 product listing.

**What this establishes:** XT2135-2 is a distinct regulatory model identifier and Motorola associates it with MC38C / moto g60 vision.

**What it does not establish:** motherboard revision, DVT overlay selection, component population, firmware implementation, memory map, or an OS handoff contract.

## 3. Motorola-published Android kernel source trail

Motorola's public `MotorolaMobilityLLC/kernel-msm` repository is the manufacturer's kernel-source repository.

Two source-publication tracker issues identify exact XT2135-2 European firmware build strings and link to Motorola-published source releases:

| Firmware build named in issue | Motorola source release tag | Publication record |
|---|---|---|
| `XT2135-2_HANOIP_RETEU_12_S2RIS32.32-20-9-9-2-1_...` | `MMI-S2RIS32.32-20-9-9-2-1` | [Motorola kernel-msm issue #559](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/559) |
| `XT2135-2_HANOIP_RETEU_12_S2RIS32.32-20-9-9-2-3_...` | `MMI-S2RIS32.32-20-9-9-2-3` | [Motorola kernel-msm issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574) |

In issue #559, a Motorola contributor states that the code was released and links the `MMI-S2RIS32.32-20-9-9-2-1` tag. In issue #574, a Motorola contributor links the `MMI-S2RIS32.32-20-9-9-2-3` tag and closes the request as completed.

**What this establishes:** Motorola publicly published Android/Linux kernel source associated by its own tracker with these XT2135-2 firmware build identifiers.

**What it does not establish:** that this repository contains Motorola's complete boot firmware, first-stage/second-stage bootloader, UEFI implementation, secure monitor, or an XNU-compatible producer. A Linux kernel source release is not a firmware handoff specification. It does not tell us the exact `boot_args` values, SecureDT representation, memory ownership, entry CPU state, or pre-OS display/input services expected by the pinned XNU baseline.

Repository: [MotorolaMobilityLLC/kernel-msm](https://github.com/MotorolaMobilityLLC/kernel-msm)  
Release tags: [S2RIS32.32-20-9-9-2-1](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-1) · [S2RIS32.32-20-9-9-2-3](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)

## 4. Shared hanoip family source — secondary evidence

The public community organization describes its repositories as stable `hanoip` trees for the Moto G40 Fusion / Moto G60 family and is marked archived by GitHub.

Source: [moto-hanoip organization](https://github.com/moto-hanoip/).

The shared device tree also describes itself as the Android device tree for Motorola Moto G40 Fusion / Moto G60 (`hanoip`): [motorola-sm6150-devs/device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip).

**Evidence class:** community-maintained Android/Linux family source, not a Motorola board schematic or exact XT2135-2 revision map.

**Limitations:** shared family sources cannot by themselves select DVT1 or DVT2 for a particular XT2135-2 unit. They cannot prove which hardware components are populated in every unit or what the phone's firmware hands to an operating system.

## 5. Handoff evidence matrix

| Required information for XNU comparison | Evidence located in this review | Status |
|---|---|---|
| Exact regulatory model identity | Motorola lists XT2135-2 / MC38C / moto g60 vision | Confirmed |
| Motorola Android kernel-source publication for named XT2135-2 builds | Motorola tracker issues link to source release tags | Confirmed publication trail |
| Exact motherboard revision / DVT overlay mapping | No authoritative XT2135-2 mapping located | Unknown |
| Firmware/bootloader source and versioned interface | Kernel source publication is not boot firmware documentation | Unknown |
| Firmware-to-OS entry contract | No exact-model producer specification located | Unknown |
| XNU `boot_args` producer semantics | No exact-model source or specification located | Unknown |
| Device-tree format supplied at handoff | Android/Linux family DTS evidence only; actual firmware handoff representation unknown | Unknown |
| Device-tree pointer lifetime and ownership | No exact-model producer contract located | Unknown |
| Physical memory map and reserved-region ownership | Shared family carveouts are not a complete exact-target map | Unknown |
| CPU entry state / execution environment | No exact-model producer documentation located | Unknown |
| Pre-OS display and input services | No exact-model firmware protocol evidence located | Unknown |

## 6. Research decision

The newly located Motorola kernel-source release trail improves source provenance for the Android kernel side of the project. It does **not** close the firmware-to-XNU handoff gap.

Do not treat a published Linux kernel tree as proof that Motorola's boot firmware is open, that its bootloader implements UEFI, or that it emits Apple's SecureDT format. Do not infer XNU compatibility from the existence of a matching Android kernel source release.

No executable kernel patch is justified by this evidence alone.

## 7. Next safe research task

Continue a public-documentation audit for exact-model board revision and firmware interface descriptions. Prioritize manufacturer-authored regulatory/service documents and source metadata. If no exact handoff specification is public, record that absence as an unresolved research limit rather than trying to infer it from unrelated Android data.

This remains a source and documentation task only. No device changes, firmware extraction, boot configuration, handoff construction, or boot payload work is part of this milestone.

## 8. Sources

- [Motorola EU Product Compliance Statements](https://en-gb.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity)
- [Motorola kernel-msm issue #559](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/559)
- [Motorola kernel-msm issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)
- [Motorola kernel-msm source release 2-1](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-1)
- [Motorola kernel-msm source release 2-3](https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-S2RIS32.32-20-9-9-2-3)
- [moto-hanoip community organization](https://github.com/moto-hanoip/)
- [Shared hanoip Android device tree](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [Boot handoff field reference](../../docs/BOOT_HANDOFF_FIELD_REFERENCE.md)
- [ARM64 boot contract compatibility audit](../../xnu/source-reviews/ARM64_BOOT_CONTRACT_AUDIT.md)

*Project: MotoDarwin18*
