# Source Review: `pexpert/pexpert/arm64/boot.h`

**Status:** provisional structure review; exact comparison with `xnu-11215.1.10` remains pending.

## Role

This header defines the ARM64 boot argument structure passed into the Mach kernel. It is part of the ABI between the preceding boot environment and XNU. It is not interchangeable with a Linux boot protocol or an arbitrary flattened device tree.

## Observed structure fields

The accessible upstream definition contains these fields:

| Field | Meaning | MotoDarwin18 question |
|---|---|---|
| `Revision` | Structure revision | Which exact revision does the selected XNU require? |
| `Version` | Structure version | Which fields and semantics are valid for that version? |
| `virtBase` | Virtual base of memory | What address-space assumptions are active at entry? |
| `physBase` | Physical base of memory | What physical range does the kernel image occupy? |
| `memSize` | Memory size | What does this measure, and which regions are excluded? |
| `topOfKernelData` | Highest physical address used by kernel data | How is the boundary computed and validated? |
| `Video` | Boot video metadata | Can be absent or unused for an initial headless research target? |
| `machineType` | Machine type | Is there a supported, non-Apple platform identification path? |
| `deviceTreeP` | Flattened device-tree pointer | Which format, alignment, address space, and lifetime are required? |
| `deviceTreeLength` | Device-tree byte length | How is the blob bounded and validated? |
| `CommandLine` | Boot command-line buffer | Which options are consumed by this XNU configuration? |
| `bootFlags` | Bootloader-provided flags | Which bits are defined by the pinned revision? |
| `memSizeActual` | Actual memory size | How does it differ from `memSize` in this version? |

The source also defines video bit-field constants and boot-argument revision/version constants. Exact numeric values and packing must be read from the pinned header before any implementation is attempted.

## ABI requirements

A future handoff design must validate:

- exact structure layout, field widths, alignment, and packing;
- revision and version compatibility;
- address width and physical/virtual address interpretation;
- overflow-safe ranges for kernel image and memory boundaries;
- device-tree pointer alignment, length, format, and lifetime;
- command-line termination and maximum length;
- reserved and unknown flag handling;
- memory ownership and reserved-region exclusions.

The schema must not invent values for any of these fields. Unknown data remains unknown, rather than being replaced with plausible-looking constants.

## Why Android's device tree is not automatically enough

The Moto G60 family source tree gives useful evidence about hardware description, but it does not establish the full boot handoff expected by this XNU revision. A DTB alone is not the entire contract: the boot arguments, memory ownership, address translations, CPU entry state, and other startup assumptions also matter.

## MotoDarwin18 next step

Build a host-side parser/validator for a *documented abstract handoff manifest*, not a binary structure intended for a phone. Unit tests should cover malformed values, integer overflow, invalid lengths, unaligned ranges, overlapping regions, and unknown required fields.

No loader or phone boot procedure is proposed by this review.

## References

- [Pinned XNU path: ARM64 boot.h](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/arm64/boot.h)
- [Accessible upstream ARM64 boot header](https://github.com/apple/darwin-xnu/blob/main/pexpert/pexpert/arm64/boot.h)
- [ARM startup review](ARM_INIT_REVIEW.md)
