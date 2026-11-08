# SecureDT Contract Crosswalk — Pinned XNU vs Hanoip Evidence

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2 / MC38C  
**XNU baseline:** xnu-11215.1.10, peeled commit 8d741a5de7ff4191bf97d57b9f54c2f6d4a15585  
**Review date:** 2026-11-08  
**Status:** Source-derived requirements and source-to-source evidence comparison only. Exact XT2135-2 firmware tree and producer contract remain unknown.

## 1. Executive result

This crosswalk classifies the SecureDT-related requirements consumed by the pinned XNU ARM64 startup path and compares them with documented shared Hanoip / SDMMAGPIE Linux/Android source evidence.

**Result:** the reviewed Hanoip material offers conceptual hardware clues for CPUs, memory, interrupt controllers, timers and SoC peripherals. It does not demonstrate that an XT2135-2 firmware handoff supplies the Apple XNU SecureDT representation, the property names searched by XNU, the expected value encodings, or the memory ownership/lifetime contract.

No compatibility conversion, boot handoff, or executable kernel patch is designed here. No actual target tree was obtained or tested.

## 2. Classification rules

These labels apply to the selected XNU baseline and reviewed code path, not every possible XNU configuration.

- **Required — early path:** the reviewed boot path directly requires the item; absence is fatal or prevents that path from proceeding.
- **Required — gated path:** required only after a preceding condition selects the consumer path.
- **Later-phase dependency:** consumed after initial Platform Expert setup, during interrupt/timebase or later platform initialization.
- **Optional:** the consumer checks for the property and retains a default or continues when absent.
- **Conditional:** read only under a specific build, target or debug/development condition.
- **Format contract:** representation, pointer, length, alignment, lifetime or encoding requirement rather than a hardware feature.
- **Unknown on target:** no authoritative exact XT2135-2 firmware-side evidence has been located.
- **Family clue only:** the Hanoip/SDMMAGPIE source tree contains a related declaration, but it is not mapped to the exact XT2135-2 board revision or firmware handoff.

“Not observed in the reviewed Linux source” does not mean “absent from the handset” or “absent from firmware.”

## 3. Representation-level crosswalk

| Contract item | Pinned XNU consumer expectation | Hanoip / SDMMAGPIE evidence | Assessment |
|---|---|---|---|
| Tree representation | SecureDT walks XNU in-memory node/property records: node counters, fixed 32-byte property-name field, 32-bit property byte length, value bytes and four-byte property-record alignment | Shared Android/Linux sources are DTS/DTSI descriptions; no exact firmware handoff blob or producer format is documented | **Format contract unknown** |
| Tree pointer | boot_args.deviceTreeP is retained by Platform Expert and passed to SecureDTInit | No exact XT2135-2 firmware producer pointer or ownership specification | **Unknown** |
| Tree length | boot_args.deviceTreeLength bounds SecureDT traversal | No exact target tree size or length semantics | **Unknown** |
| Tree lifetime | Consumers retain pointers into the supplied tree; the tree-slide path adjusts the stored pointer and reinitializes SecureDT | No exact firmware lifetime, relocation, reservation or protection contract | **Unknown** |
| Tree integrity | SecureDT performs bounds checks during traversal; initialization records base and size and checks pointer-plus-size overflow | No evidence about target producer validation or protected placement | **Unknown; the name SecureDT does not prove cryptographic authenticity** |
| Numeric property encoding | Some XNU consumers interpret returned bytes as native machine-word values; each consumer determines the expected type | Linux FDT uses big-endian 32-bit cells for standard integer cells, with address/size cell counts determined by the tree | **Potential representation/encoding incompatibility; exact target tree unknown** |

