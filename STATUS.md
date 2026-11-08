# MotoDarwin18 — Project Status

**Last updated:** 2026-11-08  
**Target device:** Motorola Moto G60 XT2135-2  
**Project stage:** Documentation and feasibility research

> **Important:** MotoDarwin18 does not currently contain a working XNU kernel port, loader implementation, bootable image, or iOS 18 implementation. No Moto G60 boot or hardware compatibility is claimed.

## 1. At a glance

| Area | Current status | Notes |
|---|---|---|
| Project foundation | Documented | Repository scope, contribution guidance, and license boundaries exist |
| Device inventory | Initial documentation | Exact-model details and board-level facts still need stronger primary evidence |
| Snapdragon 732G research | Initial documentation | SoC-level capabilities are separated from handset-specific facts |
| XNU source research | Documentation scaffold | Upstream repository identified; exact immutable baseline not selected |
| XNU implementation | Not started | No Moto G60 patches, drivers, or kernel configuration |
| Loader research | Documentation scaffold | Conceptual architecture and handoff questions recorded |
| Loader implementation | Not started | No executable loader or firmware integration |
| Compatibility testing | Not started | No device boot or subsystem validation |
| iOS 18 compatibility | Long-term research target only | No proprietary iOS components or working iOS 18 environment |

## 2. Completed repository work

### Project and research documentation

- [x] Project README and scope.
- [x] MIT license for original project material, with third-party license boundaries documented.
- [x] Contribution guidance and repository ignore rules.
- [x] Research roadmap and architecture overview.
- [x] Hardware inventory for the Moto G60 XT2135-2.
- [x] Device unknowns register.
- [x] General platform requirements.
- [x] Snapdragon 732G platform requirements checklist.
- [x] Build environment notes.
- [x] XNU baseline and source provenance notes.
- [x] Research log, references, glossary, and experiment policy.
- [x] Requirements and safe, read-only ADB/Fastboot diagnostic documentation.

### XNU research area

- [x] `xnu/README.md` — directory purpose and research workflow.
- [x] `xnu/UPSTREAM.md` — upstream source record; exact commit remains unselected.
- [x] `xnu/COMPATIBILITY_MATRIX.md` — initial subsystem evidence matrix.
- [x] `xnu/patches/README.md` — patch review and provenance rules.
- [x] `xnu/patches/PATCH_TEMPLATE.md` — proposal template.
- [x] `xnu/files/README.md` — source file provenance requirements.
- [x] `xnu/scripts/README.md` — source-only validation scope.

### Loader research area

- [x] `xnuloader/README.md` — purpose, boundaries, and research sequence.
- [x] `xnuloader/ARCHITECTURE.md` — conceptual component architecture.
- [x] `xnuloader/HANDOFF_REQUIREMENTS.md` — conceptual kernel handoff checklist.
- [x] `xnuloader/COMPATIBILITY.md` — initial target compatibility register.
- [x] `xnuloader/src/README.md` — source entry criteria.
- [x] `xnuloader/include/README.md` — interface declaration policy.
- [x] `xnuloader/scripts/README.md` — source-only script scope.

### Other repository areas

- [x] `research/` and `research/soc/` documentation scaffolds.
- [x] `tests/README.md` test area scaffold.
- [x] `tools/README.md` tools area scaffold.

A checked item means the documentation or scaffold exists; it does not mean the corresponding technical capability is implemented or validated.

## 3. Current open research questions

### Device and SoC

- [ ] Confirm all hardware details against reliable sources for the exact XT2135-2 variant.
- [ ] Identify exact board-level components and controller models where public evidence exists.
- [ ] Establish the handset's physical memory map and reserved regions from authoritative evidence.
- [ ] Identify the interrupt controller, timer configuration, and platform description.
- [ ] Establish documented firmware interfaces and the actual platform handoff environment.
- [ ] Identify display, storage, USB, audio, wireless, power, thermal, and sensor dependencies.

### XNU

- [ ] Review candidate Apple XNU release tags and commits.
- [ ] Select and record an immutable upstream commit only after source and license review.
- [ ] Compare the selected revision's architecture assumptions with the platform requirements.
- [ ] Identify which XNU platform components are relevant to the target, based on evidence.
- [ ] Keep the compatibility matrix updated as claims are verified.

### Loader

