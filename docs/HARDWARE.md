# Moto G60 XT2135-2 hardware inventory

This document records hardware facts relevant to MotoDarwin18. It is a research inventory, not a claim that Darwin/XNU currently supports this phone.

## Evidence labels

- **Documented** — stated by a manufacturer or platform-vendor source.
- **Reported** — stated by a device guide or secondary source; confirm against the exact regional variant.
- **Unverified** — needs confirmation from reliable device-specific documentation or non-destructive observation.
- **Unknown** — not yet established.

## Device identity

| Item | Current record | Status |
|---|---|---|
| Device family | Motorola Moto G60 | Reported |
| Model identifier | XT2135-2 | Reported in the Moto G60 user guide |
| SoC | Qualcomm Snapdragon 732G | Reported in the user guide; confirm for this exact unit |
| SoC platform capabilities | Kryo 470 CPU, Adreno 618 GPU, Hexagon 688, FastConnect 6200 family | Documented by Qualcomm for Snapdragon 732G; this does not prove every optional feature is enabled in this phone |

## SoC platform reference

Qualcomm's Snapdragon 732G product brief lists, among other platform-level capabilities:

- 64-bit Kryo 470 CPU, up to 2.3 GHz
- Adreno 618 graphics
- Hexagon 688 processor
- Snapdragon X15 LTE modem
- FastConnect 6200 connectivity subsystem
- LPDDR4/4X memory support

These are **platform capabilities**, not a complete bill of materials for the Moto G60. OEM configuration, board design, firmware, and component substitutions can change what is present or enabled.

## Device-specific details still to verify

| Area | Research question | Status |
|---|---|---|
| RAM configuration | Exact RAM capacity and memory layout for XT2135-2 | Unverified |
| Storage | Flash type, controller, partition layout | Unknown |
| Display | Panel identifier, resolution, refresh modes, interface | Reported resolution; panel/interface unknown |
| GPU | Exact kernel driver and firmware combination | Unknown |
| Wi-Fi / Bluetooth | Exact chip integration, firmware and kernel interfaces | Unknown |
| Cellular | Modem integration and vendor interface details | Unknown |
| Audio | Codec, amplifiers, routing and DSP configuration | Unknown |
| Cameras | Sensor models, ISP path and camera firmware | Unknown |
| Sensors | Exact sensor inventory and buses | Unknown |
| Power | PMIC, charging controller, battery telemetry interfaces | Unknown |
| Boot and security | Boot chain, verified-boot configuration and device-specific trust chain | Unknown |

## Why this matters to Darwin/XNU research

A SoC feature list is not a driver inventory. A compatible platform requires a supported path for early boot, interrupt handling, timers, memory management, storage, display, input, power, and other hardware services. Vendor Android drivers and firmware are not automatically reusable by XNU.

For each component, future notes should identify:
1. The exact hardware component or controller.
2. The evidence and source.
3. Whether the information is device-specific or only SoC-family-level.
4. The relevant interface or subsystem.
5. What remains unknown.

## Sources

1. Motorola Moto G60 Smartphone User Guide, product ID lists Moto G60 model XT21351 / XT2135-2. A copy is available at [Manualzz](https://manualzz.com/doc/70255715/motorola-moto-g60-smartphone-user-guide). Treat this as a mirrored copy; locate an official Motorola-hosted copy before relying on it for critical details.
2. Qualcomm, [Snapdragon 732G Mobile Platform](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform).
3. Qualcomm, [Snapdragon 732G product brief (PDF)](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf).

## Update policy

Do not promote an item from Unverified to Documented without recording a source. Do not infer device-specific hardware solely from a chipset marketing page.
