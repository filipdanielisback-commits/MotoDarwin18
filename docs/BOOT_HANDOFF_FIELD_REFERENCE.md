# Boot Handoff Field Reference

**Status:** research reference; field meanings are provisional until checked directly against the pinned `xnu-11215.1.10` header and its consumers.

## Purpose and boundary

This document explains the ARM64 boot-argument fields identified during the preliminary review of `pexpert/pexpert/arm64/boot.h`. It separates:
1. the upstream XNU boot ABI;
2. MotoDarwin18's descriptive JSON research manifest; and
3. facts that are actually established for Motorola Moto G60 XT2135-2.

These are not interchangeable. The JSON manifest is **not** a serialized `boot_args` structure and must not be passed to a kernel or loader. This reference does not specify device boot procedures or supply target addresses.

## Source confidence

- **Pinned baseline:** Apple OSS XNU tag `xnu-11215.1.10`, peeled commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`.
- **Review limitation:** the earlier source-browser review was not verified line-by-line against that immutable tag. Therefore exact C declarations, field widths, packing, numeric constants, and semantics must be rechecked in the pinned file before implementation.
- **Target limitation:** no field below has a confirmed XT2135-2 runtime value. Shared hanoip/SDMMAGPIE evidence does not establish a complete XNU boot contract.

Pinned source: [`pexpert/pexpert/arm64/boot.h`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/arm64/boot.h).

## Field reference

The “manifest representation” column describes how the current research manifest treats a concept. It is not a statement about the C ABI type.

| XNU field | Provisional meaning | Manifest representation | XT2135-2 status / research question |
|---|---|---|---|
| `Revision` | Boot-argument structure revision | `boot_handoff.revision` | Unknown. Determine accepted revisions from the pinned header and all relevant consumers. |
| `Version` | Boot-argument structure version | `boot_handoff.version` | Unknown. Determine version semantics and compatibility checks from the pinned source. |
| `virtBase` | Virtual base associated with the kernel's memory layout | `boot_handoff.virt_base` | Unknown. Exact address-space meaning and entry assumptions need source and platform analysis. |
| `physBase` | Physical base associated with the kernel image / memory layout | `boot_handoff.phys_base` | Unknown. Do not infer from Android partition offsets or SoC documentation. |
| `memSize` | Memory-size field | `boot_handoff.mem_size` | Unknown. Exact measurement semantics, exclusions, and relationship to reserved memory need verification. |
| `memSizeActual` | Additional actual-memory-size field | Not currently represented | Unknown. Establish its precise distinction from `memSize` before adding a manifest field. |
| `topOfKernelData` | Upper boundary associated with kernel data | `boot_handoff.top_of_kernel_data` | Unknown. Exact address interpretation and inclusivity/exclusivity need verification. |
| `Video` | Video/display boot metadata | Not currently represented | Unknown. Determine whether the selected configuration requires it and whether a headless research context can omit it. |
| `machineType` | Machine/platform identification value | Not currently represented | Unknown. Determine whether this XNU revision has a viable non-Apple platform-identification model. |
| `deviceTreeP` | Pointer/reference to device-tree data | Abstracted as `device_tree` metadata | Unknown. Pointer address space, alignment, lifetime, and accepted device-tree format require verification. |
| `deviceTreeLength` | Device-tree byte length | `device_tree.length` | Unknown. Manifest field is metadata only; no actual DTB is supplied. |
| `CommandLine` | Boot command-line storage | Not currently represented | Unknown. Determine buffer size, encoding, termination rules, and supported options from pinned source and consumers. |
| `bootFlags` | Bootloader-provided flags | Not currently represented | Unknown. Do not invent bit values; enumerate only flags defined by the pinned revision. |

### Data types and layout

The exact C type, width, signedness, alignment, packing, array size, and nested layout for every field are **not asserted in this document**. They must be transcribed from the pinned header and cross-checked against all code that reads or writes the structure.

In particular:
- Do not assume every address-like field is interchangeable or uses the same address space.
- Do not assume a size field describes all installed RAM or a single contiguous range.
- Do not assume a device-tree pointer is a host-process pointer or a physical address.
- Do not assume command-line storage is an unbounded string.
- Do not treat unknown flag bits as safe to set.

## Current manifest mapping

The current example manifest deliberately keeps these six values unknown:

- `revision`
- `version`
- `phys_base`
- `virt_base`
- `mem_size`
- `top_of_kernel_data`

The device-tree object is marked `unknown`, with null format, length, and digest. Its `length` field is only a descriptive metadata slot, not a device-tree pointer or a generated blob.

Fields not yet represented in the manifest—`memSizeActual`, `Video`, `machineType`, `CommandLine`, and `bootFlags`—should remain out until their exact semantics and safe descriptive representation are established. Do not fill gaps with guessed defaults.

## Verification checklist before changing the schema

- [ ] Read the exact pinned `boot.h` at commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`.
- [ ] Record exact C declarations, nested structures, constants, and compile-time guards.
- [ ] Find every relevant reader/writer of each field in the same source baseline.
- [ ] Identify which fields are required, optional, conditional, or reserved.
- [ ] Establish address-space semantics and overflow-safe range interpretation.
- [ ] Establish device-tree format, alignment, maximum length, and lifetime requirements.
- [ ] Establish command-line buffer constraints and known flag definitions.
- [ ] Add manifest fields only when the representation is unambiguous and tests cover malformed input.
- [ ] Keep target-specific values unknown until supported by exact-model evidence.

## Related project documents

- [ARM64 boot header source review](../xnu/source-reviews/ARM64_BOOT_HEADER_REVIEW.md)
- [ARM startup source review](../xnu/source-reviews/ARM_INIT_REVIEW.md)
- [Platform initialization source review](../xnu/source-reviews/PE_INIT_REVIEW.md)
- [Boot handoff manifest validator](../boot-handoff/README.md)
- [XNU baseline](XNU_BASELINE.md)
- [XT2135-2 identity research](../research/soc/XT2135_2_IDENTITY.md)

## Current conclusion

We have a useful field inventory, but not yet a verified ABI transcription. The next technical research task is pinned-source verification and cross-reference tracing—not populating boot values or attempting a device handoff.
