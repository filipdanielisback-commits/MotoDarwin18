# MotoDarwin18 Platform Interface Matrix

This matrix translates the ARM64 XNU/pexpert boundary into research requirements for XT2135-2. It is intentionally a requirements map, not a claim that the interfaces have been implemented.

Status vocabulary:
- **Unknown** — not established by current evidence.
- **Documented** — source or hardware evidence recorded, but not independently validated.
- **Designed** — project interface contract written and reviewed.
- **Host-tested** — host-side tests pass; no target hardware conclusion.
- **Emulator-tested** — tested in an emulator that models the relevant behavior.
- **Device-tested** — verified on the exact target; not currently claimed for this project.

| Area | XNU-facing boundary / source area | Evidence needed for XT2135-2 | Current status | First safe deliverable |
|---|---|---|---|---|
| Boot handoff | ARM64 `boot_args`; `PE_init_platform`; `arm_init` | Exact boot-argument revision, entry conditions, address semantics, device-tree format and lifetime | Unknown | Written handoff contract and offline structure validator |
| Device description | pexpert device-tree accessors | Exact properties consumed by pinned XNU; compatible and address-cell conventions | Documented (family-level only) | Property inventory with provenance and required/optional classification |
| Physical memory | boot arguments, ARM pmap and VM startup | Exact DRAM ranges, reserved regions, secure/firmware carveouts, ownership and alignment | Unknown | Memory-map schema plus overlap/bounds tests |
| CPU identity/topology | ARM CPU discovery and machine routines | CPU IDs, affinity values, boot CPU, cluster topology, feature registers | Unknown | Evidence-backed CPU topology document |
| CPU lifecycle | `PE_init_cpu`, `PE_cpu_start`, `PE_cpu_halt`, signal/quiesce interfaces | Firmware coordination, start protocol, coherency, per-CPU setup and failure behavior | Unknown | Single-CPU-first design note; no startup code |
| Interrupt controller | pexpert interrupt APIs and ARM interrupt code | GIC distributor/redistributor/CPU interface, PDC routing, interrupt map and ownership | Documented (family-level only) | Interrupt topology diagram and source cross-reference |
| Timekeeping | ARM timer and machine timebase routines | Counter source, frequency, access level, interrupt routing, power-state behavior | Documented (incomplete family evidence) | Timer evidence table and unit-conversion tests |
| MMIO mapping | machine I/O mapping and pmap | Exact physical regions, lengths, access widths, cache/device attributes and security ownership | Unknown | Declarative MMIO inventory with bounds validation |
| Early console | pexpert console and serial hooks | Exact UART/controller, clock, pinmux, access policy and firmware state | Unknown | Console options assessment; retain unsupported status if evidence is absent |
| Panic/debug | pexpert panic/debug interfaces | Safe memory region, debugger policy, reset semantics, persistence rules | Unknown | Requirements-only note |
| IOKit enumeration | pexpert IOKit initialization and device drivers | Device matching model, bus topology, driver availability and dependency ordering | Unknown | Driver dependency map, beginning with no peripheral assumptions |
| Display/touch | IOKit/display/input stack | Exact panel, bridge/controller, touch controller, clocks, regulators and reset sequencing | Documented (candidate parts only) | Candidate-component provenance table |
| Storage | block/storage drivers and boot environment | Exact UFS/eMMC controller and device, partition contract, read-only discovery model | Documented (family-level only) | Storage architecture note; no partition operations |
| Power/thermal | platform power and thermal services | PMIC topology, regulator ownership, thermal sensors, firmware interfaces | Documented (family-level only) | Power-domain evidence map |
| Wireless/audio/camera | later IOKit and subsystem drivers | Exact components, firmware dependencies, bus topology and licensed driver sources | Unknown / partial | Driver feasibility notes only |

## Dependency order

1. **Boot contract and memory description** — without these, the kernel cannot safely establish its initial execution environment.
2. **CPU and exception environment** — establish architecture capabilities and the boot CPU assumptions.
3. **Interrupt and timekeeping model** — required for reliable scheduling, timers, and kernel progress.
4. **Minimal diagnostics** — provide a trustworthy way to observe failures.
5. **Secondary CPUs and basic buses** — only after the single-CPU foundations are understood.
6. **Storage and IOKit device enumeration** — separate from early kernel bring-up.
7. **Display, touch, wireless, audio, camera, power-management integration** — later and individually scoped.

This is a research dependency order, not a boot recipe.

## Evidence rules

- A shared `hanoip` source-tree reference is family-level evidence, not exact XT2135-2 proof.
- A SoC capability is not proof that the handset exposes or enables that capability.
- A device-tree node does not prove that firmware leaves the device available to XNU.
- A header declaration does not prove that an implementation is generic or usable on a new platform.
- A source file from another Apple platform must not be copied as a Motorola implementation.
- Never invent register addresses, interrupt IDs, timer frequencies, memory ranges, or boot flags.
- Mark a row **Implemented** only when project-authored code exists; mark it **Host-tested**, **Emulator-tested**, or **Device-tested** only after that exact level of validation.

## Immediate next research tasks

- Verify the exact pexpert and ARM startup declarations in `xnu-11215.1.10`.
- Cross-reference each pexpert API with its ARM implementation and call sites.
- Identify which machine routines are required before VM and interrupt initialization.
- Convert the boot-handoff and memory requirements into a machine-readable schema.
- Add offline tests for missing fields, overlapping memory ranges, invalid alignment, and evidence scope.

No XNU kernel build, emulator boot, or Moto G60 device test is claimed by this matrix.
