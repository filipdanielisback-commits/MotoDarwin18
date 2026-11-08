# Community Hanoip U-Boot FDT Evidence Audit

**Project:** MotoDarwin18  
**Target under investigation:** Motorola Moto G60 XT2135-2 / MC38C  
**Candidate source:** `eng-brener/hanoip-mainline`  
**Reviewed commit:** `ea0186ba9a556549a004bd14e77d9c53681e0302`  
**Reviewed file:** `work/sensors-20261026/se11-id-read/uboot-expanded.dts`  
**File blob SHA:** `290c82eff78064e345f475a08c8183d9a1eaec1d`  
**Review date:** 2026-11-08  
**Status:** Secondary community-source evidence; not an exact XT2135-2 firmware handoff dump.

## 1. Why this source was reviewed

A public GitHub search surfaced a community Hanoip project containing a file named `uboot-expanded.dts`. The file is more concrete than a generic family DTS summary because it is a large expanded Linux device-tree source snapshot with a root model/compatible declaration and populated CPU, memory, interrupt, timer and display descriptions.

The repository README self-describes its scope as a mainline Linux/U-Boot effort for a Moto G60 identified as `hanoip` / `SM7150`, and labels the platform as Snapdragon 730G / SM7150 / SDMMAGPIE. It also describes the Linux-facing tree used by that project's U-Boot build as an embedded FDT. These are statements made by that community repository, not Motorola certification.

The reviewed repository search did not return occurrences of `XT2135-2` or `MC38C`. This is a scoped code-search result, not proof that those strings occur nowhere in every historical revision or unindexed file.

## 2. Direct observations in the pinned DTS file

The pinned file declares:

- Root model: `Motorola Moto G60`.
- Root compatibility strings: `motorola,hanoip` and `qcom,sm7150`.
- A `/chosen` node with Linux boot arguments and a simple-framebuffer description.
- Eight CPU nodes under `/cpus`.
- A memory node and a `/reserved-memory` section.
- GIC-compatible interrupt-controller descriptions.
- An Arm generic-timer description.
- Numerous Qualcomm SoC and peripheral nodes.

A source-level presence check of the complete 5,300-line file found:

| XNU crosswalk item | Present in this community DTS file? | Interpretation |
|---|---:|---|
| `/chosen` | Yes | Linux FDT has a chosen node |
| `/chosen/dram-base` | No | Not observed in this file |
| `/chosen/dram-size` | No | Not observed in this file |
| `arm-io` node | No | XNU's Apple-style selector not observed |
| `interrupt-controller = "master"` | No | XNU's selector not observed |
| `device_type = "timer"` | No | XNU's selector not observed |
| GIC-compatible descriptions | Yes | Hardware concept is represented in this FDT |
| Arm generic timer description | Yes | Hardware concept is represented in this FDT |
| Memory and reserved-memory nodes | Yes | Linux memory description exists; not a complete XNU memory-ownership contract |
| Simple framebuffer | Yes | A Linux-facing framebuffer description exists; not proof of a pre-OS UEFI GOP service |

“Not observed” is scoped only to this pinned file. It does not establish absence from another DTB, firmware-generated tree, board overlay, or a particular XT2135-2 unit.

## 3. Provenance and applicability limits

This is **not** an authoritative Motorola firmware document and must not be promoted to exact-model firmware evidence.

Reasons:

1. The repository identifies its subject at the broader Moto G60 / Hanoip / SM7150 level.
2. The root DTS strings identify `motorola,hanoip` and `qcom,sm7150`, not XT2135-2 / MC38C.
3. The repository's own SoC label is SM7150 / Snapdragon 730G, while the MotoDarwin18 target's reported identity is Snapdragon 732G / SM7150-AC. This naming difference is a reason to preserve the variant uncertainty, not a basis for independently identifying the target silicon.
4. The repository describes a community-built U-Boot's embedded Linux FDT. That is not the same thing as an unmodified Motorola firmware handoff tree.
5. No physical PCB revision, DVT1/DVT2 mapping, exact MC38C association, or authoritative target-unit provenance was established by the reviewed file.
6. The source is a conventional DTS representation of an FDT-style Linux tree, not an XNU SecureDT memory image.

The repository's operational README content was not reproduced or assessed as a procedure. This audit uses only source provenance and declarative DTS facts.

## 4. What the source adds to the SecureDT comparison

The file strengthens the **family-level** evidence that Linux on a Hanoip-labelled Moto G60 can describe CPU topology, memory, reserved regions, GIC, generic timer and display information in an FDT-style tree.

It does not fill the critical XNU gaps:

- It does not document an XT2135-2 firmware producer for `boot_args.deviceTreeP` and `deviceTreeLength`.
- It does not establish the XNU SecureDT node/property record layout or lifetime contract.
- It does not show XNU's required `/chosen/dram-base` and `dram-size` properties in this particular Linux DTS file.
- It does not supply XNU's `arm-io` / `ranges` SoC-base selector.
- It does not show the exact interrupt-controller and timer selectors searched by the pinned XNU source.
- It does not establish memory ownership, reserved-region semantics for XNU, CPU startup services, or target firmware state.

A community U-Boot Linux FDT could be useful as a later *comparison sample* if its exact device and source provenance are established. It is not evidence that the XT2135-2 stock firmware already provides an XNU-compatible tree, nor does it prove that such compatibility is impossible.

## 5. Compatibility decision

**No executable XNU patch is justified.**

The newly reviewed file is valuable as a concrete Hanoip-family Linux FDT example, but it is not the exact target producer. The observed differences are between a Linux FDT source sample and XNU's SecureDT consumer expectations. Without an authoritative XT2135-2 firmware-side contract, these are format and evidence gaps—not a demonstrated bug in upstream XNU.

Do not infer target properties, copy addresses, synthesize a tree, or choose a board overlay from this sample.

## 6. Pinned source reference

- [Community Hanoip expanded DTS at reviewed commit](https://github.com/eng-brener/hanoip-mainline/blob/ea0186ba9a556549a004bd14e77d9c53681e0302/work/sensors-20261026/se11-id-read/uboot-expanded.dts)
- [Devicetree Specification](https://www.devicetree.org/specifications/)
- [MotoDarwin18 SecureDT Contract Crosswalk](../../xnu/source-reviews/SECUREDT_CONTRACT_CROSSWALK.md)

## 7. Conclusion

This is the strongest new public Hanoip FDT sample located in this review, but it remains secondary family-level evidence. It narrows what a Linux-facing Hanoip tree can look like while leaving the XT2135-2 firmware producer, physical board revision and XNU SecureDT contract unresolved.

*Project: MotoDarwin18*
