# XT2135-2 Identity and Hanoip Mapping

**Target identifier:** XT2135-2  
**Research date:** 2026-11-08  
**Status:** Exact commercial/regulatory model identity verified; exact board-revision overlay mapping remains unresolved.

## Why this distinction matters

The XT2135-2 suffix must not be silently treated as interchangeable with every device marketed simply as Moto G60. Motorola's own declaration distinguishes XT2135-2 from XT2135-1.

## Manufacturer evidence

Motorola's support page for declarations of conformity lists:

| Model identifier | Type name | Product name in declaration |
|---|---|---|
| XT2135-2 | MC38C | moto g60 vision |
| XT2135-1 | MC38B | moto g60 |

Source: [Motorola — Declarations of Conformity](https://fr-fr.support.motorola.com/app/answers/detail/a_id/167829)

This is the strongest source in this note for the regulatory identity of the target. The repository should continue to use XT2135-2 as its exact target identifier. The product-name wording is included to avoid confusing it with XT2135-1.

## Shared Android/Linux source evidence

The public community device tree describes itself as the Android device tree for the shared Motorola Moto G40 Fusion / Moto G60 family, codename `hanoip`:

- [hanoip device tree](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [board-info.txt](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/board-info.txt)
- [BoardConfig.mk](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/BoardConfig.mk)
- [LineageOS shared Motorola SM6150 device configuration](https://github.com/LineageOS/android_device_motorola_sm6150-common/blob/lineage-20/README.md)

The inspected files state:

- `board-info.txt` requires `board=hanoip`.
- `BoardConfig.mk` sets `TARGET_OTA_ASSERT_DEVICE := hanoip`.
- The same configuration uses `sm6150` as an Android build-platform label and points to the Motorola SM6150 kernel source.
- The shared configuration lists Moto G60 as a supported member of the SM6150 device family.

These facts support using `hanoip` as a relevant family-level research source. They do **not** prove that every XT2135-2 retail unit uses every DVT overlay in that tree, nor do they identify the exact board revision of a particular phone.

## Current conclusion

| Question | Conclusion |
|---|---|
| Is XT2135-2 a distinct identifier from XT2135-1? | Yes; Motorola lists them separately. |
| What product name does Motorola's declaration associate with XT2135-2? | moto g60 vision. |
| Is `hanoip` relevant to Moto G60-family research? | Yes; community device-tree documentation explicitly covers Moto G40 Fusion / Moto G60. |
| Does `hanoip` prove the exact XT2135-2 board revision? | No. |
| Can we select DVT1 or DVT2 for XT2135-2 from the evidence above? | No; mapping remains open. |

## Open evidence needed

1. An authoritative Motorola source linking XT2135-2 / MC38C to a specific hardware revision or board identifier.
2. A source-backed explanation of how the `hanoip` device tree selects among its DVT overlays.
3. Independent evidence that the selected overlay corresponds to XT2135-2, rather than merely to another member of the shared device family.

Until these are found, keep the DVT overlay mapping marked **Unknown**. Do not infer it from the model suffix, product name, or shared device-tree codename.

## Impact on Darwin/XNU work

This identity check narrows the target naming but does not remove the platform bring-up blockers. XNU work must not hard-code a DVT-specific memory map, interrupt routing, panel, PMIC, or peripheral assumption until the relevant XT2135-2 hardware mapping is supported by evidence.
