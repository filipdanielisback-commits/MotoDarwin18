# Source Review: `osfmk/arm/arm_init.c`

**Status:** provisional control-flow review; exact comparison with `xnu-11215.1.10` remains pending.

## Role

`arm_init()` is the boot-CPU startup routine. It connects the incoming boot arguments, early Platform Expert setup, ARM64 machine initialization, virtual memory, timer and CPU services, diagnostics, and later machine startup.

This file demonstrates why a platform port cannot be implemented solely by adding a new `pe_init.c`: the ARM architecture startup sequence itself has assumptions about boot arguments, CPU state, memory, timers, interrupts, and machine routines.

## Observed startup phases

The accessible source shows this broad ordering:

1. Rebase/sign the kernel image as configured.
2. Preserve/copy boot arguments and establish the global `BootArgs` pointer.
3. Initialize boot CPU data.
4. Call `PE_init_platform(FALSE, args)` for early Platform Expert setup.
5. Configure ARM64-specific architectural state and page-size policy.
6. Parse CPU topology and identify the boot CPU.
7. Establish boot CPU data structures and bootstrap thread state.
8. Initialize early clock/timer support and begin kernel bootstrap.
9. Initialize timer callouts, CPU and processor state.
10. Read DRAM information from the platform description and initialize ARM virtual memory.
11. Establish diagnostic output and console state.
12. Call `PE_init_platform(TRUE, &BootCpuData)` for later platform services.
13. Initialize debug, timebase, per-CPU, interrupt-related, and machine startup services.

The exact sequence is configuration-dependent. Conditional compilation, architecture features, security configuration, hibernation, and target-specific hooks alter the path.

## The two PE initialization calls

The early call occurs before full VM initialization and provides the boot-argument structure. The later call occurs after major CPU/VM/console setup and passes boot CPU data in the observed boot path.

This aligns with the two branches seen in the ARM PE implementation:

- early branch: initialize device-tree access and identify the machine;
- later branch: initialize ARM interrupt and debug support.

Do not infer that the boolean alone fully describes readiness. The caller's sequence and the implementation's dependencies jointly define the contract.

## Platform dependencies exposed by this file

| Dependency | Why it matters |
|---|---|
| `boot_args` | Kernel entry contract |
| `PE_init_platform` | Early and later PE setup |
| CPU topology parsing | Boot CPU identity and later SMP assumptions |
| `args->memSize` and DRAM metadata | Page-size and memory initialization decisions |
| Device-tree lookup | DRAM and platform properties |
| ARM timer/timebase | Timekeeping and scheduler progress |
| `PE_init_cpu` | Platform CPU initialization hook |
| `serial_init` and console setup | Early diagnostic path |
| machine startup | Transition from architecture bootstrap to broader kernel startup |

## Implications for MotoDarwin18

- Establish the boot contract before writing any platform code.
- Treat DRAM metadata as authoritative only after exact-model provenance and semantics are established.
- Do not assume Apple-specific register setup functions have Motorola equivalents or can be reused.
- CPU topology, timer frequency, interrupt routing, and console hardware require independent evidence.
- A successful host-side parser test does not validate the ARM startup environment.
- No source-level observation here establishes that this XNU revision can boot on Snapdragon 732G.

## Safe next deliverable

Create a dependency graph and host-side tests for the abstract boot manifest. The tests should validate structure and arithmetic only; they must not build a kernel image or interact with a connected phone.

## References

- [Pinned XNU path: osfmk/arm/arm_init.c](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/osfmk/arm/arm_init.c)
- [Accessible upstream ARM startup source](https://github.com/apple-oss-distributions/xnu/blob/main/osfmk/arm/arm_init.c)
- [PE initialization review](PE_INIT_REVIEW.md)
- [ARM64 boot header review](ARM64_BOOT_HEADER_REVIEW.md)
