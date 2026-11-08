# XNU Early Platform Service Dependency Inventory

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2  
**XNU baseline:** `xnu-11215.1.10`  
**Pinned commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`  
**Status:** Source-derived dependency inventory; no target implementation or boot validation.

## 1. Purpose

Inventory the early ARM64 startup services used by the selected XNU baseline and classify each dependency as:

- **Architecture-generic:** a kernel/ARM64 concept, but still requiring a correct implementation and CPU/platform state.
- **Apple-specific:** an Apple XNU/Platform Expert convention, interface, or platform integration point.
- **Platform-specific:** depends on concrete board hardware, firmware, or platform description.
- **Configuration-dependent:** compiled or invoked only under particular build flags or runtime conditions.
- **Unresolved:** the available source review does not establish the full contract.

A single dependency can have more than one classification. “Architecture-generic” does not mean “already supported by Snapdragon” or “available from Android firmware”.

## 2. Scope and evidence rules

The call sequence and service names below were checked in the pinned files:

- `osfmk/arm/arm_init.c` — blob `f96a24595c2abd134f7af2526b88808514d61252`
- `pexpert/arm/pe_init.c` — blob `6a3fce5aa2c496481915ec2511379b0d6935a413`
- `pexpert/pexpert/arm64/boot.h` — blob `eab75014f92bb6475bdd4225b6e074ad82652ae5`
- `osfmk/arm64/arm_vm_init.c` — blob `0dbbd9103f131faab9e6c1ccbea3c0fa9ae46e5c`

See [Pinned XNU Source Verification](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md) for the source baseline and prior boot-argument trace.

The inventory describes what this source calls or consumes. It does not claim all services are mandatory in every build configuration, nor does it define a supported third-party platform implementation.

Evidence on the Motorola side is classified as:
- **Family clue:** shared hanoip / SDMMAGPIE Android/Linux source evidence.
- **Exact-model evidence:** directly tied to XT2135-2.
- **Unknown:** no adequate target-specific evidence is recorded.

## 3. Startup sequence overview

The following is a dependency-oriented summary of the pinned `arm_init()` boot-CPU path. Conditional blocks and configuration-specific code are omitted from the simplified sequence; this is not a complete execution trace for every XNU build.

1. Copy the incoming `boot_args` into `const_boot_args` and establish `BootArgs`.
2. Initialize boot CPU data with `cpu_data_init()`.
3. Call early Platform Expert initialization: `PE_init_platform(FALSE, args)`.
4. Apply ARM64 timer and Apple platform register setup where enabled.
5. Parse CPU topology and establish boot CPU identity and stacks.
6. Establish the bootstrap thread and current-thread context.
7. Run `cpu_bootstrap()`, `rtclock_early_init()`, and `kernel_startup_bootstrap()`.
8. Initialize timer-call, CPU and processor infrastructure.
9. Read selected device-tree properties, including `/chosen/dram-base` and `dram-size`, then initialize VM with `arm_vm_init()`.
10. Initialize serial/debug output and the console.
11. Call later Platform Expert initialization: `PE_init_platform(TRUE, &BootCpuData)`.
12. Initialize timebase, CPU Platform Expert services and FIQ context.
13. Continue into `machine_startup(args)`.

The order matters. For example, the early Platform Expert path initializes SecureDT before later code reads mandatory device-tree properties, while the later Platform Expert call performs interrupt and debug setup.

## 4. Dependency inventory

| Service / interface | Role in pinned source | Classification | Moto G60 evidence | Gap / status |
|---|---|---|---|---|
| Incoming ARM64 entry state | Supplies a valid boot CPU context and accessible boot arguments to startup | Architecture-generic + platform-specific | ARM64-capable SoC family only | Exact firmware entry contract unknown |
| `boot_args` producer | Supplies revision, version, memory bases/sizes, device tree and related metadata | Apple-specific ABI + platform-specific producer | No Motorola producer contract recorded | Not demonstrated |
| `cpu_data_init` | Initializes XNU boot CPU data structures | Architecture-generic kernel service | No XNU target implementation | Requires correct CPU/platform integration |
| `PE_init_platform(FALSE, args)` | Captures boot args, device-tree pointer/length and video fields; initializes SecureDT; identifies machine | Apple-specific + platform-specific | Linux DTS family clues only | No Motorola Platform Expert implementation |
| `SecureDTInit` / SecureDT queries | Parses and queries the early device tree; startup reads properties from it | Apple-specific interface + platform description | Shared Linux DTS exists | Format/property/ownership compatibility unknown |
| `pe_identify_machine` | Identifies the XNU machine from boot arguments/platform information | Apple-specific + platform-specific | XT2135-2 identity documented, but no XNU machine mapping | Unknown |
| CPU topology parsing | Establishes boot CPU number and topology | Architecture-generic concept + platform-specific data | Shared source describes an eight-core family topology | Exact-model topology and firmware description not confirmed |
| ARM64 exception/interrupt stacks | Provides per-CPU stack context for exceptions and interrupts | Architecture-generic | No target XNU CPU setup | Implementation absent |
| `configure_timer_apple_regs` | Programs Apple-specific timer-related registers in this build path | Apple-specific + configuration-dependent | No evidence these Apple registers exist on Qualcomm platform | Not transferable by assumption; unresolved |
| `wfe_timeout_configure/init` | Configures wait-for-event timeout behavior | Architecture-generic mechanism + implementation-specific | No XNU implementation for target | Requires source/configuration audit |
| `configure_misc_apple_boot_args` | Applies Apple-specific boot-argument-related configuration | Apple-specific + configuration-dependent | No corresponding Motorola contract | Unresolved |
| `configure_misc_apple_regs` | Applies Apple platform register configuration | Apple-specific + configuration-dependent | No evidence of matching register interface | Not transferable by assumption |
| `cpu_bootstrap` | Performs early CPU-machine initialization | Architecture-generic interface + machine-specific implementation | Snapdragon family evidence only | Required machine routines not implemented |
| `rtclock_early_init` | Establishes early real-time clock/timebase services | Architecture-generic service + platform-specific clock source | Generic timer listed in shared DTS | Exact timer source, frequency contract and XNU integration unknown |
| `kernel_startup_bootstrap` | Begins generic kernel startup bootstrap | Generic XNU kernel service | No XNU target port | Depends on successful earlier machine/VM setup |
| `timer_call_init` | Initializes timer callout infrastructure | Generic XNU kernel service | No target timer backend | Depends on working clock/timebase and interrupt path |
| `cpu_init` | Initializes CPU subsystem state | Generic XNU interface + architecture/platform implementation | ARM64 family only | Required machine implementation absent |
| `processor_bootstrap` | Initializes processor/scheduler-side structures | Generic XNU kernel service | No target implementation | Depends on CPU and interrupt/timer services |
| `PE_parse_boot_argn` / `PE_get_default` | Reads boot options and platform defaults | Apple Platform Expert service | No producer/parser contract for target | Command-line format and property/default source unknown |
| `SecureDTLookupEntry("/chosen")` | Looks up chosen node for early platform data | Apple-specific API + platform-description contract | Shared Linux DTS family evidence; no exact handoff tree | Required chosen-node properties not established |
| `dram-base` / `dram-size` properties | Pinned ARM startup reads both properties and panics if absent | Apple-specific consumer contract + platform-specific data | Shared DTS carveouts, not an exact complete memory map | Critical missing property/semantics evidence |
| `arm_vm_init` | Builds XNU ARM64 VM mappings from boot arguments and memory information | Architecture-generic VM concept + platform-specific memory contract | No exact physical memory map | Critical gap |
| `serial_init` | Enumerates/initializes serial output for debug | Platform-specific + configuration-dependent | No exact target debug UART handoff or XNU driver | Unknown; not proven available |
| `PE_create_console` / `PE_init_printf` | Sets up Platform Expert console and print output | Apple-specific service + platform-specific backend | No target console implementation | Unknown |
| `cpu_machine_idle_init` | Initializes machine idle behavior | Architecture-generic interface + platform-specific power/idle implementation | Shared PMIC/thermal clues only | No XNU idle/power implementation |
| `PE_init_platform(TRUE, &BootCpuData)` | Later Platform Expert phase calls interrupt and debug initialization | Apple-specific API + platform-specific implementation | GICv3/PDC are family-level clues | No XNU interrupt/debug backend |
| `pe_arm_init_interrupts` | Initializes ARM interrupt handling from platform information | Architecture-specific + platform-specific | Shared SDMMAGPIE DTS describes GICv3/PDC | Exact routing/ownership and XNU integration unknown |
| `pe_arm_init_debug` / `pe_arm_debug_init_early` | Initializes platform debug facilities | Apple-specific + platform-specific | No exact target debug interface | Unknown |
| `ml_map_cpu_pio` | Maps CPU-related platform I/O used by this build | Apple-specific machine-layer interface + platform-specific | No verified target mapping | Unknown |
| `cpu_timebase_init` | Initializes per-CPU timebase | Architecture-specific service + platform-specific clock | Generic timer family clue only | Exact implementation and calibration unknown |
| `PE_init_cpu` | Initializes CPU-specific Platform Expert services | Apple-specific + platform-specific | No Motorola implementation | Unknown |
| `fiq_context_init` | Initializes FIQ context | ARM-specific + platform-specific | No target XNU implementation | Unknown |
| `machine_startup` | Transfers into later machine/kernel startup | Generic XNU flow + machine-specific dependencies | No target machine layer | Not reachable until prior dependencies are satisfied |

## 5. High-priority dependency groups

### A. Entry contract and early Platform Expert

**Critical.** The kernel must receive a compatible entry context and boot-argument representation. The early `PE_init_platform(FALSE, args)` path captures the device-tree pointer and length, initializes SecureDT and calls machine identification.

Moto evidence does not establish an Apple-compatible `boot_args` producer, a SecureDT-compatible tree, or an XNU machine identifier.

### B. Device-tree and memory contract

**Critical.** The pinned `arm_init.c` reads `dram-base` and `dram-size` from `/chosen`, then passes boot arguments into `arm_vm_init()`. The VM code uses `virtBase`, `physBase`, `memSize`, `memSizeActual` and `topOfKernelData`.

The shared hanoip source tree has useful reserved-memory and SoC descriptions, but does not prove a complete XT2135-2 memory map or the precise device-tree values/semantics this XNU consumer expects.

### C. CPU, interrupt and timer services

**Critical for sustained kernel execution.** The startup flow establishes CPU data, topology, stacks, timebase and interrupt infrastructure. Shared family sources suggest GICv3/PDC and an Arm generic timer, but Linux declarations do not implement XNU's machine-layer interfaces.

The Apple-specific register routines in the pinned XNU path must be treated as Apple platform integration, not as generic ARM64 setup. No Qualcomm equivalent is assumed.

### D. Console and diagnostics

**Important for observability.** XNU initializes serial and console services in the startup path. No exact XT2135-2 serial/debug path or XNU driver is established. A lack of console output would also make later failures harder to distinguish, so this remains a major research dependency even if not a fundamental ABI field.

### E. Later device services

Display, UFS, wireless, Bluetooth, audio, sensors, camera and power management matter for a useful device environment, but they should not be conflated with the minimum early startup contract. Their existence in Android/Linux sources does not establish an XNU driver or user-space compatibility.

## 6. What the inventory says about Moto G60

### Family-level clues already recorded

- Shared SDMMAGPIE source describes GICv3 and Qualcomm PDC.
- An Armv8 generic timer is listed at 19.2 MHz.
- The shared tree describes CPU nodes and several memory reservations.
- Hanoi overlays describe UFS, display, touch, wireless and power components.

### Exact-model facts still missing

- XT2135-2 board revision mapped to a specific overlay.
- Firmware-to-kernel entry-state contract.
- Producer format and semantics for boot arguments.
- Exact physical RAM banks and reserved-region ownership.
- Exact device-tree handoff format, required properties, pointer lifetime and trust model.
- Exact interrupt routing and firmware ownership.
- Exact timer source/configuration and XNU timebase integration.
- Target debug/console interface.
- A Motorola implementation of the required XNU Platform Expert and machine-layer services.

## 7. Research priority and exit criteria

| Priority | Research task | Exit condition |
|---:|---|---|
| 1 | Trace all early Platform Expert calls and conditional paths | Call graph and build-configuration caveats documented |
| 2 | Audit machine identification and required device-tree properties | Required property names, consumers and unknown producer contract recorded |
| 3 | Audit ARM64 CPU entry assumptions and generic-vs-Apple-specific routines | Every early routine classified with source references |
| 4 | Audit memory ownership and VM input contract | No unknown target memory values represented as facts |
| 5 | Map interrupt/timebase service requirements | Required abstractions and family-level evidence separated |
| 6 | Inventory console/debug dependencies | Target-specific unknowns and evidence requests documented |

No device boot handoff, bootloader change, firmware modification, or device-altering test is part of these milestones.

## 8. Source references

All XNU references below are pinned to `xnu-11215.1.10`:

- [ARM startup — `osfmk/arm/arm_init.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)
- [ARM Platform Expert initialization — `pexpert/arm/pe_init.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_init.c)
- [ARM64 boot arguments — `pexpert/pexpert/arm64/boot.h`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/arm64/boot.h)
- [ARM64 VM initialization — `osfmk/arm64/arm_vm_init.c`](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm64/arm_vm_init.c)
- [Pinned source verification report](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md)
- [Boot ABI compatibility gap analysis](BOOT_ABI_COMPATIBILITY_GAPS.md)
- [Hanoip / SDMMAGPIE platform evidence](../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
- [Device unknowns register](DEVICE_UNKNOWNS.md)

## 9. Conclusion

The early XNU startup path depends on a combination of generic ARM64 mechanisms, Apple-specific Platform Expert and machine-layer services, and platform-specific firmware/hardware information.

Moto G60 family sources provide some encouraging clues about the underlying SoC peripherals, but they do not establish the exact firmware contract or supply the required XNU services. The largest blockers remain the boot entry contract, SecureDT/device-tree semantics, memory ownership, machine identification, interrupt/timebase integration, and Platform Expert implementation.

**Overall status: dependency inventory documented; target compatibility and implementation remain unproven.**

*Project: MotoDarwin18*


## Follow-up: Secure Device Tree requirements

See [Secure Device Tree Requirements Analysis](SECURE_DEVICE_TREE_REQUIREMENTS.md) for the pinned SecureDT binary layout, early property consumers, mandatory `/chosen` DRAM properties, and the unresolved distinction between XNU SecureDT records and standard Linux FDT.
