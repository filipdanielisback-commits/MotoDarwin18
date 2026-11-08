# XT2135-2 Confirmed Platform Facts and XNU Compatibility Review

**Project:** MotoDarwin18  
**Target:** Motorola moto g60 vision, XT2135-2 / MC38C  
**Review date:** 2026-11-08  
**Pinned XNU baseline:** `xnu-11215.1.10`  
**Status:** Evidence classification and source review; no executable kernel patch

## 1. Purpose and evidence vocabulary

This review reconciles Motorola's exact-model regulatory evidence, Motorola's Android kernel-source publication trail, and the community `hanoip` / SDMMAGPIE Linux source family. It then compares only appropriately scoped facts against the pinned XNU startup and early-platform requirements.

Use these labels strictly:

- **Confirmed — exact model:** explicitly stated in an authoritative source naming XT2135-2 / MC38C.
- **Confirmed — source provenance:** an official source trail ties an Android firmware build to a published Android/Linux kernel source release. This does not confirm boot-firmware behavior.
- **Family-level clue:** present in a shared G40 Fusion / G60 `hanoip` software tree or SoC DTS, but not mapped to the exact XT2135-2 board revision.
- **Secondary / reported:** present in non-primary specification material or general platform references, not established by the exact-model Motorola declaration.
- **Unknown:** the evidence reviewed does not establish the fact. “Not observed” is not proof of absence.

## 2. Facts confirmed for XT2135-2

### 2.1 Motorola exact-model declaration

Motorola's EU Declaration of Conformity identifies:

- Market model: **moto g60, XT2135-2**
- Type name: **MC38C**
- Product description: mobile cellular phone with Bluetooth, WLAN, GPS, GLONASS, Galileo, FM receive and NFC
- Declared radio capabilities include IEEE 802.11a/b/g/n/ac and Bluetooth 5.0, alongside the listed GSM, UMTS and LTE bands
- Declaration issue date: 2021-03-05

Motorola's compliance index separately lists XT2135-1 as MC38B / moto g60 and XT2135-2 as MC38C / moto g60 vision. Do not merge the two variants' radio bands or model claims.

