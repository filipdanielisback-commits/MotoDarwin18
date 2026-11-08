# Research references

This list prioritizes primary sources. A link is a starting point for research, not proof that a particular component works on Moto G60 XT2135-2.

## Device documentation

- Motorola, [EU Declaration of Conformity — XT2135-2 / MC38C (PDF)](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf), issued 2021-03-05. Identifies the market model as moto g60 XT2135-2 and lists regulatory radio capabilities.
- Motorola, [Declarations of Conformity index](https://en-emea.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity). Maps XT2135-2 to the Moto G60 Vision / MC38C type.
- Motorola Moto G60 Smartphone User Guide. [Manualzz mirror](https://manualzz.com/doc/70255715/motorola-moto-g60-smartphone-user-guide). Secondary source; prefer an official Motorola-hosted copy when available.

## Qualcomm platform documentation

- Qualcomm, [Snapdragon 732G Mobile Platform](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform).
- Qualcomm, [Snapdragon 732G Mobile Platform product brief (PDF)](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf). Manufacturer-documented SoC features; optional features may depend on OEM/carrier selection.
- Qualcomm, [Snapdragon 732G announcement](https://www.qualcomm.com/news/releases/2020/08/qualcomm-announces-snapdragon-732g-improve-high-tier-mobile-gaming).

## Hanoip / SDMMAGPIE engineering references

These are community-maintained Android/Linux engineering sources for the shared Moto G40 Fusion / Moto G60 (`hanoip`) family. They are not official Motorola schematics and must be checked against the exact target board revision.

- [hanoip Android device tree](https://github.com/motorola-sm6150-devs/device_motorola_hanoip), including [BoardConfig.mk](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/BoardConfig.mk) and [modules.load](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/modules.load).
- [LineageOS Motorola SM6150 kernel source](https://github.com/LineageOS/android_kernel_motorola_sm6150/tree/lineage-20).
- [SDMMAGPIE SoC device tree](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi).
- [Motorola SDMMAGPIE base device tree](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-moto-base.dtsi).
- [Hanoi base device tree](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-base.dts).
- [Hanoip common overlay](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi).
- [Hanoi panel description](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/hanoi-panel.dtsi).
- [Hanoi touchscreen description](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-touchscreen.dtsi).
- [Hanoi battery and thermal overlay](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/hanoi_battery_thermal_overlay.dtsi).
- [Hanoip DVT1 overlay](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt1-overlay.dts) and [DVT2 overlay](https://github.com/LineageOS/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt2-overlay.dts).

## Darwin / XNU background

- Apple, [XNU source code](https://github.com/apple-oss-distributions/xnu). This is the open-source kernel source; it is not the source code for all proprietary iOS components.
- Apple Open Source, [Open Source releases](https://opensource.apple.com/). Use release-specific source archives and licenses when documenting a component.

## Related project research

- HakiOS project materials should be consulted directly for its supported devices, implementation status, and licensing. Do not assume that support for another Snapdragon device implies support for Moto G60.
- Any third-party project or binary referenced here must be reviewed for its license, provenance, target hardware, and redistribution terms before reuse.

## Citation practice

For every technical claim added to the repository:
1. Link the original source, not just a search result or copied summary.
2. Record the document title and relevant version/date where possible.
3. Separate vendor-documented platform capabilities from the exact phone's implementation.
4. Mark uncertain or inferred claims explicitly.
5. Do not upload proprietary firmware, restore images, keys, or other material unless redistribution rights are clear.
