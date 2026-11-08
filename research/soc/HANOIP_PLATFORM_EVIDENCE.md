# Hanoip / SDMMAGPIE Platform Evidence — Provisional Research

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2  
**Related device codename:** `hanoip` (shared Moto G40 Fusion / Moto G60 source tree)  
**Research date:** 2026-11-08  
**Status:** Community-source evidence; exact XT2135-2 board revision not yet established

## 1. Scope and caution

This note records findings from publicly available Android device configuration and Linux kernel device-tree sources associated with the shared Motorola `hanoip` device family.

The sources are valuable because they expose platform descriptions that are not present in marketing specifications. However:

- The device tree covers Moto G40 Fusion and Moto G60, not only XT2135-2.
- The kernel source is a LineageOS `lineage-20` branch, not an official Motorola hardware schematic or a vendor programming manual.
- Multiple board-revision overlays exist. The exact overlay corresponding to a particular XT2135-2 unit has not been established.
- Generic SoC nodes may describe capabilities or components that are not enabled in every handset configuration.
- A Linux device-tree declaration is evidence of how that Linux configuration describes hardware; it is not proof of Darwin/XNU support.

Treat findings below as **candidate platform-family evidence**, unless a source explicitly ties them to the exact XT2135-2 revision.

## 2. Sources inspected

### Device configuration

- [motorola-sm6150-devs/device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip) — README describes an Android device tree for Moto G40 Fusion / Moto G60 (`hanoip`).
- [BoardConfig.mk](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/BoardConfig.mk) — labels the bootloader board `hanoip`, Android build platform `sm6150`, and kernel source as `kernel/motorola/sm6150`.
- [modules.load](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/modules.load) — lists the device configuration's expected kernel modules, including `qca_cld3_wlan.ko`.

### Kernel device tree

- [sdmmagpie.dtsi](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi) — shared SoC-level device-tree description.
- [sdmmagpie-moto-base.dtsi](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-moto-base.dtsi) — Motorola platform base and reserved-memory adjustments.
- [sdmmagpie-hanoi-base.dts](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-base.dts) — Hanoi-family base description.
- [sdmmagpie-hanoip-common-overlay.dtsi](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi) — common hanoip overlay.
- [sdmmagpie-hanoip-dvt1-overlay.dts](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt1-overlay.dts) and [DVT2 overlay](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt2-overlay.dts) — separate board-revision overlays.
- [hanoi-panel.dtsi](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/hanoi-panel.dtsi) — panel selection and DSI configuration.
- [hanoi_battery_thermal_overlay.dtsi](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/hanoi_battery_thermal_overlay.dtsi) — battery profiles, charger, and thermal descriptions.
- [sdmmagpie-hanoi-touchscreen.dtsi](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-touchscreen.dtsi) — touchscreen controller description.

The Qualcomm Snapdragon 732G product brief identifies SoC part number SM7150-AC. The Android build files use `sm6150` labels, while the kernel device tree names the SoC family `sdmmagpie`. These are source-tree naming conventions that need careful reconciliation; do not infer a different physical chipset from a directory or build-variable name alone.

## 3. Findings by subsystem

### 3.1 Memory layout

**Finding:** The shared SoC device tree contains a `reserved-memory` section with carveouts for secure/firmware and peripheral purposes, including hypervisor, shared memory, modem, camera, DSP, WLAN, and other regions. The Motorola base and Hanoi board files further adjust some reservations and add a secure-display shared-memory pool.

**What this establishes:** The Linux platform configuration expects multiple reserved physical-memory regions and device-specific carveouts.

**What it does not establish:** These entries are not a complete physical DRAM map. They do not independently establish the installed RAM size, all usable RAM banks, exact memory map for every XT2135-2 revision, or the complete firmware-reserved layout.

**Status:** Partial platform-family evidence; exact handset memory map remains **Unknown**.

### 3.2 Interrupt controller

**Finding:** `sdmmagpie.dtsi` describes an `arm,gic-v3` interrupt controller, with distributor and redistributor register regions, plus a Qualcomm PDC interrupt-controller node.

