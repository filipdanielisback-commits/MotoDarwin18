# Kernel Handoff Requirements — Research Checklist

**Status:** Conceptual checklist; no device-specific handoff contract is defined.

## Purpose

A loader and kernel need an agreed boundary describing the execution environment and information available to the kernel. This document lists categories to research from authoritative documentation. It intentionally does not specify operational boot steps, memory addresses, register values, or device-modification procedures.

## Information categories

| Category | Questions to resolve | Moto G60 status |
|---|---|---|
| Execution context | What architecture and execution state does the kernel expect? | Unknown |
| Firmware contract | Which documented services or interfaces exist at the boundary? | Unknown |
| Kernel image | Which image format, metadata, and compatibility identifiers are required? | Not selected |
| Memory description | How are available and reserved memory regions represented? | Unknown |
| Platform description | How are board identity and hardware resources described? | Unknown |
| Interrupt and timer context | What platform facts must be available to kernel initialization? | Unknown |
| Display or diagnostic context | Is any early diagnostic facility documented and supported? | Unknown |
| Ownership and lifetime | Which component owns each buffer or data structure, and for how long? | Unknown |
| Validation status | What checks are documented, and which component is responsible for them? | Unknown |
| Error reporting | How are unsupported or inconsistent conditions represented? | Not defined |

## Requirements for a future written contract

Any proposed contract must:

1. Cite the exact kernel source revision and the documentation that defines its expectations.
2. Distinguish standard architecture requirements from vendor-specific extensions.
3. Define data ownership and lifetime without relying on undocumented assumptions.
4. Specify versioning and how incompatible versions are recognized.
5. Explain how incomplete or contradictory platform information is reported.
6. Record security and licensing constraints for any external components.
7. State which target-specific details remain unverified.

## Evidence rules

- An ARM64 CPU does not imply a particular firmware interface.
- Another device using a related Qualcomm platform is not proof of the Moto G60's firmware behavior.
- A public XNU source tree does not automatically document every proprietary platform interface.
- A conceptual checklist is not a working loader or kernel handoff implementation.

## Current conclusion

No supported loader-to-XNU handoff for Motorola Moto G60 XT2135-2 has been established. All entries remain research questions until backed by exact, reliable evidence.
