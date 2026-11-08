## 2026-11-08 — XT2135-2 board-revision mapping audit

### Findings

- Motorola's conformity index confirms XT2135-2 / MC38C / moto g60 vision, distinct from XT2135-1 / MC38B.
- The public community Android device tree describes a shared Moto G40 Fusion / Moto G60 hanoip target. Its README, BoardConfig.mk, and board-info.txt establish a software build identity (hanoip), not a physical PCB revision.
- BoardConfig uses hanoip for OTA assertion and bootloader board-name strings and selects shared platform-family kernel configuration. Those strings do not identify DVT1 or DVT2.
- The previously reviewed Hanoip kernel family source contains DVT1 and DVT2 overlay material, but no authoritative link from XT2135-2 / MC38C to either overlay was located.
- A third-party service-document listing for the broad XT2135-X family is only an unverified lead. Its contents and authenticity were not established, and it does not map an exact XT2135-2 board revision.

### Decision

The exact regulatory model identity and shared software-family identity are confirmed. The physical board revision and DVT overlay mapping remain unknown. Do not select an overlay or make a DVT-specific kernel change.

### Detailed evidence

See [XT2135-2 Board-Revision Evidence Audit](../research/firmware/XT2135_2_BOARD_REVISION_AUDIT.md).

## 2026-11-08 — XT2135-2 public firmware/source provenance audit

### Question

Does public manufacturer material now establish the exact XT2135-2 firmware-to-OS handoff contract required for comparison with pinned XNU?

### Findings

- Motorola's EU product-compliance index identifies XT2135-2 as MC38C / moto g60 vision, distinct from XT2135-1 / MC38B.
- Motorola's `MotorolaMobilityLLC/kernel-msm` source-publication tracker links exact XT2135-2 European Android firmware build identifiers to Motorola kernel source release tags `MMI-S2RIS32.32-20-9-9-2-1` and `MMI-S2RIS32.32-20-9-9-2-3`.
- This improves provenance for the Android/Linux kernel source associated with those firmware builds.
- The Motorola kernel-source releases do not establish the contents of the boot firmware, bootloader implementation, firmware-to-OS entry ABI, XNU `boot_args` producer semantics, SecureDT representation, memory ownership, or pre-OS display/input protocols.
- The shared `hanoip` Android/Linux source remains family-level evidence. It does not map an exact XT2135-2 unit to DVT1 or DVT2.

### Decision

The public source trail is useful, but the exact firmware-to-XNU handoff remains **unknown**. No kernel source patch or compatibility claim is justified by these sources.

### Sources and detailed matrix

See [XT2135-2 Public Firmware and Source Evidence Register](../research/firmware/XT2135_2_PUBLIC_SOURCE_EVIDENCE.md).

# Research log

## 2026-11-08 — SecureDT consumer contract crosswalk

### Work completed

- Rechecked the pinned SecureDT structures and traversal code, Platform Expert initialization, machine/SoC identification, interrupt/timer discovery, and early ARM64 DRAM-property consumers.
- Classified tree representation and pointer/length/lifetime requirements separately from node/property requirements.
- Split early fatal requirements, gated SoC/CPU requirements, later interrupt/timebase dependencies, optional metadata, and debug/target-conditional properties.
- Compared those consumer expectations with the documented shared Hanoip / SDMMAGPIE Linux source clues without upgrading family evidence to exact XT2135-2 facts.

### Findings

- XNU SecureDT consumes an Apple-specific in-memory node/property representation; standard FDT has a different header/structure/strings layout and standard big-endian cell encoding.
- The reviewed ARM64 path requires /chosen/dram-base and /chosen/dram-size; absence is fatal in that path.
- The /cpus assertion is gated by successful SoC-base discovery through the arm-io path.
- Interrupt-controller and timer nodes are later Platform Expert dependencies. Their expected XNU naming and reg interpretation are not proven by the Hanoip GICv3/PDC and timer clues.
- CPU frequency fields and several model/debug/firmware metadata properties are optional or conditional, not universal mandatory requirements.
- No exact XT2135-2 firmware tree, property encoding, pointer lifetime, memory ownership, or producer contract was located.

### Decision

