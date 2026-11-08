# Darwin/XNU Porting Plan — MotoDarwin18

**Target:** Motorola Moto G60 XT2135-2 (official Motorola documentation also identifies this model as moto g60 vision)  
**Status:** Planning and platform research; no kernel implementation or bootable image exists.  
**Principle:** Build evidence first, then small, testable software components. Do not treat a successful compile as proof of device compatibility.

## Project objective

Investigate whether a suitably selected, publicly available Darwin/XNU source baseline can be adapted to the ARM64 platform used by the XT2135-2. Keep the initial goal limited to a minimal XNU kernel bring-up. iOS 18 userland compatibility is a separate, much larger research track and is not implied by a kernel port.

## Current blockers

1. The public `hanoip` Android/Linux sources cover a shared Moto G40 Fusion/Moto G60 family. They do not yet prove which DVT board overlay matches a particular XT2135-2 unit.
2. The complete physical memory map, exact peripheral population, firmware interfaces, and boot handoff for the target revision remain unverified.
3. The XNU upstream baseline has not yet been pinned to an immutable tag and commit with a documented reason for choosing it.
4. No target-specific XNU platform expert, interrupt, timer, memory, or device drivers have been implemented.
5. A standard XNU source build does not itself produce a kernel that can boot on this Motorola phone.

## Phased implementation

### Phase 0 — Establish exact target and source provenance

- Record the exact commercial model, regulatory model identifier, device codename, and known board-family identifiers separately.
- Correlate public device-tree files and board overlays without assuming a model suffix selects a particular overlay.
- Select an immutable XNU source tag and record its license, commit, architecture support, and build prerequisites.
- Keep Apple's proprietary iOS components, restore images, signing material, and firmware outside this repository unless their use and redistribution are explicitly authorized.

**Exit criteria:** The device identity record and XNU baseline record are reviewed, sourced, and reproducible.

### Phase 1 — Reproducible source and host-build research

- Define a supported host environment and toolchain from the selected XNU release's own build documentation.
- Record dependencies and exact tool versions.
- Reproduce only the upstream build targets documented as supported by that release.
- Keep host-build results separate from Motorola-target build results.

**Exit criteria:** A clean, repeatable upstream build or a precise, documented list of blockers. A host build is not a device boot test.

### Phase 2 — Platform description and compatibility model

- Convert verified hardware evidence into a structured platform inventory.
- Define explicit unknowns for memory regions, interrupt topology, timers, storage, display, wireless, power, and firmware services.
- Map each XNU subsystem to required platform information and evidence.
- Avoid copying Android kernel drivers into XNU; their protocols and operating-system interfaces differ.

**Exit criteria:** Each required platform feature has a source-backed description, a confidence level, and a test plan.

### Phase 3 — Minimal platform bring-up design

- Design a narrow platform layer around documented XNU interfaces.
- Specify the expected handoff information conceptually: memory map, CPU state, device description, and console/debug facilities.
- Review architecture assumptions and upstream APIs before writing target-specific code.
- Keep all early work source-only and testable in host-side checks or an appropriate emulator.

**Exit criteria:** Reviewed interface designs and tests exist before hardware-dependent implementation begins.

### Phase 4 — Incremental kernel subsystem work

Work in dependency order, with independent review and tests for each area:

1. CPU/ARM64 assumptions and early kernel diagnostics.
2. Physical memory and virtual-memory description.
3. Interrupt-controller integration.
4. Clock and timer integration.
5. Console and basic platform services.
6. Storage and other peripherals, only after their exact hardware interfaces are verified.

Display, wireless, audio, sensors, camera, and power management are later projects. They are not prerequisites for proving the earliest kernel milestone.

**Exit criteria:** Each subsystem has evidence, implementation notes, and reproducible tests. No subsystem is marked supported merely because code compiles.

### Phase 5 — Compatibility assessment beyond the kernel

- Assess the boundary between XNU and the required user-space environment.
- Track proprietary Apple frameworks and services as separate compatibility gaps.
- Treat iOS 18 application and SpringBoard compatibility as long-term, optional research—not as an automatic result of kernel work.

## Milestones and honest status labels

Use only these labels in the compatibility matrix:

- **Unknown:** insufficient evidence.
- **Documented:** supported by source or reliable documentation, not tested.
- **Designed:** an interface or approach has been reviewed, not implemented.
- **Implemented:** code exists, but may not yet be tested.
- **Host-tested:** a reproducible test passed on a host.
- **Emulator-tested:** a reproducible test passed in a named emulator.
- **Device-tested:** a reproducible test passed on the exact target revision.
- **Unsupported:** evidence shows the requirement cannot currently be met.

A successful compile must never be described as a successful boot.

## Safety, integrity, and licensing

- Early milestones use source review, documentation, host-side tests, and emulation.
- This plan does not authorize bootloader changes, firmware modification, flashing, partition changes, or other device-altering procedures.
- Preserve upstream copyright and license notices. Review each imported file individually; the repository's MIT license does not override third-party licenses.
- Do not redistribute proprietary Apple or Motorola materials.
- Stop and document a blocker rather than guessing a register map, memory region, interrupt number, or firmware interface.

## Immediate next milestone

Complete Phase 0: establish the exact XT2135-2 identity against the shared `hanoip` source tree, then pin and review an appropriate XNU source baseline. Only after those two records are complete should we begin a first source-level implementation task.
