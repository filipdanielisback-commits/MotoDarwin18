# Device Tree Property Compatibility Matrix

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2  
**XNU baseline:** `xnu-11215.1.10`  
**Research date:** 2026-11-08  
**Status:** Source-to-source comparison; exact XT2135-2 firmware handoff remains unknown.

## 1. Purpose and interpretation

This matrix compares properties consumed by the pinned XNU ARM64 startup and early Platform Expert code with the available shared `hanoip` / `SDMMAGPIE` Linux/Android source-tree evidence.

It is a compatibility assessment of **documented source descriptions**, not a dump or inspection of the device's live firmware tree. It does not establish what an individual XT2135-2 unit actually passes to an operating system.

### Status vocabulary

- **Conceptual overlap:** both ecosystems describe a related hardware concept, but the expected node, property, encoding, or consumer contract is not shown to match.
- **Not observed in reviewed source:** the cited Hanoip evidence note does not record the exact XNU property or an equivalent declaration. This does **not** mean the property is absent from the device or firmware.
- **Format/contract mismatch:** available source formats or known consumer expectations differ; direct compatibility must not be assumed.
- **Unknown:** evidence is insufficient to make a comparison.
- **Conditional XNU consumer:** the property is read only for a particular build, target, or code path.

Evidence scope is also stated explicitly: **device-family** means shared Hanoip/G60-family source; **SoC-family** means a shared SDMMAGPIE/Qualcomm description; **exact-model** means evidence tied to XT2135-2 itself. No exact-model firmware-tree evidence is available for this matrix.

## 2. Compatibility matrix

| XNU path / expected item | Pinned XNU expectation | Hanoip / SDMMAGPIE evidence reviewed | Assessment | Evidence scope / confidence |
|---|---|---|---|---|
| Boot arguments: `deviceTreeP` | Pointer to the Apple SecureDT node/property representation | No producer-side firmware handoff pointer or ownership contract is documented | **Unknown** | Exact-model unknown |
| Boot arguments: `deviceTreeLength` | Byte length used by SecureDT bounds logic | No exact handoff length or lifetime contract is documented | **Unknown** | Exact-model unknown |
| Tree binary representation | Apple-specific node/property records used by pinned SecureDT | Research sources are Linux kernel DTS/DTSI and Android device configuration; no evidence that firmware supplies Apple's record layout | **Format/contract mismatch risk** | Device-family source; handoff unknown |
| `/chosen/dram-base` | Required in reviewed ARM64 boot-CPU path; consumed as a native `unsigned long` value | Shared sources describe reserved-memory carveouts, but the reviewed evidence does not document this Apple-style property | **Not observed in reviewed source**; Linux memory descriptions are only conceptual overlap | Device-family / SoC-family |
| `/chosen/dram-size` | Required in reviewed ARM64 boot-CPU path; consumed as a native `unsigned long` value | No exact equivalent property is recorded in the Hanoip evidence note; carveouts do not define the complete RAM range | **Not observed in reviewed source** | Device-family / SoC-family |
| `/chosen/xnu_platform_stall` | Conditional development/debug property | No corresponding declaration recorded | **Conditional; not observed** | Exact-model unknown |
| `/cpus` node | XNU searches for CPU topology; reviewed code asserts its presence after obtaining a usable SoC base | Shared source review records CPU/platform topology context, but does not establish the precise Apple-style tree shape or all required child properties | **Conceptual overlap; exact structure unknown** | SoC-family / device-family |
| `/cpus/*/state` | XNU processes CPU entries whose state compares as `running` | Exact Apple-style `state` property, value encoding, and per-core values are not recorded in the reviewed evidence | **Not observed in reviewed source** | Exact-model unknown |
| CPU frequency properties | Optional `timebase-frequency`, `bus-frequency`, `memory-frequency`, `peripheral-frequency`, `fixed-frequency`, `clock-frequency`; XNU accepts 4- or 8-byte values in reviewed paths | Shared tree documents an Armv8 generic timer at 19.2 MHz, but this does not establish the set, location, or encoding of all CPU frequency properties | **Partial conceptual overlap only** | SoC-family |
| Node identified by `name = arm-io` | Apple-style node lookup; `device_type` and `ranges` used in the SoC-base path | Shared sources describe Qualcomm SoC and peripheral nodes, not an evidenced Apple `arm-io` node with the same property contract | **Conceptual overlap; naming/encoding mismatch possible** | SoC-family |
| `arm-io/device_type` | Copied as SoC device-type metadata | No matching Apple-style node/property pair recorded | **Not observed in reviewed source** | Exact-model unknown |
| `arm-io/ranges` | XNU reads the second machine-word entry as the SoC physical base in the reviewed path | No exact property value, cell count, width, or mapping to this XNU interpretation recorded | **Not observed; do not equate with Linux `ranges`** | Exact-model unknown |
| Interrupt controller node | XNU searches for `interrupt-controller = master` | Shared SoC tree describes an Arm GICv3 interrupt controller and Qualcomm PDC | **Conceptual overlap; not an established match** | SoC-family |
| Interrupt-controller `reg` | XNU interprets the first two machine-word entries as register offset and size in the reviewed mapping path | GICv3/PDC register descriptions exist at family source level, but the Apple node selector and exact `reg` representation are not established | **Conceptual overlap; encoding and node contract unknown** | SoC-family |
| Timer node | XNU searches for `device_type = timer` | Shared tree describes an Armv8 generic timer at 19.2 MHz and a memory-mapped timer block with timer-frame entries | **Conceptual overlap; XNU node selection not established** | SoC-family |
| Timer `reg` | XNU interprets two machine-word entries for the selected timer node | Memory-mapped timer descriptions are recorded, but no proof of an Apple-style `device_type = timer` node or identical value encoding | **Conceptual overlap; exact property contract unknown** | SoC-family |
| `name = device-tree` node | Optional metadata node searched by XNU | No matching node recorded in the reviewed Hanoip summary | **Not observed in reviewed source** | Exact-model unknown |
| `target-type` and `model` | Optional metadata copied into bounded buffers | Android/Linux device identity and codename are documented outside this Apple-style node/property contract | **Conceptual metadata overlap only** | Device-family |
| `/chosen/debug-enabled` | Optional debug metadata | No matching property recorded | **Not observed in reviewed source** | Exact-model unknown |
| `/chosen/firmware-version` | Optional firmware metadata | No matching property recorded | **Not observed in reviewed source** | Exact-model unknown |
| `/chosen/system-firmware-version` | Conditional firmware metadata | No matching property recorded | **Conditional; not observed** | Exact-model unknown |
| `/chosen/unique-chip-id` | Optional unique-chip identifier | No matching property recorded | **Not observed in reviewed source** | Exact-model unknown |
| `/chosen/dram-vendor-id` | Optional memory-vendor metadata | Alternative ATL and SUNWODA battery profiles are documented; these are battery profiles, not DRAM vendor evidence | **Not observed; no valid equivalent identified** | Exact-model unknown |
| `/product/chip-role` | Conditional target-specific metadata | No matching property recorded | **Conditional; not observed** | Exact-model unknown |