Sources:
- [Motorola EU Declaration of Conformity — XT2135-2 / MC38C](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf)
- [Motorola Declarations of Conformity index](https://en-us.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity)

The declaration is regulatory evidence. It does not identify the WLAN/Bluetooth silicon, antenna topology, driver, calibration data, or the implementation of any pre-OS service.

### 2.2 Motorola Android kernel-source provenance

Motorola's public `MotorolaMobilityLLC/kernel-msm` source-publication tracker links named XT2135-2 European Android firmware build identifiers to Motorola kernel-source release tags:

- `MMI-S2RIS32.32-20-9-9-2-1`
- `MMI-S2RIS32.32-20-9-9-2-3`

This confirms a public source-provenance trail for the Android/Linux kernel associated with those named builds. It does **not** establish the bootloader or firmware implementation, a UEFI interface, the firmware-to-kernel entry state, an Apple `boot_args` producer, SecureDT format, memory ownership, or a handoff usable by XNU.

Sources:
- [Motorola kernel-msm source tracker issue #559](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/559)
- [Motorola kernel-msm source tracker issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574)

## 3. Reported platform facts that are not exact-model confirmed

| Claim | Evidence class | What can safely be said |
|---|---|---|
| Snapdragon 732G / SM7150-AC | Secondary / reported | Commonly reported for this model and consistent with Qualcomm platform material; the reviewed Motorola declaration does not name the SoC. Do not treat the SoC identity as established by that declaration. |
| Kryo 470 CPU, Adreno 618 GPU, Hexagon 688 | SoC-level specification | Qualcomm describes these as Snapdragon 732G platform features; that is not proof of exact handset configuration or exposed firmware interfaces. |
| 6 GB RAM / 128 GB storage, 6000 mAh battery, display dimensions and camera resolutions | Secondary / reported | Useful consumer-spec leads only; not a board-level bill of materials or memory map. |
| MC50 battery component | Exact-model declaration reference, installed part unknown | Motorola's declaration material lists MC50 among compatible components; this does not prove which battery supplier or exact component is installed in a particular unit. |

## 4. Facts inferred only from the shared hanoip / SDMMAGPIE source family

The public community Android device tree describes itself as a shared Moto G40 Fusion / Moto G60 (`hanoip`) device tree. Its `BoardConfig.mk` and `board-info.txt` use `hanoip` as Android build / OTA / bootloader-board identity. These strings are software configuration identifiers, not physical PCB revision identifiers.

The following remain **family-level clues**, not confirmed XT2135-2 component facts:

| Area | Shared-source observation | Exact XT2135-2 conclusion |
|---|---|---|
| CPU topology | Shared SoC tree describes an eight-core topology | Exact unit topology and firmware description not independently confirmed |
| Interrupts | GICv3 and Qualcomm PDC nodes | Strong family-level architecture clue; exact routing, ownership and XNU integration unknown |
| Timers | Armv8 generic timer listed at 19.2 MHz and a memory-mapped timer block | Family-level description; exact enabled source and XNU timebase contract unknown |
| Memory | Reserved-memory carveouts for firmware and peripherals | Not a complete physical DRAM map or ownership record |
| Storage | UFS host and SD-card controller paths; eMMC-labelled alias also present | Exact installed flash component and final target controller configuration unknown |
| Display | Tianma ILI7807S 678-class 1080x2460 MIPI-DSI panel include and refresh-mode descriptions | Candidate for shared family configuration; exact XT2135-2 panel and display path unconfirmed |
| Touch | Ilitek SPI touchscreen node | Candidate family configuration; exact controller and pre-OS input interface unconfirmed |
| Wireless | WCN3990 Bluetooth node; Android module list includes `qca_cld3_wlan.ko` | WLAN module name is not a chip part number; exact combo-chip and firmware unknown |
| Power | PM6150/PM6150L descriptions and MC50 battery profiles | Exact PMIC population, regulators and installed battery variant unknown |
| Audio | WCD937x / AW882xx descriptions in shared overlays | Exact codec/amplifier population unknown |
| Sensors / USB / thermal | Shared family nodes and configuration | Exact component population, wiring and active configuration unknown |

Sources:
- [Shared hanoip Android device tree](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [Hanoip platform evidence register](../soc/HANOIP_PLATFORM_EVIDENCE.md)
- [XT2135-2 board-revision audit](XT2135_2_BOARD_REVISION_AUDIT.md)

### 4.1 Board revision remains unresolved

No authoritative source reviewed maps XT2135-2 / MC38C to a specific physical PCB revision or to the Hanoip DVT1 versus DVT2 overlay. The `hanoip` board name does not resolve this. Do not choose a DVT overlay or make a DVT-specific hardware claim.

## 5. Reconciled XNU compatibility assessment

The comparison target is the pinned Apple XNU source baseline `xnu-11215.1.10`, commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`. The source review records XNU-side consumer expectations; it does not establish a Motorola producer contract.

| XNU dependency / contract | XNU-side finding | Exact XT2135-2 evidence | Assessment |
|---|---|---|---|
| ARM64 entry context | Startup expects a valid architecture and machine entry context | ARM64-capable platform is reported; exact entry state, exception level, stack, MMU/cache state and pointer accessibility undocumented | **Critical unknown** |
| `boot_args` ABI | Pinned XNU declares an Apple-specific structure and consumes revisioned fields | No Motorola producer or documented translator for this ABI | **Not demonstrated** |
| Memory layout and ownership | XNU VM consumes physical/virtual bases, sizes and kernel-data boundary | Shared Linux carveouts only; no exact complete RAM map or firmware ownership contract | **Critical unknown** |
| SecureDT representation | Pinned SecureDT uses Apple-specific in-memory node/property records | Reviewed Moto evidence is Linux DTS/FDT-family source; no exact firmware handoff representation documented | **Compatibility unproven** |
| Required DRAM properties | Reviewed XNU ARM64 path consumes `/chosen/dram-base` and `/chosen/dram-size` | No exact-target producer evidence for names, widths, encodings or values | **Critical producer evidence missing** |
| CPU topology / machine identity | XNU queries CPU and machine/platform information | Family topology clue only; no XNU machine identifier or exact handoff tree | **Unknown** |
| Interrupt controller | XNU requires Platform Expert interrupt initialization | GICv3/PDC family clue; routing, ownership and XNU backend absent | **Hardware clue only** |
| Timer / timebase | XNU requires early clock/timebase and timer interrupt services | 19.2 MHz generic timer family clue; exact source and XNU backend absent | **Hardware clue only** |
| Console / diagnostics | Early Platform Expert debug and console services are configuration-dependent | No exact-model console handoff or XNU backend evidence | **Unknown** |
| Video metadata / display | XNU records boot video metadata; later display requires a separate backend | Panel family clue only; no verified pre-OS framebuffer/GOP or XNU display driver | **Unknown** |
| Touch input | Not a core XNU entry ABI requirement; relevant to a loader UI | Ilitek family clue only; no exact pre-OS input protocol evidence | **Unknown** |
| Storage, wireless, audio, sensors, power | Later platform and system usability dependencies | Family-level clues only, no XNU drivers or exact BOM | **Not implemented / exact hardware partly unknown** |

### 5.1 Important format distinction

The pinned XNU SecureDT representation is not the standard flattened device-tree binary format used by Linux device-tree workflows. Similar node/property concepts do not establish binary compatibility. The exact XT2135-2 firmware handoff format is unknown; therefore it is not valid to conclude that the firmware passes an FDT unchanged, an Apple SecureDT tree, or any other specific format.

The fact that a property was not found in the reviewed Linux source is not proof that the property is absent from the actual firmware handoff.

### 5.2 Compatibility conclusion

The project has a useful exact-model identity and regulatory radio record, plus a Motorola Android kernel-source provenance trail. It does not yet have the producer-side firmware contract or exact board inventory required to compare against XNU's early boot consumers.

This is a **missing evidence / missing platform integration** problem, not a demonstrated defect in the pinned XNU source.

## 6. Executable source-patch decision

**Decision: no executable XNU source patch is justified by the current evidence.**

In particular, do not change `boot.h`, `pe_init.c`, `arm_init.c`, SecureDT, ARM64 VM startup, interrupt code, or timer code merely to accommodate an assumed Moto handoff.

A future executable patch can be reconsidered only when all of the following exist:

1. An immutable XNU source location and exact consumer behavior are identified.
2. An authoritative producer-side contract applies to XT2135-2 and, where relevant, its exact board revision.
3. A concrete semantic, layout, encoding or lifecycle mismatch is demonstrated between producer and consumer.
4. The issue is proven to be an XNU source defect or a narrowly defined portability limitation, rather than an unknown producer feature or missing platform implementation.
5. The proposed source change is minimal, reviewed for file-level license/provenance, and has a source-only test strategy.

If the eventual issue is that Motorola firmware does not produce Apple's ABI, that alone does not prove an XNU bug; it may instead require a separately specified platform integration layer. This review does not design or construct such a handoff.

## 7. Next research milestones

1. Keep the board revision and DVT overlay mapping unresolved until authoritative evidence ties them together.
2. Maintain a confirmed-versus-family-level platform inventory as new sources appear.
3. Continue source-level review of XNU consumer assumptions and configuration-dependent startup paths.
4. Reopen executable patch consideration only after an exact producer/consumer mismatch is documented.
5. Keep all work at public-source, documentation and host-side review level; no device modification or boot compatibility claim is made.

## 8. Conclusion

**Confirmed:** XT2135-2 / MC38C identity and the Motorola-declared regulatory radio capabilities; a Motorola public Android/Linux kernel-source trail for named XT2135-2 builds.

**Family-level only:** the detailed GICv3/PDC, timer, storage, display, touch, WLAN, PMIC, audio and other peripheral descriptions from shared hanoip / SDMMAGPIE sources.

**Unknown:** physical board revision, DVT mapping, exact BOM, complete memory map, firmware-to-OS ABI, CPU entry state, exact device-tree handoff, XNU machine mapping and all device-specific XNU services.

**Patch disposition:** no executable kernel patch at this time. No Moto G60 XNU boot or iOS compatibility is demonstrated.

*Research and source-review document only.*