**What this establishes:** The shared SDMMAGPIE Linux platform description uses a GICv3-based interrupt architecture with a Qualcomm power-domain controller description.

**What it does not establish:** The complete XT2135-2 interrupt routing, all device interrupt assignments, firmware ownership, or whether a future XNU baseline can use this integration unchanged.

**Status:** GICv3/PDC are strong platform-tree clues; exact board routing remains **Unverified**.

### 3.3 Timers and timekeeping

**Finding:** The same SoC device tree declares an Armv8 generic timer with a listed frequency of 19.2 MHz. It also describes a memory-mapped timer block and timer-frame entries.

**What this establishes:** The Linux platform tree provides a concrete timer description to investigate.

**What it does not establish:** That every timer source is enabled on every board revision, that the listed frequency is the complete timekeeping story, or that XNU can directly reuse the Linux configuration.

**Status:** 19.2 MHz Arm generic-timer description is a platform-family finding; exact target configuration remains **Unverified**.

### 3.4 Storage

**Finding:** The SoC device tree aliases identify an embedded UFS host, an SDC1 eMMC slot, and an SDC2 SD-card slot. The device configuration references Android partitions under a UFS host path. The common Motorola overlay supplies UFS PHY/host configuration and enables the relevant storage nodes.

**What this establishes:** The Linux source configuration describes a UFS storage path and a separate SD-card controller path. The source tree also contains an eMMC-labelled SDC1 alias, whose exact role in the final target configuration needs further checking.

**What it does not establish:** The exact flash component manufacturer/model, its capacity in a particular XT2135-2, or a Darwin-compatible storage driver.

**Status:** UFS host path and SD-card controller are strong configuration evidence; exact flash component remains **Unknown**.

### 3.5 Display controller and panel

**Finding:** The Hanoi panel include selects a panel description named `dsi-panel-mot-tianma-ili7807s-678-1080x2460-video.dtsi`. The board-specific panel file configures a primary MIPI DSI display path and lists 60 Hz and 120 Hz dynamic refresh modes. It also references PM6150L backlight support and panel power/reset controls.

**What this establishes:** A Tianma / ILI7807S 678-class 1080 × 2460 panel is a strong candidate for the shared Hanoi/G60 family Linux configuration. The display path is described through Qualcomm MDSS/SDE and DSI nodes.

**What it does not establish:** The panel supplier/model in every XT2135-2 unit, the physical display-controller silicon as a standalone component, or an XNU display driver.

**Status:** Panel and DSI path are **Probable for the hanoip family**, not yet exact-model confirmed.

### 3.6 Wireless

**Finding:** The shared SoC device tree contains a Bluetooth node with compatible string `qca,wcn3990`. The hanoip Android module list includes `qca_cld3_wlan.ko`.

**What this establishes:** The shared source configuration has a Qualcomm WCN3990 Bluetooth description at the SoC-tree level and expects a Qualcomm CLD3 WLAN kernel module in its Android software configuration.

**What it does not establish:** The exact Wi-Fi combo-chip fitted to XT2135-2, whether the generic WCN3990 node is the selected hardware on every board revision, or the full firmware and calibration dependencies. The WLAN module name alone is not a chip part number.

**Status:** WCN3990 is a **candidate Bluetooth platform description**; Wi-Fi chip identity remains **Unknown**.

### 3.7 Power management and thermal

**Finding:** The Hanoi platform overlays reference PM6150 and PM6150L power-management devices, their regulator/ADC/charger/gauge interfaces, and thermal zones. The battery/thermal overlay includes MC50 battery profiles from ATL and SUNWODA, both described as 6000 mAh profiles.

**What this establishes:** The Linux configuration uses a PM6150/PM6150L-family power-management description and contains alternative MC50 battery profiles and thermal monitoring configuration.

**What it does not establish:** The exact PMIC package population on every XT2135-2 board revision, which battery supplier is present in a particular unit, or the complete electrical design.

