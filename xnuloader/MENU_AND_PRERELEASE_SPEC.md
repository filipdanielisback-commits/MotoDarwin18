# XNULoader Menu and Pre-release Specification

**Project:** MotoDarwin18  
**Target research device:** Motorola Moto G60 XT2135-2  
**Status:** Design specification only — no loader implementation or bootable artifact exists.  
**Last updated:** 2026-11-08

## 1. Purpose

This document records the proposed user-interface concept and release policy for a future MotoDarwin18 XNULoader. It is not an implementation guide, boot procedure, firmware interface specification, or claim of device compatibility.

The initial visual concept is a simple menu with two user-facing entries:

1. **Boot iOS 18**
2. **Boot Original Android**

These are aspirational labels. Neither option is currently implemented or demonstrated to work.

## 2. Proposed visual design

The loader should eventually have a clean, readable interface with:

- MotoDarwin18 project name and XNULoader identifier.
- Two clearly separated menu entries.
- A visible highlight showing the current selection.
- Short navigation hints.
- A restrained, high-contrast layout suitable for a phone display.
- Clear error and unavailable-state presentation if a future implementation cannot offer an option.

The design should prioritize legibility and predictable behavior over visual effects. It should not imitate Apple's proprietary boot interface or imply official Apple software.

## 3. Proposed input model

The concept under consideration is:

- Volume Up / Volume Down: move the highlighted selection.
- A separate confirmation input: activate the highlighted entry.

The exact confirmation key, key-event availability, repeat behavior, timeout policy, accessibility behavior, and input handling are **not specified**. They must not be assumed until a supported input environment is established and reviewed.

This document does not define hardware key scanning, firmware calls, boot services, or device-specific input code.

## 4. Menu option semantics

### 4.1 “Boot iOS 18”

Proposed label only. It must remain unavailable or clearly marked as a nonfunctional placeholder until all of the following have been independently established:

- A lawful and technically supportable userland source and licensing model.
- A compatible XNU kernel and target platform implementation.
- A documented loader-to-kernel interface for the exact target.
- Required platform services and hardware support.
- Reproducible validation appropriate to the claimed capability.

A menu label is not evidence that iOS 18 can run on the target. No Apple proprietary firmware, restore image, keys, or userland files may be redistributed in a project release without the necessary rights.

### 4.2 “Boot Original Android”

Proposed label only. It must not promise that the loader can preserve, chain-load, restore, or return to the installed Android environment. Such behavior would require a separately documented and validated design. No partition, boot configuration, or firmware modification is authorized by this specification.

## 5. Development and release stages

Use explicit stages so that a design mock-up is never confused with an executable loader.

| Stage | Meaning | Permitted public claim |
|---|---|---|
| Concept | Menu idea and visual design documented | “Concept only” |
| Specification | Behavior and limitations documented | “Design specification available” |
| UI prototype | Non-device, non-booting mock-up | “UI prototype; not a loader” |
| Host-tested component | Isolated component tested on a host system | Name the exact component and test |
| Integrated loader | Loader code integrated in a documented environment | Do not claim target support without target evidence |
| Target validation | Exact-model behavior validated under an approved test plan | State the exact test, hardware revision, and limitations |

The project currently remains in documentation and feasibility research. It has not reached the UI prototype or integrated-loader stage.

## 6. First pre-release policy

The first GitHub pre-release, if published, should be a **source-and-documentation milestone only**.

### Include

- Repository source and documentation available at the selected commit.
- A clear summary of completed research and current limitations.
- Links to the project status, porting plan, XNU baseline, and loader specification.
- A statement that no bootable loader or operating-system image is included.
- A statement that the release is for development and research only.

### Do not include

- A `.img`, disk image, firmware image, boot payload, or other device-installable artifact.
- Instructions for flashing, unlocking, bypassing, or changing protected boot configuration.
- Apple proprietary iOS components, restore images, keys, or vendor firmware.
- Claims that iOS 18 or original Android can be launched from XNULoader.
- Unsupported device compatibility or test claims.

GitHub's automatically generated source archives represent repository source at a selected tag; they are not a device image and must not be described as bootable.

## 7. Required release-page wording

Suggested title:

**MotoDarwin18 — Development Pre-release 0.1.0**

Suggested short description:

> Early documentation and feasibility research milestone for Darwin/XNU compatibility research on the Motorola Moto G60 XT2135-2. Includes project documentation and source-level research only.

Required warning:

> **NOT BOOTABLE — NOT FOR INSTALLATION.** This pre-release does not contain XNULoader, a bootable image, an XNU port, or an iOS 18 implementation. Do not attempt to install or flash this release to a device. The menu options described in the documentation are conceptual only.

Suggested release notes:

- Added XNULoader menu concept and input-model documentation.
- Recorded the proposed “Boot iOS 18” and “Boot Original Android” labels as future UI concepts.
- Documented the source-only release policy and explicit non-bootable status.
- Continued XNU, boot ABI, SecureDT, and device-tree compatibility research.
- No device boot, firmware modification, or target integration is claimed.

## 8. Versioning and evidence

A future release must identify:

- Exact source commit and tag.
- Date and release status (pre-release).
- Files included and explicitly excluded.
- CI workflow result, with a link to the actual run where available.
- Checksums for any future distributable files, if such files are appropriate and approved.
- Exact test environment and scope.
- Known issues and unsupported capabilities.

Do not publish a checksum for a file that is not included. Do not describe documentation validation as device validation.

## 9. Relationship to current project status

The current project has no implemented XNULoader, no working XNU kernel port, no bootable image, and no demonstrated iOS 18 compatibility on XT2135-2. The proposed menu is a design target only.

Relevant documents:

- [Project status](../STATUS.md)
- [XNULoader architecture](../xnuloader/ARCHITECTURE.md)
- [XNULoader handoff requirements](../xnuloader/HANDOFF_REQUIREMENTS.md)
- [Porting plan](PORTING_PLAN.md)
- [Boot ABI compatibility gaps](BOOT_ABI_COMPATIBILITY_GAPS.md)
- [Secure Device Tree requirements](SECURE_DEVICE_TREE_REQUIREMENTS.md)
- [Device Tree property compatibility matrix](DEVICE_TREE_PROPERTY_COMPATIBILITY_MATRIX.md)

---

**Conclusion:** The proposed two-option menu is recorded as a future interface concept. The first pre-release should be source-and-documentation only, explicitly non-bootable, and contain no device-installable image.
