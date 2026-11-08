# XNU ARM64 Startup: Configuration-Dependent Dependency Audit

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2 / MC38C  
**XNU baseline:** `xnu-11215.1.10`, peeled commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`  
**Review date:** 2026-11-08  
**Status:** Pinned-source research only; no kernel patch, build, boot integration, or device test.

## 1. Purpose and decision

This review follows the boot-contract audit by separating:

1. ARM64 architectural mechanisms;
2. XNU's Apple-specific startup and Platform Expert contracts;
3. compile-time and platform-configuration branches;
4. missing XT2135-2-specific implementation/evidence.

The review does **not** treat ARM64 CPU capability as proof of XNU compatibility.

**Decision: no executable XNU source patch is justified by this audit.** The examined code does expose specific platform contracts that a future port would have to satisfy, but the available Moto evidence does not prove that the XT2135-2 producer violates a particular XNU consumer. The present problem is missing target-side evidence and implementation, not a demonstrated defect in the pinned upstream source.

## 2. Source scope and reproducibility

All upstream source references below are pinned to the peeled commit above. The review inspected:

- `osfmk/arm64/start.s`
- `osfmk/arm/arm_init.c`
- `pexpert/arm/pe_init.c`
- `pexpert/arm/pe_identify_machine.c`
- `pexpert/pexpert/arm64/boot.h`
- `pexpert/pexpert/arm64/board_config.h`
- `osfmk/arm64/arm_vm_init.c`
- `osfmk/arm64/cpu.c`
- `osfmk/arm/machine_routines_apple.c`
- `config/MASTER.arm64`
- `config/MASTER.arm64.iPhoneOS`

The exact source file blob hashes were fetched from the pinned revision during this review. No Apple source files were copied into MotoDarwin18; this document records analysis and source locations only.

## 3. Startup path classification

| Layer | Pinned-source behavior | Classification | XT2135-2 status |
|---|---|---|---|
| ARM64 reset/entry assembly | Establishes XNU's expected early CPU state, stack use, exception-vector setup, bootstrap mappings and transition into C startup | ARM64 mechanism, but with an XNU-defined entry contract | Firmware entry state and image layout unknown |
| Boot arguments | Assembly reads virtual base, physical base, memory size and boot flags from the XNU `boot_args` structure; C startup copies the structure | XNU-specific producer/consumer ABI | No Motorola producer contract found |
| Early Platform Expert | Captures device-tree pointer/length and video fields, initializes SecureDT, identifies the machine | Apple XNU platform contract | Exact target SecureDT producer/format unknown |
| Early memory setup | Reads `/chosen/dram-base` and `dram-size`, then initializes ARM64 VM from boot arguments | XNU memory contract plus ARM64 VM implementation | Exact RAM map and ownership unknown |
| Interrupt/timebase setup | Later Platform Expert phase maps expected interrupt-controller and timer nodes and initializes timebase | Platform Expert contract, not just ARM64 ISA | Hanoip GIC/timer clues are family-level only |
| CPU topology and power | Uses CPU topology, CPU-data structures, reset handlers and configuration-dependent power/interrupt paths | ARM64 mechanisms plus platform-specific SMP contract | Exact target topology and CPU-start services unknown |
| Console and peripherals | Serial, framebuffer and later device services are selected through platform-specific facilities | Platform-specific, mostly later than first entry | No exact pre-OS console or XNU device implementation established |

## 4. ARM64 architectural mechanisms versus Apple contracts

### 4.1 What is genuinely architecture-level

The pinned `start.s` uses AArch64 architectural facilities such as stack-pointer selection, exception-vector base setup, translation-control and translation-table registers, cache/MMU enablement, processor identification, and the generic WFI instruction. These are ARM64 mechanisms.

However, the source also assumes XNU's own incoming state and memory layout. For example, the entry path consumes values from the boot-argument block before the C startup routine can establish its later abstractions. Therefore, “uses standard ARM64 instructions” does not mean “accepts any ARM64 firmware handoff.”

### 4.2 Apple-specific and XNU-specific contracts

The source path also relies on:

- Apple's `boot_args` structure and revision/version semantics;
- XNU Secure Device Tree APIs and the expected tree representation;
- `pe_identify_machine` and Platform Expert service entry points;
- Apple board-family and SoC configuration macros;
- platform-specific interrupt, timer, CPU power and debug hooks.

These are not supplied by the ARM architecture itself.

### 4.3 Important nuance: some Apple-named routines have non-Apple stubs

`osfmk/arm/machine_routines_apple.c` is also built for non-Apple ARM64 targets. In that case, the reviewed `configure_misc_apple_boot_args`, `configure_misc_apple_regs`, and `configure_timer_apple_regs` implementations are empty; Apple-family-specific register handling is guarded by `APPLE_ARM64_ARCH_FAMILY`.

This is evidence that the source contains a non-Apple ARM64 path for those particular hooks. It is **not** evidence that the whole XNU startup path is portable without further work: the boot ABI, SecureDT, machine identification, memory contract, interrupt/timebase services, and board configuration remain separate requirements.

## 5. Configuration-dependent assumptions

### 5.1 ARM64 startup assembly

The pinned `start.s` contains materially different paths selected by build-time and platform macros, including:

- `KERNEL_INTEGRITY_KTRR` / `KERNEL_INTEGRITY_CTRR`: routes selected privileged register operations through protected helper routines;
- `__ARM_KERNEL_PROTECT__`: changes exception-vector and kernel-protection setup;
- `HAS_APPLE_PAC`: adds pointer-authentication key-state setup;
- `KASAN`: adds an early sanitizer bootstrap;
- `APPLE_ARM64_ARCH_FAMILY`: enables Apple-family debug-register setup;
- `HAS_CLUSTER` and `NO_CPU_OVRD`: gate cluster/CPU override handling.

These branches show why the selected XNU build configuration must match the intended platform. The project has not established which of these target capabilities or protected-firmware services are present on XT2135-2. Do not select or emulate a branch based on the Snapdragon family name alone.

### 5.2 Boot CPU C startup

In `osfmk/arm/arm_init.c`, the boot CPU path:

1. copies the incoming `boot_args` into XNU's constant copy;
2. calls `PE_init_platform(FALSE, args)`;
3. calls ARM64 timer/configuration hooks;
4. parses CPU topology and initializes the boot CPU structures;
5. initializes early timer and kernel-startup facilities;
6. reads `/chosen/dram-base` and `/chosen/dram-size`;
7. calls `arm_vm_init`;
8. later calls `PE_init_platform(TRUE, &BootCpuData)`, CPU timebase setup and CPU initialization.

This is a source-level call sequence, not a recipe for constructing or passing a device handoff.

### 5.3 Platform Expert and SecureDT assumptions

The pinned `PE_init_platform` implementation copies `deviceTreeP`, `deviceTreeLength`, and video metadata from `boot_args`. On its first phase it calls `SecureDTInit` and `pe_identify_machine`. On the later phase it calls `pe_arm_init_interrupts` and debug initialization.

The pinned `pe_identify_machine.c` contains concrete SecureDT expectations:

- an `arm-io` node with `device_type` and `ranges` information for SoC-base discovery;
- a `/cpus` node and per-CPU properties such as `state` and optional frequency properties;
- an interrupt-controller node discoverable as `interrupt-controller = "master"`, with a `reg` property;
- a timer node discoverable by `device_type = "timer"`, with a `reg` property.

The interrupt/timer path maps the described regions and calls `ml_init_timebase`. Separately, `arm_init.c` requires `/chosen/dram-base` and `/chosen/dram-size`; the reviewed path panics if either is absent.

These are specific XNU consumer expectations. The shared Hanoip Linux DTS evidence for GICv3/PDC and a generic timer does not prove that the XT2135-2 firmware supplies these SecureDT nodes, names, encodings, address semantics, or ownership rules. Nor does it prove that a Linux FDT and XNU SecureDT are interchangeable.

### 5.4 ARM64 VM configuration

The pinned `arm_vm_init` reads `virtBase`, `physBase`, `memSize`, `memSizeActual`, and `topOfKernelData` from `boot_args`. The mapping strategy differs with `ARM_LARGE_MEMORY`, `XNU_MONITOR`, and `KASAN`. The non-large-memory path uses `topOfKernelData` to derive the physical aperture, while the large-memory path uses a different layout calculation. Additional protected-memory configurations reserve distinct regions.

The source also rejects unsupported memory configurations and relies on the reported region being memory XNU can actually manage. Hanoip reserved-memory entries are not a complete physical-memory ownership map. No XT2135-2-specific memory map, firmware reservation map, or matching XNU build configuration is established.

### 5.5 CPU and SMP configuration

The ARM64 CPU code has configuration-dependent behavior for `USE_APPLEARMSMP`, `CONFIG_SPTM`, `XNU_MONITOR`, `HAS_RETENTION_STATE`, and other features. CPU startup and quiesce paths use platform callbacks and reset-handler state; these are not guaranteed merely because the processor implements ARMv8-A.

The pinned `board_config.h` enumerates Apple board profiles such as T6000, T6020, T8101, T8103, T8112, T8122/T8130, T8132, T6030, T6031, and VMAPPLE. It contains no Moto G60 or Qualcomm SM7150/SM7150-AC board profile. This does not prove a port is impossible; it confirms that a Moto-specific configuration/profile has not been supplied by the reviewed upstream file.

### 5.6 Build configuration is not interchangeable

The pinned `config/MASTER.arm64.iPhoneOS` template includes Apple-selected options such as `config_pmap_ppl`, embedded-kernel settings, signed-code enforcement and a platform-dependent `ARM_EXTRAS_BASE`. The master ARM64 configuration is a build template, not a universal configuration for arbitrary ARM64 devices.

The project has not established a suitable XT2135-2 configuration, nor the target's security-monitor arrangement, protected-memory model, CPU-family macros, or platform service implementations. A successful compile under an Apple template would not establish runtime compatibility.

## 6. Evidence comparison for XT2135-2

| Requirement | Exact XT2135-2 evidence | Hanoip / family clue | Current result |
|---|---|---|---|
| ARM64-capable CPU family | Snapdragon 732G is reported for the model; exact firmware entry state is not documented | Shared SoC source describes ARM64 CPU topology | Architecture relevance only; entry contract unknown |
| XNU `boot_args` producer | None located | Android kernel source and build records only | Unknown |
| SecureDT producer and schema | None located | Linux DTS and overlays | Unknown; formats/contracts not shown equivalent |
| `/chosen/dram-base` and `dram-size` | None located | Linux memory/reserved-memory descriptions | Unknown |
| SoC base and `arm-io` mapping | None located | Qualcomm SoC peripheral nodes | No matching XNU schema demonstrated |
| Interrupt controller | None confirmed for exact board revision | GICv3/PDC family source | Family clue only |
| Timer/timebase | None confirmed for exact board revision | Generic timer and timer block family source | Family clue only |
| CPU topology/SMP services | No exact firmware contract | Eight CPU nodes in shared family source | Family clue only |
| XNU board/build profile | None | Shared Android `hanoip` software identity | No Moto XNU profile in reviewed upstream board config |
| Memory ownership/configuration | None | Reserved-memory carveouts | Critical unknown |

## 7. Compatibility and patch decision

| Question | Decision |
|---|---|
| Does the source use generic ARM64 instructions? | Yes, alongside XNU and Apple platform contracts |
| Are some Apple-named early hooks stubbed for non-Apple ARM64 builds? | Yes; that only resolves those hooks |
| Does XNU require a particular boot-argument and SecureDT contract? | Yes, in the reviewed pinned path |
| Does the exact XT2135-2 firmware provide that contract? | Unknown |
| Does Hanoip Linux DTS prove XNU SecureDT compatibility? | No |
| Is the correct XNU compile-time board/security configuration known? | No |
| Has a concrete upstream source defect been demonstrated? | No |
| Is an executable source patch justified now? | **No** |

A compatibility patch should only be proposed after a source-level consumer expectation and an authoritative exact-target producer behavior are both known, and a specific semantic mismatch is demonstrated. A missing target driver, unknown firmware contract, or absent board profile is not by itself proof of an upstream XNU bug.

## 8. Next research milestone

The next source-only milestone should be a **SecureDT contract crosswalk**:

1. enumerate the exact pinned XNU SecureDT properties and node semantics consumed before and during early platform startup;
2. classify each as mandatory, optional, configuration-gated, or later-use;
3. compare only against public Hanoip source material while preserving its family-level confidence;
4. record which required properties have no corresponding target evidence;
5. keep any proposed implementation or source patch deferred until the exact target producer contract is documented.

This remains documentation and source review only. No device handoff construction, firmware modification, bootloader changes, partition operations, or phone testing is part of the milestone.

## 9. Pinned source references

- [ARM64 startup assembly](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/arm64/start.s)
- [ARM boot CPU initialization](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/arm/arm_init.c)
- [Platform Expert initialization](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/arm/pe_init.c)
- [Machine identification, interrupt and timer discovery](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/arm/pe_identify_machine.c)
- [ARM64 boot argument structure](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/pexpert/arm64/boot.h)
- [ARM64 board configuration](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/pexpert/pexpert/arm64/board_config.h)
- [ARM64 VM initialization](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/arm64/arm_vm_init.c)
- [ARM64 CPU configuration paths](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/arm64/cpu.c)
- [Apple ARM machine-routine stubs and family guards](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/arm/machine_routines_apple.c)
- [iPhoneOS ARM64 master configuration](https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/config/MASTER.arm64.iPhoneOS)

## 10. Conclusion

The audit clarifies the boundary: the instruction-level ARM64 foundation is only one layer. The selected XNU baseline also expects an Apple-defined boot ABI, SecureDT schema, machine/platform services, memory ownership contract, and a build configuration appropriate to the target.

The current XT2135-2 evidence does not establish those contracts. The source review found concrete integration requirements, but no narrowly defined upstream source bug. **Keep executable patches deferred; proceed with the SecureDT contract crosswalk and exact-model evidence work.**

*Project: MotoDarwin18*
