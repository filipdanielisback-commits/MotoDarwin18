# ARM64 XNU Platform Expert (pexpert) Review

**Research status:** source-orientation document; not an implementation.
**Project baseline:** `xnu-11215.1.10` (provisional; see [UPSTREAM.md](UPSTREAM.md)).
**Target:** Motorola Moto G60 XT2135-2 (`hanoip` family evidence only).

## 1. What pexpert does

The Platform Expert layer is XNU's platform-facing boundary for early boot services and machine-specific facilities. It is not a complete board-support package by itself. ARM64 startup also depends on architecture code under `osfmk/arm/` and `osfmk/arm64/`, machine routines, the VM/pmap implementation, interrupt and timer code, and later IOKit drivers.

A useful mental model is:

1. The platform's boot environment establishes a documented handoff contract.
2. ARM64 startup consumes the boot arguments and initializes the earliest machine state.
3. pexpert records platform state and exposes common kernel-facing services.
4. machine/architecture code brings up CPU, memory, interrupt, and timekeeping facilities.
5. IOKit and subsystem drivers enumerate and initialize devices after the kernel reaches the appropriate startup phases.

This separation matters: adding a pexpert file alone would not make the phone a supported XNU platform.

## 2. Startup and boot handoff

The ARM startup path calls `PE_init_platform(FALSE, args)` early in `arm_init()`. Later startup performs additional initialization and calls `PE_init_platform(TRUE, ...)`. The two calls represent different bootstrap phases; they must not be treated as a single board-init callback.

Relevant upstream source locations to inspect at the pinned revision:

- `osfmk/arm/arm_init.c` — ARM/ARM64 bootstrap sequence.
- `pexpert/arm/pe_init.c` — ARM platform-expert initialization.
- `pexpert/pexpert/arm64/boot.h` — ARM64 boot-argument structure.
- `pexpert/pexpert/pexpert.h` — public pexpert declarations.
- `pexpert/device_tree.h` and related device-tree implementation — platform description access.

The ARM64 `boot_args` structure is a contract with the preceding boot environment. Fields include physical/virtual memory information, kernel data boundary, boot video information, machine type, a device-tree pointer and length, command-line storage, flags, and memory-size information. A future loader would have to provide a structure matching the exact XNU revision's definition and semantics. A Linux device tree blob is not automatically a valid XNU handoff.

**MotoDarwin18 requirement:** define and independently validate a boot-handoff specification before any device-specific startup code is written. Do not guess addresses, flags, structure versions, or ownership of memory.

## 3. Device-tree and machine identification

The platform expert uses the boot-supplied device tree to obtain platform properties and machine-identification data. This is a description input, not proof that every described device is operational.

For Moto G60 research, the shared `hanoip` Android/Linux source tree is only family-level evidence. It does not yet establish the exact XT2135-2 board revision, memory map, enabled peripherals, firmware ownership, or interrupt routing.

**Required work before implementation:**

- establish the exact XT2135-2 board/revision mapping;
- identify which device-tree properties are required by the selected XNU source;
- define address-space and translation assumptions;
- distinguish immutable hardware facts from bootloader-provided descriptions;
- reject missing, contradictory, overlapping, or out-of-range memory regions;
- document who owns each reserved region and when ownership changes.

## 4. CPU and multiprocessor services

The pexpert interface declares platform CPU operations such as:

- `PE_init_cpu`
- `PE_cpu_start`
- `PE_cpu_halt`
- `PE_cpu_signal`
- `PE_cpu_signal_deferred`
- `PE_cpu_signal_cancel`
- `PE_cpu_machine_init`
- `PE_cpu_machine_quiesce`

These are interfaces, not ready-made Qualcomm implementations. Correct behavior depends on the ARM architecture, CPU topology, power/firmware coordination, interrupt delivery, and the exact SoC integration.

