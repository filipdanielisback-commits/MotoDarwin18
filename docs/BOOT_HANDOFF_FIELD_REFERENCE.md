# Boot Handoff Field Reference

**Status:** source-verified for the declarations and consumer paths listed below, against the pinned Apple OSS XNU baseline. Target-specific values remain unknown.

## Purpose and boundary

This reference separates:
1. the upstream XNU boot ABI;
2. MotoDarwin18's descriptive JSON research manifest; and
3. facts established for Motorola Moto G60 XT2135-2.

These are not interchangeable. The JSON manifest is **not** a serialized `boot_args` structure and must not be passed to a kernel or loader. This document does not provide target addresses or a device boot procedure.

## Source baseline and confidence

- **Pinned tag:** `xnu-11215.1.10`
- **Peeled commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`
- **Verified declaration:** `pexpert/pexpert/arm64/boot.h`
- **Verified consumers:** `osfmk/arm/arm_init.c`, `pexpert/arm/pe_init.c`, `osfmk/arm64/arm_vm_init.c`, and `bsd/kern/bsd_init.c`

See [PINNED_SOURCE_VERIFICATION.md](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md) for file blob hashes and the detailed trace.

## Exact field declaration reference

| Field | Pinned ARM64 declaration | Source-verified meaning / use | XT2135-2 status |
|---|---|---|---|
| `Revision` | `uint16_t` | Boot-argument structure revision. Revision 2 adds `bootFlags`; BSD darkboot consumer checks revision before reading that field. | Unknown |
| `Version` | `uint16_t` | Boot-argument structure version; constants for versions 1 and 2 are declared. Full version-consumer audit remains open. | Unknown |
| `virtBase` | `uint64_t` | Virtual base used by ARM64 VM initialization and in the boot CPU data physical-address calculation. | Unknown |
| `physBase` | `uint64_t` | Physical base used by ARM64 VM initialization and in the boot CPU data physical-address calculation. | Unknown |
| `memSize` | `uint64_t` | Physical-memory size input; ARM startup uses it in page-size policy and VM initialization derives managed size from it. | Unknown |
| `memSizeActual` | `uint64_t` | If nonzero, supplies the VM path's `mem_actual`; otherwise the path falls back to rounded `mem_size`. | Unknown |
| `topOfKernelData` | `uint64_t` | Used in ARM64 physmap calculations and as the initial available-memory boundary. Exact target value and ownership boundary are unknown. | Unknown |
| `Video` | `Boot_Video` | Nested structure with six `unsigned long` members; Platform Expert copies its fields into video state. On ARM64 LP64, `unsigned long` is 64-bit. | Unknown |
| `machineType` | `uint32_t` | Machine-type field; the boot-argument pointer is passed to `pe_identify_machine`. No supported Motorola value established. | Unknown |
| `deviceTreeP` | `void *` | Pointer to flattened device tree; Platform Expert captures it and initializes SecureDT using it with `deviceTreeLength`. | Unknown |
| `deviceTreeLength` | `uint32_t` | Byte length paired with `deviceTreeP` for SecureDT initialization. | Unknown |
| `CommandLine` | `char[1024]` | Fixed-size command-line buffer; full producer/parser contract not yet traced. | Unknown |
| `bootFlags` | `uint64_t` | Additional bootloader flags. Header defines darkboot as bit 0; the consumer reads it only when `Revision >= 2`. | Unknown |

The header defines `BOOT_LINE_LENGTH` as 1024, revisions 1 and 2, and versions 1 and 2. The `Boot_Video` members are `v_baseAddr`, `v_display`, `v_rowBytes`, `v_width`, `v_height`, and `v_depth`. The header also defines bit shifts/mask values used to decode depth, rotation and scale from `v_depth`.

These are source-level declarations and use sites. They do not establish target values, the complete producer-side ABI, or compatibility with Motorola firmware.

## Manifest mapping

The current example manifest deliberately leaves these six values null:

- `revision`
- `version`
- `phys_base`
- `virt_base`
- `mem_size`
- `top_of_kernel_data`

The device-tree object remains `unknown`, with null format, length and digest. Its `length` is descriptive metadata only; it is not a device-tree pointer or a generated blob.

The current schema does not represent `memSizeActual`, `Video`, `machineType`, `CommandLine`, or `bootFlags`. Do not add guessed values. A schema change should follow a separate review of the field's producer/consumer contract and a corresponding test update.

## ABI cautions

- Do not treat physical and virtual addresses as interchangeable.
- Do not assume `memSize` is the amount of user-visible RAM or a single contiguous range.
- Do not assume `memSizeActual` and `memSize` are synonyms; the pinned VM code treats them differently.
- Do not assume the device-tree pointer is a host-process pointer or that an Android DTB is automatically accepted.
- Do not assume command-line storage is unbounded; the header fixes its size.
- Do not set unknown boot flag bits or infer a machine type.
- Do not calculate a binary structure layout from this summary; use the exact header and matching target ABI/compiler configuration.

## Remaining verification checklist

- [x] Read the exact pinned ARM64 `boot.h` declaration.
- [x] Record field C types, nested video members, buffer size and declared constants.
- [x] Trace key uses in ARM startup, Platform Expert initialization, ARM64 VM setup and the revision-gated darkboot consumer.
- [ ] Trace the full version compatibility contract and every conditional consumer.
- [ ] Establish producer-side rules for address spaces, alignment, lifetime and memory ownership.
- [ ] Establish whether any of the Apple-specific platform assumptions can be satisfied by a non-Apple platform.
- [ ] Keep target-specific values unknown until supported by exact-model evidence.

## Related documents

- [Pinned XNU source verification](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md)
- [ARM64 boot header review](../xnu/source-reviews/ARM64_BOOT_HEADER_REVIEW.md)
- [ARM startup review](../xnu/source-reviews/ARM_INIT_REVIEW.md)
- [Platform initialization review](../xnu/source-reviews/PE_INIT_REVIEW.md)
- [Boot handoff manifest validator](../boot-handoff/README.md)
- [XNU baseline](XNU_BASELINE.md)
- [XT2135-2 identity research](../research/soc/XT2135_2_IDENTITY.md)

## Conclusion

The selected boot-argument declarations and several important consumers are now verified against the pinned source tag. This is a meaningful improvement over the earlier provisional review, but it is not a complete boot ABI specification and does not demonstrate that MotoDarwin18 can boot on the target handset.