No executable XNU patch is justified. The crosswalk records concrete consumer requirements and evidence gaps, not a demonstrated exact-target producer/consumer mismatch.

### Detailed report

See [SecureDT Contract Crosswalk](../xnu/source-reviews/SECUREDT_CONTRACT_CROSSWALK.md).

### Next evidence gate

Continue seeking authoritative exact-model firmware-side documentation for tree representation and property semantics. If it remains unavailable, preserve the unknowns rather than inventing values or constructing a device handoff.


## 2026-11-08 — Pinned XNU ARM64 configuration-dependent startup audit

### Scope

Reviewed the pinned `xnu-11215.1.10` ARM64 startup assembly, boot CPU initialization, Platform Expert, machine-identification/interrupt-timebase discovery, VM setup, CPU paths, board configuration and iPhoneOS ARM64 build template.

### Findings

- ARM64 instructions and architectural facilities are only the lowest layer. XNU still consumes its own boot-argument ABI and depends on SecureDT, machine identification, Platform Expert, memory ownership, interrupt/timebase services and a matching build configuration.
- Some Apple-named machine-routine hooks have empty non-Apple ARM64 implementations, while Apple-family register-specific paths are guarded. This is a useful portability distinction, but it does not make the complete startup path firmware-agnostic.
- The pinned Platform Expert source expects SecureDT structures/properties for SoC-base discovery, CPU information, interrupt-controller and timer discovery. The ARM64 boot CPU path also requires `/chosen/dram-base` and `dram-size`.
- The shared Hanoip Linux source's GICv3/PDC and timer clues do not prove that the XT2135-2 firmware supplies XNU's expected SecureDT node/property contract.
- ARM64 VM and CPU behavior varies with build options including `ARM_LARGE_MEMORY`, `XNU_MONITOR`, `KASAN`, `CONFIG_SPTM`, `USE_APPLEARMSMP`, and Apple-family/SoC macros. No target-appropriate Moto XNU board/build profile is established in the reviewed upstream board configuration.

### Decision

No executable patch is justified. The audit found concrete platform integration requirements, but no demonstrated upstream XNU source defect or exact XT2135-2 producer/consumer mismatch. Keep source changes deferred.

### Detailed report

See [ARM64 Configuration-Dependent Startup Audit](../xnu/source-reviews/ARM64_CONFIGURATION_DEPENDENCY_AUDIT.md).

### Next task

Create a SecureDT contract crosswalk covering early mandatory, optional, configuration-gated and later-use properties, then compare it with Hanoip source evidence without upgrading family clues to exact-model facts.


## 2026-11-08 — Hanoip / SDMMAGPIE source-tree review

### Question

Can public Android/Linux engineering sources narrow the seven outstanding hardware questions for Moto G60 XT2135-2?

### Sources reviewed

- Shared Moto G40 Fusion / Moto G60 (`hanoip`) Android device tree and its build configuration.
- LineageOS Motorola SM6150 kernel source, especially the SDMMAGPIE SoC tree, Hanoi base tree, Hanoip common overlay, panel file, touchscreen file, and battery/thermal overlay.
- Qualcomm Snapdragon 732G product brief for SoC naming and capability context.

### Findings

- The shared device tree uses the codename `hanoip`; its BoardConfig uses `sm6150` as an Android build-platform label and points to a Motorola SM6150 kernel tree. The kernel DTS names the SoC family `sdmmagpie`, while Qualcomm's Snapdragon 732G brief lists part number SM7150-AC. Preserve these naming differences; do not infer silicon identity from a repository directory alone.
- The shared SoC DTS describes a GICv3 interrupt controller and Qualcomm PDC.
- The same DTS lists an Armv8 generic timer at 19.2 MHz and a memory-mapped timer block.
- The device-tree storage aliases describe embedded UFS, SDC1/eMMC, and SDC2/SD-card paths. Android partition references use a UFS host path.
- The Hanoi panel file includes a Tianma ILI7807S 678-class 1080 × 2460 MIPI-DSI panel description with 60/120 Hz modes.
- The Hanoi touchscreen file describes an Ilitek SPI touchscreen node.
- The shared SoC tree includes a Qualcomm WCN3990 Bluetooth node. The hanoip Android module list includes `qca_cld3_wlan.ko`; that module name does not identify the exact Wi-Fi chip.
- Hanoi battery/thermal files describe PM6150/PM6150L power-management devices and MC50 6000 mAh battery profiles from ATL and SUNWODA.
- Reserved-memory carveouts exist in the kernel DTS, but they do not amount to a complete physical memory map.

