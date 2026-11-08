# Moto G60 XT2135-2 — Device Hardware Inventory

**Project:** MotoDarwin18  
**Target device:** Motorola Moto G60  
**Exact model:** XT2135-2  
**Platform:** Qualcomm Snapdragon 732G  
**Status:** Initial research; board-level inventory incomplete  
**Last reviewed:** 2026-11-08

## 1. Purpose and evidence standard

This document records publicly documented information relevant to the exact Motorola Moto G60 XT2135-2. It separates handset-specific evidence from capabilities advertised for the Snapdragon 732G platform.

A published specification does not establish that a usable Darwin/XNU driver exists. A SoC feature does not prove that Motorola implemented, enabled, or exposed that feature in this handset.

Evidence labels:
- **Exact-model primary source:** Motorola documentation explicitly names XT2135-2.
- **Manufacturer/platform source:** Qualcomm documents a SoC capability, not necessarily this handset's implementation.
- **Secondary specification:** useful lead, but should be replaced or corroborated by primary evidence.
- **Unknown:** not established by the sources currently recorded.

## 2. Exact model identification

Motorola's EU Declaration of Conformity identifies the market model as **moto g60, XT2135-2**, type name **MC38C**. It was issued on 2021-03-05. The declaration also identifies the product as a mobile cellular phone with Bluetooth, WLAN, GPS, GLONASS, Galileo, FM receive, and NFC.

Source: [Motorola EU Declaration of Conformity — XT2135-2 (PDF)](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf).

The declaration is stronger exact-model evidence than specifications copied from a similarly named XT2135-1 variant. Do not silently merge details from the two models.

## 3. Main platform

| Component | Reported specification | Evidence scope |
|---|---|---|
| SoC | Qualcomm Snapdragon 732G | Reported for this model; retain source link and verify against exact-model documentation |
| CPU family | Qualcomm Kryo 470, up to 2.3 GHz | Qualcomm SoC-level specification |
| GPU | Qualcomm Adreno 618 | Qualcomm SoC-level specification |
| AI/DSP | Qualcomm Hexagon 688 | Qualcomm SoC-level specification |
| Cellular modem | Qualcomm Snapdragon X15 LTE | Qualcomm SoC-level specification |
| Memory support | LPDDR4/4X, platform support up to 8 GB | Qualcomm SoC capability; not the installed configuration |
| Operating system at launch | Android 11 reported | Secondary specification; exact software build varies |

Qualcomm's product brief lists the Kryo 470 CPU, Adreno 618 GPU, Hexagon 688 processor, X15 LTE modem, and part number SM7150-AC. It explicitly notes that some optional features depend on carrier and OEM selection.

Source: [Qualcomm Snapdragon 732G product brief (PDF)](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf).

## 4. Display

| Component | Reported specification | Status |
|---|---|---|
| Display size | 6.8 inches | Secondary device specification |
| Display technology | IPS LCD | Secondary device specification |
| Resolution | 1080 × 2460 | Secondary device specification |
| Display controller | Unknown | Requires exact component evidence |
| Panel identification | Unknown | Requires exact component evidence |
| Display interface | Unknown | Requires platform/board evidence |

The SoC's maximum display capability must not be confused with the actual panel or display pipeline fitted to this phone.

## 5. Memory and storage

| Component | Reported specification | Status |
|---|---|---|
| RAM configuration | 6 GB configuration reported | Confirm exact regional variant |
| Internal storage | 128 GB configuration reported | Confirm exact regional variant |
| microSD support | Reported | Exact capacity and configuration should be checked against official documentation |
| Storage controller | Unknown | Requires investigation |
| Storage component manufacturer | Unknown | Requires investigation |

Qualcomm's maximum supported memory configuration is a platform limit, not evidence of the amount installed in this handset.

## 6. Cameras

Reported device specifications list:
- Main rear camera: 108 MP
- Ultra-wide rear camera: 8 MP
- Macro rear camera: 2 MP
- Front camera: 32 MP

The exact camera sensor part numbers, camera interfaces, ISP configuration, and firmware dependencies remain unverified. Qualcomm's ISP feature list is not proof of the sensor models or camera modes Motorola enabled.

## 7. Wireless connectivity

Motorola's exact-model declaration lists:
- WLAN standards: IEEE 802.11a/b/g/n/ac
- Bluetooth: version 5.0
- GPS, GLONASS, and Galileo
- NFC
- FM receive
- Cellular standards and supported radio bands as enumerated in the declaration

This is useful handset-level regulatory evidence. It does not identify the Wi-Fi/Bluetooth combo-chip, antenna configuration, firmware, or every region/carrier-specific feature. Motorola notes that not all radio bands may be enabled depending on carrier settings and network availability.

**Important SoC comparison:** Qualcomm's Snapdragon 732G brief lists Wi-Fi 6-ready capabilities and Bluetooth 5.1 for the platform. Motorola's XT2135-2 declaration lists 802.11ac and Bluetooth 5.0. For the actual handset, use the Motorola model-specific declaration; do not promote the higher SoC-level capability to a handset specification.

## 8. Power and battery

| Component | Reported specification | Status |
|---|---|---|
| Battery capacity | 6000 mAh reported | Secondary device specification |
| Battery model | MC50 listed by Motorola as a compatible battery component | Exact-model declaration; confirm whether this is the installed part in a given unit |
| Charging | Fast charging reported | Exact implementation and supported charging modes need verification |
| PMIC | Unknown | Requires investigation |
| Power-management interfaces | Unknown | Requires investigation |

