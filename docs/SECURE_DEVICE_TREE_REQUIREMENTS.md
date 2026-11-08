# Secure Device Tree Requirements Analysis

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2  
**XNU baseline:** `xnu-11215.1.10`  
**Pinned commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`  
**Status:** Source-derived format and consumer analysis; target handoff format remains unknown.

## 1. Executive finding

The pinned XNU source does not simply accept an arbitrary Linux Device Tree Blob (DTB) because both are called a “flattened device tree”. Its `SecureDT` implementation walks an Apple XNU-specific in-memory node/property representation declared in `pexpert/pexpert/device_tree.h`.

The standard Devicetree Specification FDT encoding instead has an FDT header followed by a memory-reservation block, a tokenized structure block, and a strings block. These are distinct binary layouts. A normal Linux FDT must therefore **not be assumed directly compatible** with the pinned XNU `SecureDT` parser. Compatibility would require producer-side evidence or a separately designed and verified format-conversion layer; this document does not design or implement one.

The XNU consumer also expects platform-specific node names and properties. Most importantly, the reviewed ARM64 startup path reads `/chosen/dram-base` and `/chosen/dram-size`, and treats their absence as fatal. Moto G60 family Linux DTS evidence does not establish that an XT2135-2 firmware handoff contains this Apple-style tree or these properties.

**Conclusion:** SecureDT compatibility is a major unresolved boot-contract gap, not a matter of copying the existing Linux DTS into a kernel handoff.

## 2. Pinned source evidence

The following files were fetched from Apple XNU tag `xnu-11215.1.10`:

| File | Blob SHA | What it establishes |
|---|---|---|
| `pexpert/pexpert/device_tree.h` | `b35d4d15c21404c00b52ba6691ab13e7c989c3eb` | Apple node/property structures and public SecureDT interfaces |
| `pexpert/gen/device_tree.c` | `4eff3236bbd938266c8134d737b46b63516adbbe` | Initialization, traversal, property lookup and bounds checks |
| `pexpert/arm/pe_init.c` | `6a3fce5aa2c496481915ec2511379b0d6935a413` | Early tree initialization and metadata consumers |
| `pexpert/arm/pe_identify_machine.c` | `937ce42df60f44eccb8885281d8e8ee621b2910f` | CPU, SoC base, interrupt-controller and timer consumers |
| `osfmk/arm/arm_init.c` | `f96a24595c2abd134f7af2526b88808514d61252` | Early `/chosen` lookups and mandatory DRAM properties |

The source is analyzed, not copied into MotoDarwin18. The source file-level license notices and the XNU repository's APSL terms remain applicable to any future source reuse.

## 3. What SecureDT expects in memory

### 3.1 Node and property representation

The pinned `device_tree.h` defines:

- A node header with two 32-bit counters: `nProperties` and `nChildren`.
- A property header with a fixed 32-byte, NUL-terminated property name and a 32-bit byte length.
- The property value immediately follows its property header.
- The parser advances to the next property on a four-byte boundary.
- Child nodes follow the node's property sequence and are traversed recursively.

The `DTEntry` type is an opaque pointer to a node. Property lookup returns a pointer into the original tree plus the property's byte length; the caller interprets the returned bytes according to the property's expected type.

This is not the standard FDT header/token/strings-block encoding defined by the Devicetree Specification. Similar logical concepts—nodes, properties and children—do not make the binary representations interchangeable.

### 3.2 Initialization and validation boundary

In the reviewed source, `SecureDTInit(base, size)`:

1. Checks for integer overflow when calculating the end address.
2. Stores the supplied base pointer and size.
3. Calculates the end pointer.
4. Marks the tree initialized when the base pointer is non-null.

It does **not** parse and validate the entire tree at initialization time, verify an FDT magic value, or establish who produced the data. Later traversal/property routines perform bounds checks as they access node and property data.

The name “SecureDT” must not be interpreted as proof of cryptographic authenticity. `SecureDTIsLockedDown()` is tied to build/platform integrity configuration and memory-protection assumptions; it is not a general signature-verification API.

### 3.3 Pointer, size and lifetime requirements

The early Platform Expert code stores `boot_args.deviceTreeP` and `boot_args.deviceTreeLength`, then initializes SecureDT with those values. The tree must therefore be:

- Present at the supplied pointer and described by a correct nonzero length.
- In an address range accessible to the early kernel code.
- Stable and readable for the duration of every consumer that retains or uses tree pointers.
- Internally consistent with the node/property layout expected by this XNU revision.
- Large enough to contain every traversed node and property, with correct lengths and alignment.

The exact Motorola firmware handoff address, lifetime, ownership, protection and relocation rules are not known. The pinned source includes a tree-slide routine that adjusts the stored pointer and reinitializes SecureDT, but this does not establish a Moto G60 producer contract.

## 4. Early property-consumer inventory

“Required” below means required by the reviewed source path or a particular conditional code path—not a universal requirement for every XNU build.

| Path / node | Property | Consumer and interpretation | Requirement level |
|---|---|---|---|
| Boot arguments | `deviceTreeP` | Pointer passed to `SecureDTInit` | Required for tree-backed initialization |
| Boot arguments | `deviceTreeLength` | Byte length passed to SecureDT bounds logic | Required for bounded tree access |
| `/chosen` | `dram-base` | Read by ARM startup as an `unsigned long` value | Required in reviewed ARM64 boot-CPU path; absence causes panic |
| `/chosen` | `dram-size` | Read by ARM startup as an `unsigned long` value | Required in reviewed ARM64 boot-CPU path; absence causes panic |
| `/chosen` | `xnu_platform_stall` | Read in a development/debug conditional path | Conditional |
| `/cpus` | Child `state` | Only CPU entries whose state compares as `running` are processed | Required for a CPU entry to contribute |
| `/cpus/*` | `timebase-frequency` | Optional timebase frequency; code accepts 4- or 8-byte values | Optional; default retained if absent |
| `/cpus/*` | `bus-frequency` | Optional bus frequency; code accepts 4- or 8-byte values | Optional; default retained if absent |
| `/cpus/*` | `memory-frequency` | Optional memory frequency; code accepts 4- or 8-byte values | Optional |
| `/cpus/*` | `peripheral-frequency` | Optional peripheral frequency; code accepts 4- or 8-byte values | Optional |
| `/cpus/*` | `fixed-frequency` | Optional fixed frequency; code accepts 4- or 8-byte values | Optional |
| `/cpus/*` | `clock-frequency` | Optional CPU frequency; code accepts 4- or 8-byte values | Optional |
| Node found by `name = arm-io` | `device_type` | Copied into the SoC device-type buffer | Used by the SoC-base path |
| Node found by `name = arm-io` | `ranges` | Second machine-word entry is used as the SoC physical base | Used by the SoC-base path; exact encoding/length contract needs producer-side confirmation |
| Node found by `interrupt-controller = master` | `reg` | First two machine-word entries are used as register offset and size for mapping | Used by the reviewed interrupt-controller mapping path |
| Node found by `device_type = timer` | `reg` | First two machine-word entries are used as timer register offset and size | Used by the reviewed timer mapping path |
| Node found by `name = device-tree` | `target-type` | Copied into a bounded target-type buffer | Optional metadata |
| Node found by `name = device-tree` | `model` | Copied into a bounded model buffer | Optional metadata |
| `/chosen` | `debug-enabled` | Copied into a debug-enabled flag | Optional metadata |
| `/chosen` | `firmware-version` | Copied into the firmware-version buffer | Optional metadata |
| `/chosen` | `system-firmware-version` | Read in a specific target/build conditional | Conditional metadata |
| `/chosen` | `unique-chip-id` | Copied into the platform ECID storage | Optional metadata |
| `/chosen` | `dram-vendor-id` | Copied into platform memory-ID storage | Optional metadata |
| `/product` | `chip-role` | Read for an XNU target conditional | Conditional metadata |

### 4.1 Important interpretation details

- The ARM startup path treats missing `/chosen`, `dram-base`, or `dram-size` as fatal.
- The `pe_identify_machine` path returns early if it cannot obtain a nonzero SoC base from the `arm-io` node. If a SoC base is available, it asserts that `/cpus` exists.
- CPU frequency properties are not all mandatory. The code initializes defaults and selectively replaces them when properties are present.
- The interrupt-controller and timer mapping code searches for Apple-style identifying properties, then interprets `reg` as a pair of machine-word values. That is not automatically equivalent to Linux FDT's `reg` cell encoding.
- Some consumers copy a property into a fixed buffer and force a trailing NUL; others interpret returned bytes as raw integer values. A property name alone does not specify its encoding.
- The reviewed code does not consistently validate every property length before dereferencing/casting the value. This is a source-level producer-contract concern, not a recommendation to reproduce unsafe parsing.

## 5. Apple SecureDT versus standard Linux FDT

| Aspect | Pinned XNU SecureDT representation | Standard FDT |
|---|---|---|
| Top-level binary layout | Node/property records traversed as in-memory structures | Header, reservation map, structure block and strings block |
| Node header | `nProperties`, `nChildren` counters | Begin/end-node tokens in the structure block |
| Property header | Fixed 32-byte name plus 32-bit value length | Property token, value length and name-string offset |
| Property names | Stored in each property record | Stored in a separate strings block and referenced by offset |
| Property values | Returned as pointer/length into the tree | Stored in the tokenized structure block |
| Numeric encoding | Consumers in this source often read native machine-word values | FDT cells are big-endian 32-bit quantities |
| Alignment | SecureDT property traversal rounds records to four-byte boundaries | FDT uses specified alignment for header/reservation/structure blocks and token data |

The standard FDT layout is described in the [Devicetree Specification, Chapter 5](https://devicetree-org.github.io/devicetree-specification/). This comparison is about binary format and consumer expectations; it does not claim that the logical hardware descriptions cannot be translated between formats.

**Research implication:** the shared Moto Linux DTS files are valuable hardware evidence, but they do not prove that the bytes supplied to XNU are already in the representation expected by SecureDT.

## 6. Moto G60 evidence assessment

The existing hanoip / SDMMAGPIE evidence describes a Linux device-tree source family shared by Moto G40 Fusion and Moto G60. It includes SoC nodes, reserved-memory regions, interrupt-controller descriptions and timer declarations.

That evidence does not establish:

- The exact tree format passed by firmware on XT2135-2.
- Whether firmware passes an FDT, a vendor-specific structure, an Apple-compatible tree, or another representation.
- Whether any component translates or transforms the Linux-oriented tree before an OS handoff.
- Whether the exact target tree has Apple-style `/chosen`, `arm-io`, `interrupt-controller = master`, or `device_type = timer` conventions.
- Whether `dram-base` and `dram-size` exist, what their exact byte widths/encoding are, or whether they describe the same memory range XNU expects.
- Whether all values and register windows correspond to the exact XT2135-2 board revision.
- Whether the tree pointer remains valid and protected for the lifetime required by XNU.

Linux `reserved-memory` carveouts are not a substitute for proving the exact DRAM base/size and memory ownership contract consumed by XNU. The target's exact board revision and complete physical memory map remain unresolved.

## 7. Requirements checklist for future evidence

This checklist is for documenting evidence, not for creating or passing a boot payload.

- [ ] Identify the actual firmware-to-OS device-tree format for the exact XT2135-2 model and board revision.
- [ ] Record the authoritative producer documentation or source for the format and handoff contract.
- [ ] Establish whether the tree is standard FDT or the pinned XNU SecureDT record layout.
- [ ] Record pointer ownership, addressability, size, lifetime and relocation behavior from authoritative evidence.
- [ ] Determine whether the required `/chosen/dram-base` and `/chosen/dram-size` properties exist and document their producer-defined type/encoding.
- [ ] Document the exact `/cpus` and CPU-state/frequency properties consumed by the selected source configuration.
- [ ] Determine whether the SoC-base, interrupt-controller and timer node conventions used by the pinned Apple code are present in any authoritative target handoff description.
- [ ] Separate exact-model evidence from shared hanoip-family and generic SoC evidence.
- [ ] Review all future source reuse for file-level license and provenance requirements.

No unknown addresses, property values, tree blobs or hardware claims should be filled in by guessing.

## 8. Safe research boundaries

This milestone is limited to source inspection, documentation and offline format research. It does not include:

- Obtaining, extracting or modifying protected firmware or restore images.
- Changing device boot configuration or bootloader state.
- Creating a device boot payload or attempting a kernel handoff.
- Writing to device partitions or altering the handset.
- Treating a successful structural parse as proof of firmware authenticity or device compatibility.

A future host-only parser test may validate a documented sample format using synthetic test data, but it would not prove the exact XT2135-2 firmware contract.

## 9. Pinned source references

All XNU references below use `xnu-11215.1.10`:

- [Device tree structures and API — `pexpert/pexpert/device_tree.h`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/device_tree.h)
- [SecureDT implementation — `pexpert/gen/device_tree.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/gen/device_tree.c)
- [Platform Expert initialization — `pexpert/arm/pe_init.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_init.c)
- [Machine identification and SoC/interrupt/timer consumers — `pexpert/arm/pe_identify_machine.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_identify_machine.c)
- [ARM startup — `osfmk/arm/arm_init.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)
- [Devicetree Specification](https://devicetree.org/specifications/)
- [Moto hanoip / SDMMAGPIE platform evidence](../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
- [XNU early platform service dependency inventory](XNU_EARLY_PLATFORM_DEPENDENCIES.md)
- [Boot ABI compatibility gap analysis](BOOT_ABI_COMPATIBILITY_GAPS.md)

## 10. Conclusion

The pinned XNU SecureDT implementation expects an Apple-specific flattened node/property representation and a set of Apple platform naming/property conventions. The standard Linux FDT format used in many ARM Linux environments has a different binary layout and property encoding model.

The current Moto G60 family research is based on Linux/Android sources and does not establish the exact XT2135-2 firmware handoff format or the Apple-style properties consumed by this XNU baseline. The mandatory `/chosen/dram-base` and `dram-size` reads, together with the early `/cpus` and SoC-node consumers, are concrete unresolved requirements.

**Overall status: SecureDT requirements documented; exact target tree format, producer contract and compatibility remain unknown.**

*Project: MotoDarwin18*


## 11. Property compatibility matrix — 2026-11-08

Added the [Device Tree Property Compatibility Matrix](DEVICE_TREE_PROPERTY_COMPATIBILITY_MATRIX.md). It compares the early properties and nodes consumed by pinned `xnu-11215.1.10` with the currently documented Hanoip/SDMMAGPIE Linux source evidence.

The matrix distinguishes conceptual hardware overlap from a demonstrated property-level match. GICv3/PDC, timer descriptions, CPU topology, and reserved-memory entries are useful family-level leads, but they do not establish the Apple-style node names, property encodings, or firmware handoff contract expected by XNU. In particular, the reviewed evidence does not document `/chosen/dram-base` or `/chosen/dram-size`; this is **not observed in reviewed source**, not proof those properties are absent from the target's actual firmware tree.

No exact-model tree was extracted or tested, and no device configuration was changed.