- [ ] Determine whether authoritative public documentation describes the target firmware environment.
- [ ] Establish the kernel-side information requirements for the exact selected XNU revision.
- [ ] Determine whether a documented, supportable loader-to-kernel interface is feasible.
- [ ] Review all prospective dependencies for provenance and licensing.
- [ ] Keep any future validation limited to safe, isolated, non-device source-level work unless a separate safety review establishes otherwise.

### Testing and reproducibility

- [ ] Define source-level checks and expected results.
- [ ] Document a reproducible, isolated research environment.
- [ ] Establish a test report format that records environment, versions, evidence, and limitations.
- [ ] Do not describe source checks as device validation.

## 4. Next milestones

| Order | Milestone | Completion condition |
|---:|---|---|
| 1 | Reconcile roadmap and status | Roadmap reflects the documentation already present and separates it from implementation work |
| 2 | Strengthen device evidence | Exact-model facts have primary sources or remain explicitly unknown |
| 3 | Select XNU baseline | Immutable upstream commit, rationale, and license review are recorded |
| 4 | Complete platform gap analysis | Each relevant subsystem has evidence, unknowns, and a justified status |
| 5 | Review loader feasibility | Firmware and kernel interface assumptions are documented from authoritative sources |
| 6 | Define source-only validation | Tests are reproducible, non-destructive, and accurately scoped |

These milestones are research goals, not a prediction that a port will be technically or legally possible.

## 5. Status vocabulary

Use consistent terms in issues, commits, and documentation:

- **Documented:** a written explanation or checklist exists.
- **Verified:** a claim is supported by a reliable primary source or repeatable test, with scope stated.
- **Observed:** directly seen, but not necessarily independently reproduced.
- **Inferred:** a reasoned interpretation that is not directly established.
- **Unknown:** adequate evidence is not currently available.
- **Implemented:** project-authored code exists.
- **Validated:** a defined test passed; the test environment and limitations are recorded.
- **Not supported:** evidence establishes that the requirement cannot be met.

Do not use “working”, “bootable”, “supported”, or “compatible” without specific evidence for the exact claim.

## 6. Licensing, safety, and integrity

- Preserve upstream copyright and license notices.
- The repository's MIT license applies only to original project material that may lawfully be licensed under it.
- Review file-level licenses and provenance before reusing any third-party source.
- Do not assume another project's license or compatibility applies to copied files.
- Do not commit proprietary firmware, restore images, keys, credentials, or personal device data.
- Keep the project documentation-first and avoid instructions that alter device security or protected boot configuration.
- A source build or static check does not demonstrate a successful device boot or a complete operating-system port.

## 7. Key project links

- [Project README](README.md)
- [Research roadmap](docs/ROADMAP.md)
- [Device inventory](docs/DEVICE_INVENTORY.md)
- [Device unknowns](docs/DEVICE_UNKNOWNS.md)
- [Snapdragon 732G platform requirements](docs/SOC_PLATFORM_REQUIREMENTS.md)
- [XNU baseline research](docs/XNU_BASELINE.md)
- [XNU research area](xnu/README.md)
- [XNU compatibility matrix](xnu/COMPATIBILITY_MATRIX.md)
- [Loader research area](xnuloader/README.md)
- [Loader architecture](xnuloader/ARCHITECTURE.md)
- [Loader compatibility register](xnuloader/COMPATIBILITY.md)

---

**Current conclusion:** MotoDarwin18 has a growing documentation and research foundation. The next meaningful progress is evidence gathering and feasibility analysis—not claiming a working kernel, loader, or iOS 18 port.


## 8. Device and SoC research update — 2026-11-08

A community-maintained Linux/Android source tree for the shared Moto G40 Fusion / Moto G60 `hanoip` family has narrowed several platform questions. These are provisional family-level findings, not exact-unit confirmation.

- **Interrupts:** shared SDMMAGPIE DTS describes GICv3 and Qualcomm PDC.
- **Timers:** Armv8 generic timer is listed at 19.2 MHz; a memory-mapped timer block is also described.
- **Storage:** source tree describes embedded UFS and SD-card paths; exact flash component remains unknown.
- **Display:** Hanoi panel file selects a Tianma ILI7807S 678-class MIPI-DSI panel description with 60/120 Hz modes; exact XT2135-2 panel still needs confirmation.
- **Wireless:** WCN3990 Bluetooth node and CLD3 WLAN module appear in shared sources; exact Wi-Fi combo-chip remains unknown.
- **Power:** PM6150/PM6150L and MC50 battery profiles appear in the Hanoi overlays; exact unit population remains unverified.
- **Memory:** reserved-memory carveouts are documented, but the complete physical memory map remains unknown.