## 3. Key findings

### 3.1 Memory handoff is the most consequential unresolved row

The shared Linux source review contains reserved-memory carveouts. Those entries describe regions reserved for particular purposes; they do not by themselves prove the complete physical RAM base and size required by the reviewed XNU ARM64 startup path.

In particular, the evidence note does not establish the presence, type, width, or value of Apple's `/chosen/dram-base` and `/chosen/dram-size` properties. Their absence from the reviewed note must not be interpreted as proof that they are absent from the actual firmware tree.

### 3.2 GIC and timer descriptions are useful leads, not drop-in XNU properties

GICv3/PDC and the generic timer are documented in the shared SoC source evidence. This narrows the hardware research questions, but the pinned XNU code searches for specific Apple-style identifying properties and interprets selected `reg` values according to its own consumer assumptions.

A matching hardware concept is not enough. Node identity, property encoding, register-window interpretation, interrupt routing, and firmware ownership all need independent evidence.

### 3.3 CPU topology is not yet an Apple SecureDT contract

The presence of CPU topology in a Linux SoC description does not establish the exact `/cpus` representation, CPU child `state` values, or optional frequency-property encodings that the pinned XNU path expects.

### 3.4 The tree format is a separate compatibility gate

Even if equivalent hardware facts exist in the Linux DTS, the pinned XNU SecureDT parser expects its Apple-specific in-memory representation. A conventional FDT-style source description is not proof that firmware supplies that representation. Property-by-property semantic similarity cannot resolve a binary-format mismatch.

## 4. Evidence limits

This matrix is based on:

1. The pinned XNU source analysis in [Secure Device Tree Requirements Analysis](SECURE_DEVICE_TREE_REQUIREMENTS.md).
2. The community-source review in [Hanoip / SDMMAGPIE Platform Evidence](../research/soc/HANOIP_PLATFORM_EVIDENCE.md).
3. The shared-family caveats in [Device Unknowns](DEVICE_UNKNOWNS.md).

The Hanoip source family covers related Moto G40 Fusion / Moto G60 configurations and contains multiple board-revision overlays. It is not an official XT2135-2 schematic or a verified dump of the target's firmware handoff tree.

**Not observed in reviewed source** means only that the reviewed evidence does not document the item. It does not mean absent from the hardware, firmware, another overlay, or a runtime-generated tree.

No exact-model device tree has been extracted, parsed, converted, synthesized, or tested. No firmware or device configuration has been changed.

## 5. Recommended next research tasks

1. Keep the exact XT2135-2 firmware tree format and producer contract marked **Unknown** until authoritative evidence exists.
2. Review the source DTS/DTSI files property-by-property in a future source audit, recording exact file paths and line-level provenance rather than inferring from subsystem summaries.
3. Establish which DVT overlay applies to the exact target revision, if reliable public evidence can do so.
4. Seek authoritative documentation for memory ownership and the firmware-to-OS handoff contract.
5. Keep all property values, addresses, and encodings unknown unless directly supported by exact-model evidence.
6. If a future host-only parser is considered, use synthetic fixtures and treat successful parsing as a format test only—not evidence of target compatibility.

This work remains documentation and source research. It does not define a device tree to pass to a kernel, a conversion procedure, or a boot payload.

## 6. References

- [Pinned XNU SecureDT requirements](SECURE_DEVICE_TREE_REQUIREMENTS.md)
- [Pinned XNU early platform dependency inventory](XNU_EARLY_PLATFORM_DEPENDENCIES.md)
- [Boot ABI compatibility gap analysis](BOOT_ABI_COMPATIBILITY_GAPS.md)
- [Hanoip / SDMMAGPIE platform evidence](../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
- [Official Devicetree Specification](https://devicetree.org/specifications/)
- [XNU `device_tree.h` at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/device_tree.h)
- [XNU `device_tree.c` at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/gen/device_tree.c)
- [XNU `pe_identify_machine.c` at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_identify_machine.c)
- [XNU `arm_init.c` at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)

---

**Conclusion:** Several hardware concepts in the shared Hanoip/SDMMAGPIE source tree overlap with what XNU needs, especially CPU topology, interrupt controllers, timers, and memory descriptions. The exact Apple-style property contract, binary tree format, and mandatory DRAM handoff properties are not demonstrated for XT2135-2. Compatibility remains **unknown / not demonstrated**.