### Confidence and limitations

These are community-source findings for a shared G40 Fusion/G60 family tree, not an official Motorola schematic. The exact XT2135-2 board revision and the correct DVT overlay for a particular unit are not mapped. Hardware candidates must remain provisional until corroborated by exact-model evidence.

### Conclusion

The source tree provides useful candidate platform details for GICv3, timers, UFS/SD-card paths, display, touchscreen, wireless software, and PMIC/battery configuration. It does not establish a complete XT2135-2 board inventory or Darwin/XNU compatibility.

### Next research task

Identify the exact XT2135-2 board revision and correlate its selected device-tree overlay with official Motorola sources where possible. Continue to treat the full memory map and exact WLAN combo-chip as open questions.


A concise record of research decisions and evidence. Add new entries at the top. Keep observations separate from assumptions and conclusions.

## 2026-11-08 — Exact-model and SoC evidence review

### Question

What can be stated from primary manufacturer sources about the Motorola Moto G60 XT2135-2 and Qualcomm Snapdragon 732G, without confusing SoC capabilities with the handset's implementation?

### Verified facts

- Motorola's EU Declaration of Conformity identifies the market model as moto g60, XT2135-2, type name MC38C. The declaration was issued 2021-03-05.
- The same Motorola declaration lists WLAN IEEE 802.11a/b/g/n/ac, Bluetooth 5.0, GPS, GLONASS, Galileo, FM receive, and NFC for the named model.
- Qualcomm's Snapdragon 732G product brief lists the Kryo 470 CPU, Adreno 618 GPU, Hexagon 688 processor, X15 LTE modem, FastConnect 6200 subsystem, Spectra 350 ISP, and SM7150-AC part number.
- Qualcomm's brief lists Wi-Fi 6-ready platform capabilities and Bluetooth 5.1, while Motorola's exact-model declaration lists 802.11ac and Bluetooth 5.0 for XT2135-2.
- Qualcomm explicitly notes that certain optional platform features are subject to carrier and OEM selection.

### Interpretation

- The Motorola declaration is stronger evidence for the regulatory radio capabilities of XT2135-2 than the Qualcomm platform maximums.
- The Snapdragon 732G brief is useful for identifying broad platform capabilities, but it is not a board schematic, programming manual, firmware handoff specification, or complete bill of materials.
- The difference between platform capability and handset specification demonstrates why the project must keep two evidence categories.

### Unknowns and limitations

- The exact motherboard revision and component population are not established.
- The display, touch, storage, audio, camera, sensor, wireless combo-chip, PMIC, and controller part numbers remain open.
- The physical memory map, reserved regions, interrupt routing, timer configuration, and firmware handoff remain undocumented in this repository.
- No evidence in these sources establishes a Darwin/XNU boot path or driver support for the handset.

### Sources

- Motorola, [EU Declaration of Conformity — XT2135-2 / MC38C](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf), issued 2021-03-05.
- Qualcomm, [Snapdragon 732G Mobile Platform product brief](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf).
- Qualcomm, [Snapdragon 732G product page](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform).

### Next research task

Continue with exact-model public documentation and platform-level architectural references. Prioritize board-level evidence and clearly document when information is not publicly available.

## 2026-11-08 — Documentation foundation expanded

### Work recorded

- Added a device hardware inventory for Moto G60 XT2135-2.
- Added a compatibility matrix for major Darwin/XNU platform areas.
- Added a references index and technical glossary.
- Added this log, a platform integration checklist, a source provenance policy, and an experiment review policy.

### Findings and limits

- The public XNU repository describes XNU as part of Darwin and documents ARM64 among its supported architectures in the current repository README.
- XNU's source tree includes both general kernel subsystems and platform-specific areas. This supports the project's emphasis on platform integration rather than CPU compatibility alone.
- Independent ARM64 porting documentation highlights the need to collect board-specific details such as memory reservations, interrupt controllers, storage, display, touch, wireless components and firmware versions.
- These general references do not demonstrate Moto G60 XT2135-2 support.

