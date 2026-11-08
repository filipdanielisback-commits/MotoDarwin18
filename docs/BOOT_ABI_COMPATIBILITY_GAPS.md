# Boot ABI Compatibility Gap Analysis

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2  
**XNU baseline:** `xnu-11215.1.10`, peeled commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`  
**Date:** 2026-11-08  
**Status:** Research analysis; no target boot integration or device compatibility is established.

## 1. Purpose

Compare the verified early-startup expectations of the selected XNU source baseline with the evidence currently available for the Moto G60 XT2135-2.

This is a gap register, not a boot procedure. It does not provide addresses, register values, firmware changes, bootloader operations, or a device handoff implementation.

## 2. Evidence rules

Use these categories consistently:

- **XNU requirement verified:** directly supported by the pinned XNU source reviewed in this project.
- **Family-level clue:** described by shared hanoip / SDMMAGPIE Android or Linux sources, but not confirmed for the exact XT2135-2 board revision.
- **Exact-model fact:** directly tied to XT2135-2 by reliable evidence.
- **Unknown:** the evidence needed to make a compatibility decision is not available.
- **Gap:** a required interface or contract has not been shown to match.

A documented Linux device-tree node is not proof of XNU support. A source-level ABI declaration is not proof that Motorola firmware supplies that ABI.

## 3. Executive summary

**Current conclusion: the boot ABI is not demonstrated to be compatible.**

The pinned XNU source expects a specific ARM64 startup environment and a structured `boot_args` handoff. The public hanoip sources provide useful clues about the SoC and peripheral topology, but they do not establish the firmware-to-kernel contract, exact board revision, complete physical memory map, or an XNU-compatible device-tree and CPU-state handoff.

The largest blockers are:

1. No verified XT2135-2 firmware-to-kernel handoff contract.
2. No confirmed mapping from the exact handset board revision to the shared DVT overlays.
3. No exact-model physical memory map or reserved-memory ownership record.
4. No demonstrated compatibility between the target's platform description and XNU's Secure Device Tree expectations.
5. No verified CPU entry-state, exception-level, MMU, cache, or interrupt-controller initialization contract.
6. No target-specific XNU Platform Expert, interrupt, timer, or console implementation.

These gaps are independent. Resolving one does not imply the others are solved.

## 4. Compatibility matrix

| Area | Pinned XNU expectation / dependency | Available Moto evidence | Assessment |
|---|---|---|---|
| Firmware entry contract | ARM64 startup receives a pointer to the expected boot arguments and enters the XNU startup path in a compatible processor state | Android/Linux source trees exist, but no exact-model public firmware handoff contract is recorded | **Unknown — critical gap** |
| `boot_args` structure | ARM64 structure with revision/version, address and memory fields, video metadata, machine type, device-tree pointer/length, command line, flags and actual memory size | No evidence that XT2135-2 firmware produces this Apple-specific structure | **Not demonstrated — critical gap** |
| Revision/version compatibility | XNU declares revisions 1/2 and versions 1/2; at least one consumer gates `bootFlags` on revision 2 | No Motorola producer contract or supported version mapping | **Unknown — critical gap** |
| CPU execution state | Startup assembly and C code rely on a defined ARM64 boot CPU state, stack, translation setup and boot-argument accessibility | SoC family is ARM64-capable; exact firmware entry state is not documented here | **Unknown — critical gap** |
| Kernel virtual/physical layout | `virtBase`, `physBase`, and related boot values feed startup and VM mapping | No exact-model kernel image layout or address-space contract | **Unknown — critical gap** |
| Physical memory | XNU VM uses `memSize`, `memSizeActual`, and `topOfKernelData` to establish managed memory and allocator boundaries | Shared DTS contains reserved-memory carveouts; it is not a complete exact-model RAM map | **Partial clue; critical gap** |
| Device tree | Platform Expert captures `deviceTreeP` and `deviceTreeLength`, then initializes SecureDT and queries properties | Shared Linux DTS files describe platform hardware; no proof they match the format, properties, ownership, or lifetime expected by this XNU build | **Not demonstrated — critical gap** |
| Machine identification | Early Platform Expert path calls `pe_identify_machine(boot_args_ptr)` | No supported XNU machine-type mapping for XT2135-2 | **Unknown — critical gap** |
| Video metadata | XNU captures the nested `Video` structure during early Platform Expert initialization | Family-level panel and DSI clues exist; no verified XNU-compatible framebuffer handoff | **Unknown; not necessarily first milestone blocker** |
| Interrupt controller | Later Platform Expert initialization calls `pe_arm_init_interrupts`; kernel requires a compatible interrupt environment | Shared SDMMAGPIE DTS describes GICv3 and Qualcomm PDC | **Promising family-level clue; integration unknown** |
| Timer/timebase | XNU startup and scheduler require a usable timer/timebase and interrupt path | Shared DTS lists an Arm generic timer at 19.2 MHz and a timer block | **Promising family-level clue; exact configuration and XNU integration unknown** |
| Console/debug | Platform Expert invokes debug setup and early startup needs diagnosable output | No verified target console handoff or XNU console integration | **Unknown** |
| Storage | Not required to prove the earliest CPU/startup milestone, but needed for a useful persistent system | Shared tree describes UFS and SD-card controller paths | **Family-level clue; driver and exact device unknown** |
| Power/thermal | Required for robust device operation; not necessarily the first kernel entry dependency | Shared overlays mention PM6150/PM6150L and MC50 battery profiles | **Family-level clue; exact population unknown** |
| Display | Later subsystem; XNU video metadata does not itself implement the display controller | Candidate Tianma ILI7807S MIPI-DSI panel in family source | **Family-level clue; no XNU driver** |
| Wireless/audio/sensors/camera | Later platform and user-space dependencies | Some shared family nodes/modules are documented | **Family-level clues only; no XNU drivers** |
| Security/firmware services | Platform may depend on firmware-owned resources and secure services; exact XNU configuration assumptions must be audited | No exact-model public contract recorded | **Unknown — critical research gap** |

## 5. Detailed gap analysis

### 5.1 Firmware entry and CPU state

**XNU-side evidence:** The pinned ARM64 startup code treats the incoming boot arguments and processor state as part of the kernel entry contract. The C startup routine copies the structure and calls early Platform Expert initialization. Startup assembly establishes or relies on translation mappings before entering C.

**Moto-side evidence:** ARM64-capable Snapdragon platform family. This is not evidence of the exact register state, exception level, stack, cache state, translation regime, or pointer accessibility at the point where an XNU image would begin.

**Gap:** No exact-model producer-side boot contract has been established. A generic ARM64 CPU is insufficient to establish compatibility with Apple's startup assumptions.

**Evidence needed:** Authoritative, non-invasive documentation of the platform's firmware interfaces and a source-level comparison with the selected XNU startup contract. Until then, status remains Unknown.

### 5.2 Boot arguments and structure compatibility

**XNU-side evidence:** The pinned `boot.h` declares a specific `boot_args` structure. Its field types, order, nested `Boot_Video` structure and 1,024-byte command-line buffer are recorded in [Pinned XNU Source Verification](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md).

**Moto-side evidence:** No evidence shows that the target firmware creates this Apple-specific structure or that a documented platform interface translates an existing handoff into it.

**Gap:** Structure existence in XNU does not mean another vendor's firmware supplies it. Matching a few field names would not establish ABI compatibility; layout, versioning, address semantics, ownership and lifetime all matter.

**Evidence needed:** A documented producer contract and a complete source-level compatibility review. No guessed structure values should be added to the project manifest.

### 5.3 Memory map and ownership

**XNU-side evidence:** Pinned ARM64 VM code uses `virtBase`, `physBase`, `memSize`, `memSizeActual`, and `topOfKernelData`. These values influence managed memory, physical-to-virtual mapping and the initial allocator boundary.

**Moto-side evidence:** Shared SDMMAGPIE device-tree files contain multiple reserved-memory carveouts for firmware and peripheral subsystems.

**Gap:** Reserved-memory entries alone do not describe every physical RAM bank, every reservation, firmware ownership, or the exact map for the XT2135-2 board revision. A Linux DTS snapshot cannot safely be treated as a complete XNU memory map.

**Evidence needed:** Exact-model and revision-scoped memory evidence with provenance, including the distinction between usable RAM and firmware/peripheral reservations. Until then, all target addresses and sizes remain unknown.

### 5.4 Device-tree contract

**XNU-side evidence:** Early Platform Expert initialization captures the device-tree pointer and length, initializes SecureDT, identifies the machine, and reads properties such as model/target information and selected `/chosen` properties.

**Moto-side evidence:** Public Linux device-tree sources describe the shared hanoip / SDMMAGPIE family and multiple board-revision overlays.

**Gap:** The existence of a Linux device tree does not establish that the target's firmware passes a tree in the format and semantic contract expected by this XNU version. Property names, compatible strings, address encodings, pointer lifetime, and trust/ownership rules need separate review.

**Evidence needed:** A documented device-tree producer/consumer contract and property-level comparison. Do not assume that a Linux DTB can be supplied unchanged to SecureDT.

### 5.5 Interrupts and timers

**XNU-side evidence:** The later Platform Expert path calls the ARM interrupt and debug initialization functions. Kernel execution also depends on working timer/timebase services.

**Moto-side evidence:** Shared SDMMAGPIE sources describe GICv3/PDC and a 19.2 MHz Arm generic timer.

**Gap:** A controller or timer node in a Linux DTS does not implement the corresponding XNU platform service. Exact interrupt routing, enabled timer source, firmware ownership, initialization order and required register/interrupt abstractions remain unverified.

**Evidence needed:** Revision-specific source evidence and a separately reviewed XNU interface design. No interrupt numbers, register maps, or initialization values are inferred here.

### 5.6 Machine identity and platform services

**XNU-side evidence:** Early startup calls `pe_identify_machine`; Platform Expert also supplies platform-specific services and later interrupt/debug setup.

**Moto-side evidence:** The target identity is XT2135-2, associated with the shared hanoip family, but no supported machine-type value or Motorola Platform Expert implementation is established.

**Gap:** Product model strings and Android board codenames are not automatically valid XNU machine identifiers. Platform Expert APIs represent operating-system services, not merely a hardware list.

**Evidence needed:** A source-level inventory of required Platform Expert services and a design explaining which can be satisfied by documented platform interfaces.

## 6. What is and is not a first milestone dependency

### Early kernel-entry research dependencies

These are the highest priority because failure in any one can prevent reaching meaningful kernel initialization:

1. Exact entry-state and firmware contract.
2. Compatible boot-argument producer contract.
3. Kernel image virtual/physical layout assumptions.
4. Complete memory ownership and reservation model.
5. Device-tree format, lifetime and required properties.
6. CPU topology and required early platform services.
7. Interrupt and timer dependencies needed for continued execution.

### Later platform work

These are important for a usable device but should not be confused with proof of initial kernel entry:

- Display and touchscreen.
- UFS storage and removable storage.
- Wireless, Bluetooth and audio.
- Camera and sensors.
- Battery, charging, thermal and power management.
- iOS 18 userland and proprietary Apple services.

This ordering is a research prioritization, not a claim that any early dependency has already been solved.

## 7. Compatibility decision

| Question | Current decision |
|---|---|
| Is the SoC architecture broadly relevant to ARM64 XNU research? | Yes, at the architecture level only |
| Is the Apple ARM64 `boot_args` ABI known? | Its selected source declarations and several consumers are documented |
| Does XT2135-2 firmware provide that ABI? | Unknown |
| Is the exact target memory map known? | No |
| Is the exact target device-tree contract known? | No |
| Are GICv3 and generic timer plausible platform-family components? | Yes, based on shared Linux source evidence |
| Are XNU interrupt/timer services implemented for this device? | No |
| Is a minimal XNU kernel boot demonstrated? | No |
| Is iOS 18 compatibility demonstrated? | No |

**Overall status: Not demonstrated / blocked by missing platform evidence.** This is not a conclusion that a port is impossible. It means the available evidence is insufficient to claim compatibility or responsibly proceed to device-specific integration.

## 8. Recommended next research tasks

1. **Complete XNU consumer audit:** trace version checks, command-line parsing, machine identification and all early Platform Expert calls in the pinned baseline.
2. **Create a platform-service dependency inventory:** list early XNU calls and classify them as architecture generic, Apple-specific, or target-specific, with source references.
3. **Improve exact-model evidence:** keep board-revision mapping and memory ownership unknown until authoritative sources establish them.
4. **Review device-tree semantics:** document the difference between Linux DTS conventions and the selected XNU SecureDT consumer expectations.
5. **Define host-only tests:** validate documentation, schema consistency, provenance and source-reference integrity without connecting to or modifying a phone.

Do not proceed from this gap analysis to device handoff construction or device modification. The next milestone is still source and evidence review.

## 9. Sources

### Pinned XNU sources

- [ARM64 boot header at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/arm64/boot.h)
- [ARM startup at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)
- [ARM Platform Expert initialization at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_init.c)
- [ARM64 VM initialization at xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm64/arm_vm_init.c)
- [Detailed pinned source verification in this project](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md)

### Moto platform-family sources

- [Motorola hanoip Android device tree](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [LineageOS SDMMAGPIE kernel device-tree source](https://github.com/LineageOS/android_kernel_motorola_sm6150)
- [MotoDarwin18 Hanoip / SDMMAGPIE evidence report](../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
- [MotoDarwin18 exact-model unknowns register](DEVICE_UNKNOWNS.md)

## 10. Conclusion

The pinned XNU startup contract is now substantially better understood, and the shared hanoip source tree provides useful hardware-family clues. The bridge between those two bodies of evidence remains unproven.

The most important unanswered question is not simply whether the Snapdragon 732G is ARM64-capable. It is whether the exact XT2135-2 firmware, memory layout, device description and platform services can satisfy the selected XNU startup contract. Current public evidence does not answer that question.

*Project: MotoDarwin18*
