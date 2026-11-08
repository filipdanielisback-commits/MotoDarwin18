# ARM64 Platform Porting Checklist

This checklist is an evidence gate for future MotoDarwin18 platform work. It does not describe how to alter the phone or its boot configuration.

## Gate 0 — Source baseline

- [ ] Confirm the exact upstream XNU tag and peeled commit.
- [ ] Re-open every relevant source file at that exact revision.
- [ ] Record per-file license and provenance before copying or modifying anything.
- [ ] Identify build configuration and supported ARM64 assumptions.
- [ ] Record any differences between the pinned tag and newer upstream code.

## Gate 1 — Boot contract

- [ ] Identify the exact ARM64 `boot_args` layout and revision.
- [ ] Document entry address, execution level, exception state, and CPU state requirements from authoritative source material.
- [ ] Define physical and virtual address semantics.
- [ ] Define the device-tree format, pointer lifetime, and memory ownership.
- [ ] Define kernel image, kernel data, and reserved-memory boundaries.
- [ ] Validate the proposed handoff description offline.
- [ ] Reject unknown or contradictory fields rather than supplying guessed defaults.

## Gate 2 — Memory and translation

- [ ] Establish exact physical DRAM ranges for the target revision.
- [ ] Identify reserved, secure, firmware, peripheral, and crash-log regions.
- [ ] Check alignment, overlap, overflow, and address-width constraints.
- [ ] Document MMIO ranges separately from RAM.
- [ ] Establish memory attributes and cache-coherency assumptions.
- [ ] Cross-reference boot-time mappings with ARM pmap expectations.

## Gate 3 — CPU and interrupts

- [ ] Establish CPU identity and affinity mapping.
- [ ] Record required ARM architectural features from reliable evidence.
- [ ] Document boot CPU assumptions.
- [ ] Identify interrupt controller components and firmware ownership.
- [ ] Document interrupt routing and trigger/polarity data.
- [ ] Establish timer interrupt delivery and per-CPU initialization requirements.
- [ ] Keep secondary CPU support out of scope until its lifecycle contract is independently documented.

## Gate 4 — Timekeeping and diagnostics

- [ ] Identify the architectural counter and its actual frequency.
- [ ] Document access permissions and timer interrupt routing.
- [ ] Identify any power-state effects on counter continuity.
- [ ] Evaluate a minimal diagnostic console using evidence, not guessed UART addresses.
- [ ] Document panic and reset behavior without assuming persistent storage.

## Gate 5 — Project-authored implementation readiness

- [ ] Each proposed interface has a source reference and rationale.
- [ ] Each hardware constant has exact-model evidence.
- [ ] Generic code is separated from platform-specific code.
- [ ] New code has a clear license and copyright header.
- [ ] Host-side tests cover parsers, schemas, arithmetic, bounds, and failure paths.
- [ ] Tests do not require a connected phone or modify device state.
- [ ] Emulator tests, if any, state exactly which hardware behavior is modeled.
- [ ] Status labels distinguish designed, implemented, host-tested, emulator-tested, and device-tested.

## Explicit non-goals for this research phase

- No bootloader unlocking or bypass.
- No firmware or partition modification.
- No flashing, erasing, formatting, or booting experimental images.
- No use or redistribution of proprietary Apple firmware, restore images, keys, or user data.
- No claim of iOS 18 userland compatibility from a successful XNU source build.

A checked box means the corresponding evidence or review exists in the repository. It does not imply that the phone has been modified or tested.