See [Hanoip / SDMMAGPIE platform evidence](research/soc/HANOIP_PLATFORM_EVIDENCE.md). The shared source tree covers related models and contains board-revision overlays; it does not prove a working XNU port or exact XT2135-2 compatibility.


## 9. Boot ABI compatibility analysis — 2026-11-08

The selected XNU ARM64 boot-argument declarations and several startup consumers have been verified against the pinned `xnu-11215.1.10` source. A new [Boot ABI Compatibility Gap Analysis](docs/BOOT_ABI_COMPATIBILITY_GAPS.md) compares those requirements with available Moto G60 XT2135-2 and shared hanoip-family evidence.

Key conclusion: compatibility is **not demonstrated**. The exact firmware handoff contract, target memory map, device-tree contract, CPU entry state, and target-specific platform services remain unknown. Shared GICv3, timer, storage, display, wireless, and power descriptions are family-level clues only.

This is a research assessment, not a device test. No kernel, loader, bootable image, or target integration is implemented.


## 10. XNU early platform dependency inventory — 2026-11-08

Added [XNU Early Platform Service Dependency Inventory](docs/XNU_EARLY_PLATFORM_DEPENDENCIES.md). It traces the pinned ARM64 startup path and classifies early dependencies as architecture-generic, Apple-specific, platform-specific, configuration-dependent, or unresolved.

The highest-priority open areas remain the firmware entry/boot-argument contract, SecureDT and required `/chosen` properties, exact memory ownership, machine identification, CPU entry assumptions, interrupt/timebase integration, and target Platform Expert services. Shared hanoip/SDMMAGPIE hardware descriptions remain family-level evidence only.

This is a source-derived documentation milestone; it does not implement or validate an XNU port.


## 11. Secure Device Tree requirements analysis — 2026-11-08

Added [Secure Device Tree Requirements Analysis](docs/SECURE_DEVICE_TREE_REQUIREMENTS.md), based on pinned `xnu-11215.1.10` source for `device_tree.h`, `device_tree.c`, `pe_init.c`, `pe_identify_machine.c`, and `arm_init.c`.

Key finding: the reviewed XNU SecureDT code walks an Apple-specific node/property record layout. It must not be assumed to accept a standard Linux FDT blob directly. The reviewed ARM64 startup path requires `/chosen/dram-base` and `/chosen/dram-size`; early machine identification also consumes CPU and SoC/interrupt/timer node conventions. The actual XT2135-2 firmware handoff format and property contract remain unknown.

This is a source/documentation milestone only. No target tree has been extracted, converted, passed to a kernel, or tested on the handset.


## 12. Device Tree property compatibility matrix — 2026-11-08

Added [Device Tree Property Compatibility Matrix](docs/DEVICE_TREE_PROPERTY_COMPATIBILITY_MATRIX.md), comparing the pinned XNU early property consumers with the currently documented Hanoip/SDMMAGPIE Linux source evidence.

The matrix records conceptual overlap for CPU topology, GICv3/PDC, timers, and memory descriptions while keeping exact Apple-style property matches and the XT2135-2 firmware handoff unknown. The mandatory `/chosen/dram-base` and `/chosen/dram-size` properties are not documented in the reviewed Hanoip evidence; “not observed” is not a claim that they are absent from the actual device tree.

This remains a source/documentation milestone. No target tree, boot payload, or device configuration was generated or tested.


## 13. XNULoader menu and pre-release specification — 2026-11-08

Added [XNULoader Menu and Pre-release Specification](xnuloader/MENU_AND_PRERELEASE_SPEC.md). It records the proposed “Boot iOS 18” and “Boot Original Android” menu labels, the tentative Volume Up/Down navigation concept, explicit unknowns around input behavior, and a source-and-documentation-only first pre-release policy.

The first pre-release is specified as **not bootable and not for installation**, with no `.img` or other device-installable artifact. The menu options are conceptual only. No loader implementation, XNU port, iOS 18 environment, Android-return mechanism, or target boot is claimed.
