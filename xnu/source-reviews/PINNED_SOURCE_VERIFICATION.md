# Pinned XNU Source Verification

**Baseline:** Apple OSS XNU tag `xnu-11215.1.10`  
**Peeled commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`  
**Review status:** selected boot ABI declarations and consumer paths verified against files fetched at the pinned tag. This is a source review, not a build or platform-compatibility result.

## Files checked at the pinned tag

| Source path | Verified file blob SHA | Review result |
|---|---|---|
| `pexpert/pexpert/arm64/boot.h` | `eab75014f92bb6475bdd4225b6e074ad82652ae5` | Exact ARM64 `boot_args` declarations, nested video structure, constants and buffer size checked |
| `osfmk/arm/arm_init.c` | `f96a24595c2abd134f7af2526b88808514d61252` | Boot CPU entry, early Platform Expert call, memory-size use and physical/virtual base relation checked |
| `pexpert/arm/pe_init.c` | `6a3fce5aa2c496481915ec2511379b0d6935a413` | Boot-argument capture, device-tree initialization, video-field copying and later interrupt/debug initialization checked |
| `pexpert/pexpert/pexpert.h` | `fbde4d4b984c937423ed69455d2f5b1c619ce525` | `PE_init_platform(boolean_t, void *)` declaration and Platform Expert API surface checked |
| `osfmk/arm64/arm_vm_init.c` | `0dbbd9103f131faab9e6c1ccbea3c0fa9ae46e5c` | Use of virtual/physical bases, memory sizes and `topOfKernelData` checked |
| `bsd/kern/bsd_init.c` | `7e0623ac04a7c807c0a693381186ddd770ff7ea6` | Revision-gated darkboot flag consumer checked |

The blob hashes identify the file contents returned for the named tag. The repository's immutable peeled commit is recorded above. No Apple source file is copied into MotoDarwin18; this document records findings and provenance only.

## Exact ARM64 boot argument declaration

The pinned ARM64 header declares these fields, in order:

| Field | Pinned declaration | What the declaration establishes |
|---|---|---|
| `Revision` | `uint16_t` | 16-bit unsigned revision field |
| `Version` | `uint16_t` | 16-bit unsigned version field |
| `virtBase` | `uint64_t` | 64-bit unsigned virtual-base field |
| `physBase` | `uint64_t` | 64-bit unsigned physical-base field |
| `memSize` | `uint64_t` | 64-bit unsigned memory-size field |
| `topOfKernelData` | `uint64_t` | 64-bit unsigned highest-physical-address boundary described by the header comment |
| `Video` | `Boot_Video` | Nested video metadata structure |
| `machineType` | `uint32_t` | 32-bit unsigned machine-type field |
| `deviceTreeP` | `void *` | Pointer to the flattened device tree; 64-bit pointer in this ARM64 ABI |
| `deviceTreeLength` | `uint32_t` | 32-bit unsigned device-tree length |
| `CommandLine` | `char[BOOT_LINE_LENGTH]` | Fixed-size character array |
| `bootFlags` | `uint64_t` | 64-bit unsigned bootloader flags |
| `memSizeActual` | `uint64_t` | 64-bit unsigned actual-memory-size field |

The header defines `BOOT_LINE_LENGTH` as **1024**.

The nested `Boot_Video` structure contains six `unsigned long` members: `v_baseAddr`, `v_display`, `v_rowBytes`, `v_width`, `v_height`, and `v_depth`. On the ARM64 LP64 target these are 64-bit C `unsigned long` values. The header also defines depth/rotation/scale bit shifts and a depth mask.

The header defines:
- `kBootArgsRevision` = 1
- `kBootArgsRevision2` = 2, with a comment that revision 2 added `boot_args.bootFlags`
- `kBootArgsVersion1` = 1
- `kBootArgsVersion2` = 2
- `kBootFlagsDarkBoot` = bit 0

These declarations establish the source-level field types and constants. They do **not** establish the correct values for a Motorola device, all structure offsets for every compiler configuration, or a complete boot protocol for a non-Apple platform.

## Consumer trace findings

### ARM startup: `osfmk/arm/arm_init.c`

The boot CPU entry copies the incoming structure into `const_boot_args`, redirects `args` to that copy, and calls `PE_init_platform(FALSE, args)` early in startup.

The function reads `args->memSize` when selecting an advertised kernel page-size policy. It also computes the physical address corresponding to the boot CPU data using `physBase`, the virtual address of that data, and `virtBase`. Later in startup, `PE_init_platform(TRUE, &BootCpuData)` is called in the boot CPU path; this is a distinct later call and must not be confused with the early call that passes `boot_args`.

### Platform Expert: `pexpert/arm/pe_init.c`

On its first initialization, `PE_init_platform` stores the incoming boot-argument pointer in `PE_state.bootArgs`, copies `deviceTreeP` and `deviceTreeLength` into Platform Expert state, and copies the video metadata fields into `PE_state.video`.

On the early (`vm_initialized == FALSE`) path it initializes Secure Device Tree access from the captured pointer and length, then calls `pe_identify_machine(boot_args_ptr)`. It subsequently reads several properties from the device tree. On the later path it calls `pe_arm_init_interrupts(args)` and `pe_arm_init_debug(args)`.

This confirms that the device-tree pointer and length are consumed together by the platform initialization path. It does not establish that an Android DTB from the target handset is directly acceptable to this XNU baseline.

### Virtual memory: `osfmk/arm64/arm_vm_init.c`

The VM initialization path assigns `args->virtBase` and `args->physBase` to the kernel's global virtual and physical base values.

It uses `args->memSize` to establish the managed physical-memory size, rounds the size to a software page boundary, and derives `mem_actual` from `memSizeActual` when that field is nonzero; otherwise it falls back to the rounded `mem_size`. The source comments describe the internal `mem_actual` quantity as the highest physical address plus one.

The same path uses `topOfKernelData` in physical-to-virtual mapping calculations and initializes `first_avail` / `avail_start` from it. Thus this field is not merely a generic “kernel image end” label: its exact boundary semantics matter to memory mapping and allocator initialization.

### Revision-gated flag: `bsd/kern/bsd_init.c`

When darkboot support is compiled in, the consumer checks that the boot-argument pointer is non-null and that `Revision >= kBootArgsRevision2` before reading `bootFlags`. It tests `kBootFlagsDarkBoot` and otherwise treats darkboot as disabled.

This is direct evidence that the revision field gates access to the added flag. It is not a reason to set that flag in a third-party platform handoff.

## Fields whose consumers remain only partially traced

- **`Version`:** declaration and version constants are verified; a complete audit of all version-dependent readers/writers has not been performed.
- **`machineType`:** declaration is verified and the complete boot-argument pointer is passed to `pe_identify_machine`; this review has not established a supported Motorola machine-type value or a complete mapping of that function's behavior.
- **`CommandLine`:** fixed-size storage declaration is verified; its full parsing and producer/consumer contract has not been audited in this pass.
- **`Video`:** the nested layout and Platform Expert copy are verified; no conclusion is made that target display metadata is available or required for an initial research configuration.
- **All pointer and address fields:** C types are verified, but physical-vs-virtual address rules, mapping lifetime, cacheability, alignment and ownership must be derived from the complete startup contract, not guessed from field names.

## Implications for MotoDarwin18

1. Update documentation to distinguish source-verified field declarations from unknown target values.
2. Keep all XT2135-2 runtime addresses, sizes, device-tree metadata and machine identifiers unknown until exact-model evidence exists.
3. Do not derive boot values from Android partition offsets, shared-family device trees, SoC marketing material or a guessed memory map.
4. Keep the JSON manifest descriptive. It is not a binary `boot_args` structure and is not a loader input.
5. Treat a passing manifest validator or CI run as a documentation/software-quality result only, not evidence of ABI implementation or device compatibility.

## Remaining verification work

- Trace the full version compatibility contract and all conditional structure consumers.
- Trace the producer-side contract for every field, including pointer address spaces and object lifetimes.
- Audit the exact target-independent platform assumptions that remain Apple-specific.
- Record target-specific evidence separately, without promoting family-level evidence to exact-model confirmation.

## References

All links are pinned to the selected tag:

- [ARM64 boot header](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/arm64/boot.h)
- [ARM startup](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)
- [ARM Platform Expert initialization](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_init.c)
- [Platform Expert declarations](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/pexpert.h)
- [ARM64 VM initialization](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm64/arm_vm_init.c)
- [BSD initialization](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/bsd/kern/bsd_init.c)
- [MotoDarwin18 XNU baseline](../../docs/XNU_BASELINE.md)

*Project: MotoDarwin18*