**Status:** PM6150/PM6150L and MC50 profiles are **Probable hanoip-family evidence**; exact unit bill of materials remains **Unverified**.

## 4. Consolidated evidence matrix

| Area | Current evidence | Confidence for XT2135-2 | Still unknown |
|---|---|---|---|
| Memory | Reserved-memory carveouts in shared SoC/board tree | Low to medium | Complete physical map and revision-specific reservations |
| Interrupts | GICv3 and Qualcomm PDC nodes | Medium | Full target routing and firmware ownership |
| Timers | Armv8 generic timer, 19.2 MHz; memory-mapped timer description | Medium | Exact enabled sources and target-specific behavior |
| Storage | UFS host path and SD-card controller description | Medium | Exact storage component and full controller configuration |
| Display | Tianma ILI7807S panel include; MIPI DSI path | Medium | Exact panel in XT2135-2 unit and controller implementation |
| Wireless | WCN3990 Bluetooth node; CLD3 WLAN module listed | Low to medium | Exact combo-chip, firmware, calibration, and variant selection |
| Power | PM6150/PM6150L and MC50 battery profiles | Medium | Exact board BOM and installed battery vendor |

Confidence describes the relevance of the source to the exact model, not whether the source file itself contains the stated text.

## 5. Highest-priority unresolved questions

1. Which board-ID / DVT overlay corresponds to the exact XT2135-2 hardware revision?
2. Can an official Motorola source release or exact-model regulatory document corroborate the panel, PMIC, and wireless components?
3. What is the complete physical memory map, including all RAM banks and reserved regions?
4. What are the exact GIC/PDC routing and timer details for the selected board revision?
5. Which storage node is active for internal flash in the exact device configuration, and what is the actual storage component?
6. Does the WCN3990 Bluetooth description correspond to the same combo module used for WLAN in this handset?
7. Which PM6150/PM6150L components and MC50 battery profile are actually populated in the target unit?

## 6. Licensing and reuse

The cited kernel device-tree files contain Linux Foundation / kernel source copyright notices and GPL version 2 licensing statements. The Android device configuration repository identifies its own files as Apache-2.0.

This document summarizes findings and links to upstream sources. Do not copy kernel source files into MotoDarwin18 under the repository's MIT license. Any future source reuse requires file-level license and provenance review.

## 7. Conclusion

The shared hanoip / SDMMAGPIE source tree significantly narrows the research questions. It provides useful candidates for GICv3, a 19.2 MHz Arm generic timer, UFS and SD-card paths, a Tianma ILI7807S MIPI-DSI panel, WCN3990 Bluetooth, CLD3 WLAN software, and PM6150/PM6150L power management.

These findings are not yet a complete XT2135-2 hardware inventory. They do not establish an XNU port, a loader handoff, or a working driver. The exact board revision and complete memory map remain key gaps.

*Project: MotoDarwin18*


## 8. Additional community Linux FDT sample — 2026-11-08

A separate public community repository, `eng-brener/hanoip-mainline`, contains a pinned expanded DTS snapshot with root model `Motorola Moto G60` and compatible strings `motorola,hanoip` / `qcom,sm7150`. It describes eight CPU nodes, memory and reserved-memory, GIC, generic timer and a simple framebuffer.

This is useful corroborating **Hanoip-family Linux FDT evidence**, but it is not Motorola-authoritative and is not identified as XT2135-2 / MC38C. The repository describes the FDT used by its own U-Boot build, so it must not be treated as the original stock-firmware handoff. It also labels the platform SM7150 / Snapdragon 730G; preserve the distinction from the target's reported SM7150-AC / Snapdragon 732G.

The sample does not contain the XNU-specific `dram-base`, `dram-size`, `arm-io`, `interrupt-controller = "master"`, or `device_type = "timer"` selectors. This absence applies only to this particular file.

Detailed provenance and limitations: [Community Hanoip U-Boot FDT Evidence Audit](../firmware/HANOIP_COMMUNITY_UBOOT_DTB_EVIDENCE_AUDIT.md).