### Current project conclusion

**No working Moto G60 Darwin/XNU port is claimed.** Hardware inventory and compatibility status remain incomplete. All device-specific claims must be supported by exact-model evidence.

### Sources

- [Apple XNU repository](https://github.com/apple-oss-distributions/xnu)
- [UniXNU: Port a device](https://unixnu.com/porting/steps)
- [UniXNU: Architecture overview](https://unixnu.com/porting/)

## Entry template

### YYYY-MM-DD — Short title

**Question:** What was being investigated?

**Sources:** Link primary sources and record versions or dates.

**Verified facts:**
- 

**Observations:**
- 

**Inferences (labelled):**
- 

**Unknowns / contradictions:**
- 

**Conclusion:** What can and cannot be claimed?

**Next research task:**
- 


## 2026-11-08 — Confirmed platform facts and XNU compatibility reconciliation

### Work completed

- Reconciled Motorola's XT2135-2 / MC38C declaration with the Motorola Android kernel-source publication trail.
- Reclassified shared hanoip / SDMMAGPIE subsystem observations as family-level clues unless an exact XT2135-2 board-revision link exists.
- Compared the evidence against the pinned XNU ARM64 entry, `boot_args`, VM, SecureDT, CPU, interrupt, timer, console and later platform-service dependencies.
- Recorded the executable source-patch decision.

### Findings

- Confirmed exact-model facts are primarily model identity and regulatory radio capabilities in Motorola's declaration.
- Motorola's public source tracker provides Android/Linux kernel-source provenance for named XT2135-2 builds, not a firmware-to-XNU handoff specification.
- The shared Hanoip tree's `hanoip` identifiers are software build identity labels, not physical PCB revision identifiers.
- Detailed GICv3/PDC, timer, storage, display, touch, WLAN, PMIC and audio observations remain family-level evidence.
- The exact board revision, DVT overlay mapping, complete memory map, entry CPU state, producer-side boot ABI and SecureDT handoff remain unknown.

### Decision

No executable XNU patch is justified. No specific upstream XNU source defect or exact producer/consumer mismatch has been demonstrated. Do not modify boot ABI consumers or platform startup code to compensate for unknown target behavior.

### Detailed review

See [XT2135-2 Confirmed Platform Facts and XNU Compatibility Review](../research/firmware/XT2135_2_CONFIRMED_PLATFORM_FACTS.md).


## 2026-11-08 — XT2135-2 firmware and board-revision documentation follow-up

### Sources reviewed

- Motorola official Right to Repair page and its linked repair-document portal.
- Third-party EletrônicaBR listing for a broad XT2135-X / G60 / G40 service-document package.
- Third-party schematic index advertising an XT2135-x component-location item.
- Motorola kernel-msm issue #574 and the linked Android/Linux kernel-source release.
- Android Open Source Project device-tree overlay documentation.

### Findings

- Motorola's official page confirms that service manuals, parts lists and schematics are distributed through its repair-document channel. The linked partner portal returned a JavaScript/anti-bot interstitial, so no XT2135-2-specific manual or revision data was independently verified.
- The third-party service listing groups XT2135-X, G60 and G40. Its document contents and applicability to MC38C / a specific PCB revision were not verified.
- A separate third-party schematic index also lacks verifiable board-revision detail.
- Motorola issue #574 links a named XT2135-2 Android 12 firmware build to the Motorola `kernel-msm` source release tag `MMI-S2RIS32.32-20-9-9-2-3`. This is Android kernel source provenance, not a boot-firmware or XNU handoff specification.
- General Android documentation explains DTB/DTBO overlay behavior, but does not identify the overlay used on this exact handset.

### Decision

No authoritative exact-model PCB assembly/revision mapping, DVT1/DVT2 selection, or firmware-to-XNU entry contract was found. Keep those facts unknown. No executable XNU patch is justified.

### Detailed record

See [XT2135-2 Firmware and Board-Revision Documentation Follow-up](../research/firmware/XT2135_2_FIRMWARE_BOARD_REVISION_FOLLOWUP.md).
