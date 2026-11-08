# Research log

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