**MotoDarwin18 requirement:** initially document only the boot CPU and topology evidence. Secondary-CPU support remains unsupported until topology, startup protocol, coherency, per-CPU interrupt state, and safe shutdown behavior are all established.

## 5. Interrupt handling

The pexpert headers expose interrupt-related entry points, including external-interrupt handling and interrupt-handler installation. The actual controller implementation and interrupt routing are platform- and architecture-dependent.

The shared `hanoip` source contains GICv3 and Qualcomm PDC references. That is useful evidence, but it does not establish the exact controller programming model, interrupt ownership, routing, trigger configuration, or firmware handoff for this specific XT2135-2.

**MotoDarwin18 requirement:** produce an interrupt-controller evidence document before any driver code. It must distinguish distributor, redistributor, CPU interface, wakeup controller, and platform-specific routing. No register addresses or interrupt numbers should be invented from family-level evidence.

## 6. Timekeeping and timers

Kernel timekeeping requires a reliable counter source, frequency and conversion information, interrupt delivery, and well-defined behavior across CPU power states. ARM architectural timers may provide a starting point, but their availability and configuration are platform facts that must be verified.

**MotoDarwin18 requirement:** identify the counter source, frequency, access level, interrupt path, and suspend/resume behavior from trustworthy evidence. The previously observed 19.2 MHz timer-related entry in shared source material must not be mistaken for the architectural timer frequency.

## 7. Memory and MMIO

The platform must establish a correct physical memory map and safe mappings for device registers. This is a cross-layer responsibility involving boot arguments, device-tree descriptions, ARM translation tables, pmap, cache attributes, and machine routines.

**MotoDarwin18 requirement:** no physical address, MMIO size, cacheability attribute, or reserved-memory range is implementation-ready merely because it appears in a related device tree. Each value needs exact-model or otherwise authoritative evidence and a documented provenance trail.

## 8. Console, diagnostics, and optional services

The pexpert API includes console, boot-argument, debugger, panic, and configuration services. Some are optional or can be stubbed only where the selected XNU configuration explicitly permits it. A missing early console can make bring-up harder to diagnose, but a guessed UART mapping is not an acceptable shortcut.

For the first research milestone, prioritize a documented early diagnostic path. Treat display, touch, audio, Wi-Fi, Bluetooth, NFC, camera, and other end-user peripherals as later driver work, not prerequisites for understanding the pexpert boundary.

## 9. What pexpert does not solve

pexpert does not, by itself, provide:

- a Motorola bootloader or a compatible kernel loader;
- a complete Qualcomm board-support package;
- correct DRAM discovery and memory reservation;
- a complete interrupt-controller implementation;
- CPU power sequencing or firmware coordination;
- storage, display, touch, Wi-Fi, Bluetooth, audio, or camera drivers;
- proprietary iOS userland, services, firmware, or signing material;
- proof of iOS 18 application or system-framework compatibility.

## 10. Research conclusion

The first meaningful platform deliverable is not a new C source file. It is a revision-specific contract describing boot arguments, device-tree inputs, physical memory, CPU topology, interrupt-controller responsibilities, timer source, MMIO mapping rules, and the earliest diagnostic channel.

Only after that contract is evidence-backed should MotoDarwin18 propose a small, isolated pexpert adaptation. Any implementation must be tested on the host or in an appropriate emulator first. This research does not authorize or require changing the phone.

## References

- [Apple XNU source repository](https://github.com/apple-oss-distributions/xnu)
- [ARM64 startup: arm_init.c](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)
- [ARM pexpert initialization](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_init.c)
- [ARM64 boot arguments](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/arm64/boot.h)
- [pexpert public declarations](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/pexpert.h)
- [Apple Platform Expert API overview](https://developer.apple.com/documentation/kernel/driver_support/platform_expert)

**Revision note:** these paths are pinned to the project's provisional XNU tag. Before writing code, re-check each declaration and call site against the exact tag and record the source file's individual license.
