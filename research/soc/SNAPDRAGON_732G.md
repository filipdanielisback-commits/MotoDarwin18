# Qualcomm Snapdragon 732G — Research Note

**Target handset:** Motorola Moto G60 XT2135-2  
**SoC part number:** SM7150-AC  
**Status:** Platform-level overview; not a board inventory  
**Last reviewed:** 2026-11-08

## 1. Purpose

Collect manufacturer-documented Snapdragon 732G platform facts relevant to later compatibility research. Keep these separate from the exact Moto G60 XT2135-2 implementation.

The Qualcomm product brief is a platform capability document. It is not a full programming manual, board schematic, firmware interface specification, or confirmation that every optional feature is implemented by Motorola.

## 2. Primary source

- Qualcomm, [Snapdragon 732G Mobile Platform product brief (PDF)](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf).
- Qualcomm, [Snapdragon 732G product page](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform).
- Motorola, [EU Declaration of Conformity — XT2135-2 / MC38C](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf).

The Motorola declaration is the model-specific source for the handset's identity and selected radio features. The Qualcomm brief is the source for SoC-level capabilities.

## 3. Manufacturer-documented platform components

Qualcomm's brief identifies the following platform components and capabilities:

| Area | Qualcomm-documented platform information | Important limitation |
|---|---|---|
| CPU | Kryo 470, octa-core, 64-bit, up to 2.3 GHz | Does not provide the XT2135-2 board's full CPU/firmware description |
| GPU | Adreno 618; Vulkan 1.1 and other graphics APIs listed | Does not establish a Darwin graphics driver |
| AI/DSP | Hexagon 688, vector and tensor acceleration | Does not establish availability to a hypothetical XNU environment |
| Modem | Snapdragon X15 LTE; advertised peak rates and LTE categories | Actual radio bands and enablement depend on handset and carrier |
| Wi-Fi | FastConnect 6200; Wi-Fi 6-ready platform capabilities | Motorola's XT2135-2 declaration lists 802.11a/b/g/n/ac |
| Bluetooth | Platform brief lists Bluetooth 5.1 | Motorola's XT2135-2 declaration lists Bluetooth 5.0 |
| Camera/ISP | Spectra 350, CV-ISP, dual 14-bit ISP features | Does not identify the actual camera sensors or enabled modes |
| Audio | Aqstic codec support up to WCD9341 and amplifier support up to WSA8815 | Does not prove those exact components are fitted |
| Memory | LPDDR4/4X, 2 × 16-bit interface, up to 1866 MHz and 8 GB | Does not establish the installed RAM configuration or physical map |
| Display | Maximum on-device display support listed as QHD+ | Does not identify the handset panel/controller |
| Location | GPS, GLONASS, BeiDou, Galileo, QZSS, SBAS listed | Exact handset configuration may differ |
| USB/display | DisplayPort over USB Type-C support listed | Does not prove the phone exposes DisplayPort |
| Security | Secure Boot, Qualcomm TEE and other security capabilities listed | Not a public description of this handset's complete trust chain |

Qualcomm notes that certain optional features are subject to carrier and OEM selection. This is a key reason not to treat the platform brief as a handset bill of materials.

## 4. Exact-handset comparison

Motorola's EU Declaration of Conformity names the market model as **moto g60, XT2135-2**, type name **MC38C**. Its radio description includes IEEE 802.11a/b/g/n/ac and Bluetooth 5.0, plus GPS, GLONASS, Galileo, FM receive, and NFC.

This produces two useful examples of evidence hierarchy:

1. Qualcomm lists Wi-Fi 6-ready capability for the platform, while Motorola's exact-model declaration lists 802.11ac for the handset.
2. Qualcomm lists Bluetooth 5.1 for the platform, while Motorola's exact-model declaration lists Bluetooth 5.0 for the handset.

For claims about XT2135-2, prefer the exact-model Motorola declaration over a maximum SoC capability. The declaration does not identify the combo-chip, antenna design, firmware, or all software interfaces.

## 5. Relevance to Darwin/XNU research

The SoC name and 64-bit CPU capability are only an initial filter. A credible platform assessment still needs evidence for:

- Exact CPU topology and platform initialization assumptions.
- Firmware handoff and hardware-description interfaces.
- Physical memory map, reserved regions, and memory attributes.
- Interrupt controller implementation, routing, and timer interfaces.
- Storage, USB, display, touch, audio, and peripheral controllers.
- Power, clock, reset, and thermal-management dependencies.
- Device-specific firmware and vendor services.

This note does not establish that XNU supports the Moto G60, that a suitable loader interface exists, or that the listed peripherals can be initialized by open-source drivers.

## 6. Open questions

- What exact board revision and component population correspond to the target unit?
- What authoritative public sources describe its firmware and hardware handoff?
- What is the exact physical memory layout?
- Which interrupt controller and timer configuration are used?
- Which storage, display, touch, audio, wireless, and power-management components are fitted?
- Which required interfaces are documented, and which depend on proprietary vendor software or firmware?

See [DEVICE_UNKNOWNS.md](../../docs/DEVICE_UNKNOWNS.md) and [SOC_PLATFORM_REQUIREMENTS.md](../../docs/SOC_PLATFORM_REQUIREMENTS.md).

## 7. Evidence policy

For each new claim, record:
- Source title and direct URL.
- Publisher and document date/version.
- Whether the source describes the SoC, exact handset, or a related model.
- The specific claim supported.
- Confidence and known limitations.

Do not copy platform maximums into the handset inventory as if they were confirmed phone specifications. Do not infer support for one Snapdragon device from another device's project.

**Conclusion:** Snapdragon 732G manufacturer documentation provides a useful SoC capability baseline. The exact XT2135-2 declaration provides a small but valuable set of handset-specific facts. Board-level integration and operating-system compatibility remain open research questions.

*Project: MotoDarwin18*