The standard Devicetree Specification describes a DTB as a header plus reservation, structure and strings blocks, with tokenized node/property records. Its standard integer cells are big-endian. Similar logical concepts (nodes, properties, children) do not make the DTB binary representation interchangeable with XNU SecureDT. See the [Devicetree Specification](https://devicetree.org/specifications/) and the existing [Secure Device Tree Requirements Analysis](../../docs/SECURE_DEVICE_TREE_REQUIREMENTS.md).

## 4. Early boot property and node crosswalk

### 4.1 Boot-argument tree reference

| XNU field | Classification | Hanoip evidence | Target status |
|---|---|---|---|
| deviceTreeP | Required format contract for tree-backed early Platform Expert setup | None for firmware producer | Unknown |
| deviceTreeLength | Required format contract for bounded traversal | None for firmware producer | Unknown |

Platform Expert copies these fields from boot_args and calls SecureDTInit in the first PE_init_platform phase. The SecureDT API's base/size pair is part of the consumer contract. The exact XT2135-2 producer contract has not been found.

### 4.2 DRAM properties

| Path/property | Classification | Hanoip evidence | Target status |
|---|---|---|---|
| /chosen | Required — early ARM64 boot-CPU path | Shared Linux DTS family material, but no exact Apple-style firmware-tree node evidence | Unknown |
| /chosen/dram-base | Required — early ARM64 boot-CPU path; source reads it as an unsigned machine-word value | Linux memory nodes and reserved-memory carveouts are present in family source; they do not prove this property | Unknown |
| /chosen/dram-size | Required — early ARM64 boot-CPU path; source reads it as an unsigned machine-word value | Same family-level memory evidence; no exact property contract established | Unknown |

The reviewed ARM startup code panics if it cannot find /chosen, dram-base, or dram-size. This is a concrete consumer requirement. It does not establish whether XT2135-2 firmware supplies these properties, uses another representation, or describes memory differently.

The shared Hanoip reserved-memory entries are not a complete physical-memory map and do not establish which regions firmware, the operating system, or other components own.

### 4.3 SoC identity and base

| Node/property | Classification | Pinned consumer behavior | Hanoip evidence / target status |
|---|---|---|---|
| Node found by name = arm-io | Required — gated SoC-identification path | Used to locate the SoC I/O description | Family source describes Qualcomm SoC peripheral nodes; exact Apple-style node absent from verified target evidence |
| arm-io/device_type | Consumed on the SoC-base path | Copied into an internal SoC device-type buffer | Exact property/value unknown |
| arm-io/ranges | Consumed on the SoC-base path | Second machine-word entry is read as the SoC physical base | Hanoip Linux bus/ranges descriptions are not proven to have the same layout or encoding |
| /cpus | Required — gated by successful nonzero SoC-base discovery | pe_identify_machine asserts successful lookup of /cpus after the SoC-base check passes | Shared source describes CPU nodes; exact SecureDT structure, naming and CPU-state semantics unknown |

**Control-flow nuance:** if the SoC-base lookup returns zero, pe_identify_machine returns before the /cpus lookup. If a nonzero SoC base is found, the reviewed code asserts that /cpus exists. Therefore /cpus is a gated requirement, not an unconditional requirement for every execution through that function.

### 4.4 CPU child properties

| Path/property | Classification | Pinned consumer behavior | Hanoip evidence / target status |
|---|---|---|---|
| /cpus/*/state | Required for a CPU entry to contribute to the frequency scan | Entries whose state property is missing or does not compare as running are skipped | Shared family source has CPU nodes; exact property bytes and running-state representation unknown |
| timebase-frequency | Optional | Replaces a default when present; consumer has 4-byte and 8-byte branches | Family timer declaration includes a 19.2 MHz generic timer, but this does not prove this CPU property or its encoding |
| bus-frequency | Optional | Replaces a default when present | Exact target value/property unknown |
| memory-frequency | Optional | Replaces a default when present | Exact target value/property unknown |
| peripheral-frequency | Optional | Replaces a default when present | Exact target value/property unknown |
| fixed-frequency | Optional | Replaces a default when present | Exact target value/property unknown |
| clock-frequency | Optional | Replaces a default when present | Shared CPU descriptions do not establish the exact SecureDT property |

The source initializes defaults before reading these optional properties. The existence of a generic timer in a Linux DTS is not proof that the XNU consumer sees a matching CPU property.

## 5. Later Platform Expert dependencies

These are not the same as the initial tree-pointer and DRAM requirements. They are consumed by the later Platform Expert initialization phase.

| Node/property | Classification | Pinned consumer behavior | Hanoip evidence / target status |
|---|---|---|---|
| Node found by interrupt-controller = master | Later-phase dependency | Searched during interrupt-controller mapping | Family SoC tree describes GICv3 and PDC; no exact XNU-style node identity or target handoff mapping |
| Interrupt-controller reg | Later-phase dependency | First two native machine-word entries are used as register offset and size, then combined with SoC base for mapping | Linux reg is encoded according to parent address/size cells in standard FDT; semantic equivalence not established |
| Node found by device_type = timer | Later-phase dependency | Searched during timer mapping | Family source describes generic and memory-mapped timer resources; exact XNU-style node unknown |
| Timer reg | Later-phase dependency | First two native machine-word entries are used as register offset and size | Exact target encoding and address relationship unknown |

**Control-flow nuance:** PE_init_platform(TRUE, ...) calls pe_arm_init_interrupts. The reviewed mapper returns failure if it cannot find/map the expected interrupt-controller or timer regions. The caller does not turn that return value into an explicit panic in the inspected function. This is still a later platform dependency, but it should not be mislabeled as the same immediate fatal condition as missing DRAM properties.

The Hanoip GICv3/PDC and timer entries are hardware-family clues only. They do not prove the XNU SecureDT node names, property values, register-window interpretation, interrupt routing, timer selection or ownership.

## 6. Optional and conditional metadata

| Path/property | Classification | Consumer behavior | Target status |
|---|---|---|---|
| Node found by name = device-tree, property target-type | Optional metadata | Copied into a bounded internal buffer when found | Unknown |
| Node found by name = device-tree, property model | Optional metadata | Copied into a bounded internal buffer when found | Motorola regulatory identity is confirmed separately; no exact SecureDT property evidence |
| /chosen/debug-enabled | Optional metadata | Read when /chosen exists; copied into debug flag | Unknown |
| /chosen/firmware-version | Optional metadata | Copied into firmware-version buffer when present | Motorola Android firmware release tags do not establish this SecureDT property |
| /chosen/system-firmware-version | Conditional metadata | Read in a specific macOS ARM64 target conditional | Not established for XT2135-2 |
| /chosen/unique-chip-id | Optional metadata | Copied into platform ECID storage when present | Unknown |
| /chosen/dram-vendor-id | Optional metadata | Copied into platform memory-ID storage when present | Unknown |
| /product/chip-role | Conditional metadata | Read only in a target-specific conditional path | Unknown |
| /chosen/xnu_platform_stall | Conditional debug/development property | Read only under DEVELOPMENT or DEBUG in the reviewed ARM startup path | Not a general production requirement |

Optional and conditional metadata should not be promoted into mandatory XT2135-2 requirements. Conversely, optional does not mean safe to guess if a future selected configuration consumes the value.

## 7. Family evidence: what it does and does not establish

The current shared Hanoip / SDMMAGPIE source review provides these **family-level clues**:

- CPU topology declarations in the shared tree.
- GICv3 and Qualcomm PDC descriptions.
- A 19.2 MHz generic timer declaration and a memory-mapped timer block.
- UFS and SD-card controller paths.
- Reserved-memory carveouts.

These are useful leads for a later hardware compatibility study. They do **not** establish:

- The exact XT2135-2 firmware tree representation.
- That firmware passes an Apple SecureDT tree rather than a standard FDT or another vendor format.
- The actual /chosen contents and dram-base / dram-size properties.
- The exact arm-io node, ranges encoding or SoC base expected by this XNU source.
- The interrupt-controller = master and device_type = timer naming conventions.
- The exact property widths, byte order or address/size-cell interpretation at the firmware boundary.
- The tree pointer's lifetime, relocation behavior, protection or memory ownership.
- The physical board revision or DVT1/DVT2 mapping for the target unit.

Motorola's exact-model identity declaration and Android kernel-source publication trail do not supply these missing firmware-to-XNU contracts.

## 8. Requirements status summary

| Requirement group | XNU classification | Exact XT2135-2 evidence | Current status |
|---|---|---|---|
| SecureDT binary representation | Required format contract | None | **Unknown / critical gap** |
| Tree pointer, length and lifetime | Required format contract | None | **Unknown / critical gap** |
| /chosen/dram-base, /chosen/dram-size | Required early | None | **Unknown / critical gap** |
| arm-io SoC base description | Required gated path | None | **Unknown** |
| /cpus and CPU state | Required gated path; state gates each entry | Family CPU nodes only | **Family clue only** |
| CPU frequency fields | Optional | Generic timer clue only | **Unknown** |
| Interrupt-controller and timer nodes | Later-phase dependency | GICv3/PDC/timer family clues | **Family clue only** |
| Optional model/debug/firmware metadata | Optional or conditional | No exact property-level evidence | **Unknown / not blocking by itself** |

## 9. Decision and next research gate

**No executable XNU patch is justified.** The crosswalk identifies consumer requirements and missing evidence, but it does not demonstrate that the exact XT2135-2 producer violates a particular requirement. A Linux DTS declaration is not a substitute for the target firmware contract.

The next valid evidence gate is an authoritative exact-model source that documents the firmware-side tree format and property semantics. If no such public source exists, the project should record the limitation rather than invent values or infer a handoff from Android/Linux DTS files.

Any later proposal must identify:
1. the exact pinned XNU consumer and its selected configuration;
2. an authoritative exact-target producer description;
3. a specific representation or semantic mismatch;
4. why the mismatch is not merely missing evidence;
5. the narrow source-level correction, if one is genuinely required.

This report does not provide a recipe for creating a device tree, setting boot arguments, or transferring control to XNU. No device changes, firmware changes, bootloader changes, partition operations, or target tests were performed.

## 10. Source references

### Pinned XNU

All upstream source references use peeled commit 8d741a5de7ff4191bf97d57b9f54c2f6d4a15585:

- [SecureDT structures and declarations — device_tree.h](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/pexpert/device_tree.h)
- [SecureDT traversal and bounds handling — device_tree.c](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/gen/device_tree.c)
- [Platform Expert phases — pe_init.c](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/arm/pe_init.c)
- [CPU, SoC, interrupt and timer consumers — pe_identify_machine.c](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/arm/pe_identify_machine.c)
- [Early DRAM-property consumers — arm_init.c](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/arm/arm_init.c)

### Project evidence

- [Secure Device Tree Requirements Analysis](../../docs/SECURE_DEVICE_TREE_REQUIREMENTS.md)
- [Device Tree Property Compatibility Matrix](../../docs/DEVICE_TREE_PROPERTY_COMPATIBILITY_MATRIX.md)
- [Hanoip / SDMMAGPIE Platform Evidence](../../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
- [XT2135-2 Confirmed Platform Facts](../../research/firmware/XT2135_2_CONFIRMED_PLATFORM_FACTS.md)
- [XT2135-2 Firmware and Board-Revision Follow-up](../../research/firmware/XT2135_2_FIRMWARE_BOARD_REVISION_FOLLOWUP.md)

### External format reference

- [Devicetree Specification](https://devicetree.org/specifications/) — standard FDT structure, property representation and cell encoding.

## 11. Conclusion

The pinned XNU code defines a concrete SecureDT consumer contract. The shared Hanoip sources provide useful hardware-family clues but do not establish the exact XT2135-2 firmware-side tree, required early properties, property encodings, or later interrupt/timer service descriptions.

The highest-priority unresolved items remain the SecureDT representation and lifetime, the mandatory DRAM properties, and the exact SoC/CPU/interrupt/timer property semantics. Keep source patches deferred until an authoritative exact-target producer contract and a concrete mismatch are demonstrated.

*Project: MotoDarwin18*


## 12. Additional community Hanoip FDT sample reviewed — 2026-11-08

A public community repository contains a 5,300-line expanded Linux DTS snapshot whose root identifies `Motorola Moto G60`, `motorola,hanoip` and `qcom,sm7150`. It includes CPU, memory/reserved-memory, GIC, generic-timer and framebuffer descriptions.

The source-level check found no `/chosen/dram-base`, `/chosen/dram-size`, `arm-io`, `interrupt-controller = "master"`, or `device_type = "timer"` in that particular file. These are observations about one community Linux FDT sample only—not about stock firmware or the XT2135-2.

The community repository self-describes its work as Moto G60/Hanoip/SM7150 and describes an embedded Linux FDT in its own U-Boot build. It does not identify XT2135-2 / MC38C or a physical board revision. Therefore, this is stronger family-level sample evidence, but not an exact-target firmware producer contract.

See [Community Hanoip U-Boot FDT Evidence Audit](HANOIP_COMMUNITY_UBOOT_DTB_EVIDENCE_AUDIT.md). The SecureDT compatibility decision remains unchanged: no executable XNU patch is justified.
