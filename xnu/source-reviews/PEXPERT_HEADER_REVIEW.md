# Source Review: `pexpert/pexpert/pexpert.h`

**Status:** provisional API inventory; exact comparison with `xnu-11215.1.10` remains pending.

## Role

This header declares Platform Expert services used by kernel and IOKit code. It describes a boundary between common kernel code and platform-specific implementations. A declaration is not an implementation: the presence of a function prototype does not mean a generic implementation exists or that it can operate on Qualcomm hardware.

## Interface groups observed

### Platform initialization

- `PE_init_platform(boolean_t vm_initialized, void *args)`

The call accepts a phase flag and opaque argument pointer. On ARM, the implementation interprets the early argument as a `boot_args *`. Later call sites may pass CPU data or `NULL`, depending on context. The exact call contract must be read together with `pe_init.c` and `arm_init.c`.

### CPU lifecycle and coordination

The header exposes declarations including:

- `PE_cpu_start`
- `PE_cpu_halt`
- `PE_cpu_down`
- `PE_cpu_signal`
- `PE_cpu_signal_deferred`
- `PE_cpu_signal_cancel`
- `PE_cpu_machine_init`
- `PE_cpu_machine_quiesce`
- `PE_init_cpu`

These APIs indicate platform participation in CPU startup, shutdown, signaling, and per-CPU setup. They do not specify the Qualcomm firmware protocol. That protocol, CPU topology, coherency behavior, and interrupt delivery must be independently established before any Motorola implementation is designed.

### Interrupt and performance-monitor hooks

The observed ARM declarations include:

- `PE_handle_ext_interrupt`
- performance-monitor interrupt handler installation and enablement APIs

The actual controller and interrupt routing remain architecture/platform-specific. MotoDarwin18's family-level GICv3/PDC evidence is not sufficient to implement these functions.

### Debug, panic, and console services

The header also declares services for debugger entry, debugger availability, panic debugging, polling input, panic hooks, and related facilities. These should be considered optional platform capabilities until their dependencies and configuration guards are understood.

### Boot and random-seed helpers

The header exposes boot-related declarations and a random-seed accessor. The latter reads a device-tree property and modifies the tree as part of its contract. This is a reminder that device-tree APIs can have side effects; they are not all simple read-only getters.

## Design lessons for MotoDarwin18

- Keep interface declarations separate from implementation claims.
- Trace each API to its definition and call sites in the pinned tree.
- Record whether an API is mandatory, optional, configuration-gated, or Apple-platform-only.
- Avoid implementing CPU lifecycle hooks until firmware and topology behavior are known.
- Avoid fake success stubs for interrupts, timers, CPU power, or memory services. A stub that appears to succeed can hide a missing platform capability.
- Do not copy Apple-specific functions simply because the header declares them.

## Initial interface classification

| Interface family | Research priority | Current Motorola status |
|---|---:|---|
| Boot/PE initialization | Highest | Unknown |
| CPU initialization/topology | High | Unknown |
| CPU start/stop/signaling | Later; requires firmware contract | Unknown |
| Interrupt handling | Highest after boot contract | Family-level evidence only |
| Debug/console | Useful for diagnostics | Unknown |
| Panic persistence | Optional later service | Unknown |
| Random seed/device-tree access | Security-sensitive contract review | Unknown |
| Performance monitoring | Later optimization/debug work | Unknown |

## References

- [Pinned XNU path: pexpert/pexpert/pexpert.h](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/pexpert/pexpert.h)
- [Accessible upstream header view](https://github.com/apple/darwin-xnu/blob/main/pexpert/pexpert/pexpert.h)
- [PE initialization review](PE_INIT_REVIEW.md)

## Verification caveat

This inventory is based on accessible upstream header content and is provisional. Verify exact prototypes, typedefs, guards, and comments in the pinned tag before implementing or relying on ABI details.