Motorola's declaration lists a Motorola battery component identified as MC50 among compatible components. This does not identify the PMIC or the full power architecture.

## 9. Sensors and other components

The following require exact identification from reliable device-specific sources:
- Accelerometer
- Gyroscope
- Magnetometer
- Proximity sensor
- Ambient-light sensor
- Fingerprint reader
- Audio codec and amplifier
- Speakers and microphones
- Vibration motor
- USB controller
- Touchscreen controller

No specific chip model should be assumed until supported by evidence.

## 10. XNU compatibility research areas

These are research targets, not completed implementations:

| Area | Research objective |
|---|---|
| CPU initialization | Understand the ARM64 platform requirements |
| Interrupt controller | Identify the interrupt architecture and routing |
| Device description | Identify the hardware description available to software |
| Memory management | Establish physical memory layout and reserved regions |
| Timers | Identify platform timer interfaces |
| Storage | Identify the storage controller and access requirements |
| Display | Research panel, controller, and initialization dependencies |
| USB | Identify controller and platform interfaces |
| Audio | Identify audio hardware and software dependencies |
| Wireless | Research Wi-Fi/Bluetooth hardware and firmware dependencies |
| Power management | Document power, clock, and thermal-management requirements |

## 11. Remaining unknown hardware information

The following remain unconfirmed for the exact XT2135-2:
- Motherboard revision and exact component population
- Exact display panel, controller, and touchscreen controller
- Wi-Fi/Bluetooth chip identification and firmware dependencies
- Camera sensor part numbers and bus topology
- Audio codec and amplifier identification
- PMIC, regulators, and clock configuration
- Storage component and controller details
- Sensor chip models and bus connections
- GPIO and pin configuration
- Interrupt assignments and routing
- Detailed physical memory map and reserved regions
- Device-specific firmware interfaces and handoff details

Keep these marked unknown until reliable evidence is found.

## 12. Primary references

1. Motorola, [EU Declaration of Conformity — XT2135-2 / MC38C](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf), issued 2021-03-05. Exact model identity and regulatory radio feature list.
2. Qualcomm, [Snapdragon 732G Mobile Platform product brief (PDF)](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf). SoC-level features and optional OEM-dependent capabilities.
3. Qualcomm, [Snapdragon 732G product page](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform). Platform overview.
4. Motorola, [Declarations of Conformity index](https://en-emea.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity). Model mapping for XT2135-2 and related variants.
5. [Motorola Moto G60 user guide mirror](https://manualzz.com/doc/70255715/motorola-moto-g60-smartphone-user-guide). Secondary source; use as a lead, not as the only basis for board-level claims.

## 13. Current assessment

The exact-model Motorola declaration establishes the XT2135-2 identity and several radio capabilities. Qualcomm documents the Snapdragon 732G platform's broad capabilities. Neither source provides the complete motherboard inventory, physical memory map, interrupt configuration, firmware interfaces, or a supported Darwin/XNU boot path.

**Current project status:** hardware and platform research only. No working Moto G60 Darwin/XNU port, device-specific driver support, or loader implementation is claimed.

---
**Document:** `docs/DEVICE_INVENTORY.md`  
**Project:** MotoDarwin18  


14. Community kernel/device-tree evidence — provisional

A public LineageOS kernel tree and Android device configuration for the shared Moto G40 Fusion / Moto G60 family (`hanoip`) provide additional engineering clues. These are not official schematics and do not yet identify the board-revision overlay used by a specific XT2135-2 unit.

Candidate findings from that shared source tree:

- GICv3 and Qualcomm PDC interrupt-controller descriptions.
- Armv8 generic timer listed at 19.2 MHz and a memory-mapped timer block.
- Embedded UFS and SD-card controller paths.
- A Tianma ILI7807S 678-class 1080 × 2460 MIPI-DSI panel description, with 60/120 Hz modes.
- An Ilitek SPI touchscreen node.
- A WCN3990 Bluetooth node and a Qualcomm CLD3 WLAN module in the Android module list; the exact Wi-Fi combo-chip remains unidentified.
- PM6150/PM6150L power-management descriptions and MC50 battery profiles.

The device tree also defines reserved-memory carveouts, but these do not provide a complete physical DRAM map. All candidate findings require exact XT2135-2 board-revision correlation.

Detailed evidence, direct source links, and limitations: [HANOIP_PLATFORM_EVIDENCE.md](../research/soc/HANOIP_PLATFORM_EVIDENCE.md).

Current conclusion remains unchanged: hardware research only; no Darwin/XNU compatibility or working driver is established.


## Evidence reconciliation — 2026-11-08

The [XT2135-2 confirmed platform facts and XNU compatibility review](../research/firmware/XT2135_2_CONFIRMED_PLATFORM_FACTS.md) now separates exact-model Motorola declaration facts, Motorola Android kernel-source provenance, secondary/reported specifications, and shared hanoip-family clues.

In particular, Snapdragon 732G, RAM/storage configurations and consumer hardware specifications should not be presented as facts established by the Motorola XT2135-2 declaration. GICv3/PDC, timer, UFS, panel, touch, WLAN, PMIC, audio and other detailed hardware entries remain shared-family source clues until exact board-revision evidence is available. The physical board revision and DVT1/DVT2 mapping remain unknown.
