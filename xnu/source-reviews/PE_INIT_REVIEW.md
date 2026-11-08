# Source Review: `pexpert/arm/pe_init.c`

**Status:** provisional source-reading notes; exact comparison with `xnu-11215.1.10` remains pending.

## Role

This file implements ARM Platform Expert behavior. It is more than a single early-boot callback: it maintains platform state, consumes boot arguments and device-tree data, establishes device-tree access, identifies the machine, and provides console, panic, and IOKit-related services.

The reviewed source includes dependencies on pexpert declarations, boot definitions, device-tree APIs, machine routines, cache operations, and ARM-specific support. That dependency list is a useful signal: this file is a bridge between generic kernel startup and platform-specific facilities, not a self-contained Motorola board driver.

## `PE_init_platform(vm_initialized, args)`

The observed implementation has two phases.

### Early phase: `vm_initialized == FALSE`

On its first invocation, the implementation:

- marks the PE state initialized;
- stores the boot-argument pointer;
- takes the flattened device-tree pointer and length from the boot arguments;
- copies boot video metadata into PE state;
- initializes the secure device-tree access routines;
- calls `pe_identify_machine(boot_args)`;
- reads selected platform properties such as target type, model, debug state, and firmware identity when present;
- initializes early debug support.

This establishes a key contract: the incoming boot arguments and device-tree buffer must already be valid and remain accessible under the assumptions made by the kernel. A Motorola loader cannot simply pass an arbitrary Android DTB and assume the Apple PE implementation will accept it.

### Later phase: `vm_initialized == TRUE`

The observed implementation calls ARM interrupt and debug initialization helpers:

- `pe_arm_init_interrupts(args)`
- `pe_arm_init_debug(args)`

The argument at this stage is passed through from the caller. The precise meaning and required contents must be checked against the exact target revision and helper implementations.

**Important:** the boolean is a phase indicator in the observed implementation. It does not mean that all hardware is initialized, and it is not a generic instruction to initialize every device.

## Other responsibilities visible in this file

- Console setup and switching between video and serial output.
- Early IOKit initialization and configuration.
- Device-tree sliding/reinitialization when the tree's virtual mapping changes.
- Panic-log region discovery and management where the platform provides the relevant metadata.
- Debugger and panic-related state.
- Timebase callback plumbing.

These services carry Apple-platform assumptions. For example, panic-log setup expects a platform-defined region or particular device-tree properties. MotoDarwin18 must not invent those properties or map arbitrary memory as a panic buffer.

## Interfaces and dependencies to investigate

| Observed dependency | Why it matters to a new platform |
|---|---|
| `boot_args` | PE state is initialized from the boot handoff |
| `SecureDTInit`, `SecureDTLookupEntry`, `SecureDTGetProperty` | Device-tree structure, lifetime, validation, and property encoding |
| `pe_identify_machine` | Machine identity and platform selection |
| `pe_arm_init_interrupts` | Interrupt controller and routing integration |
| `pe_arm_init_debug` | Debug facilities and platform policy |
| `ml_io_map_*` | MMIO mapping and memory attributes |
| `PE_initialize_console`, `serial_init` call paths | Early diagnostic output |
| `InitIOKit`, `ConfigureIOKit` | Later device enumeration and configuration |

These are investigation targets, not a promise that all functions must be replaced for Moto G60.

## MotoDarwin18 implications

1. First define the boot-argument and device-tree contract.
2. Identify the minimum device-tree APIs available in the pinned XNU revision.
3. Separate early PE setup from later interrupt/debug initialization.
4. Determine which platform identity hooks are configurable and which are hard-coded to Apple platform assumptions.
5. Treat console, panic storage, and IOKit as independent capabilities; do not assume display or UART support.
6. Do not reuse Apple board-specific memory addresses, device-tree properties, or firmware assumptions.

The existing `hanoip` research is family-level Linux/Android evidence. It does not prove that the Motorola boot environment supplies the data or ownership model expected by this PE implementation.

## Safe next deliverable

Create an offline, host-testable schema for a proposed boot-handoff description. It should validate field presence, integer width, address arithmetic overflow, alignment, buffer lengths, and evidence provenance. It must not access a phone or attempt to construct a real boot handoff.

## References

- [Pinned XNU path: pexpert/arm/pe_init.c](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/pexpert/arm/pe_init.c)
- [Accessible source-browser view used for this provisional reading](https://fergofrog.com/code/codebrowser/xnu/pexpert/arm/pe_init.c.html)
- [ARM startup review](ARM_INIT_REVIEW.md)
- [ARM64 boot structure review](ARM64_BOOT_HEADER_REVIEW.md)

## Verification caveat

The accessible source-browser view is not proof of exact contents at `xnu-11215.1.10`. Confirm declarations, conditionals, and call order against the pinned source before turning any of these observations into code.
