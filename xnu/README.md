# XNU Research Area

This directory is reserved for MotoDarwin18's work related to Apple's open-source XNU kernel.

**Status:** documentation scaffold only. No Moto G60 kernel port, device driver, patch, or build configuration is implemented here yet.

## Planned layout

- `patches/` — project-authored patch series against a documented upstream XNU revision.
- `files/` — new project-authored source files, with their intended upstream paths documented.
- `scripts/` — source preparation, patch validation, and reproducibility helpers.

## Source and licensing policy

- Obtain upstream XNU source from an authoritative public source and record the exact repository, revision, and retrieval date before basing changes on it.
- XNU source is distributed under the Apple Public Source License (APSL) where its file notices specify that license. Preserve copyright and license notices, mark modifications, and review the applicable license before redistributing changes.
- Do not assume the repository's root MIT license overrides XNU's file-level licensing.
- Do not copy HakiOS patches, source files, or drivers into this project without reviewing their origin, license, notices, and compatibility.
- Keep proprietary operating-system components, device firmware, keys, and personal device data out of this directory.

## Research sequence

1. Identify and record a suitable upstream XNU revision.
2. Review architecture and platform assumptions without claiming device support from ARM64 alone.
3. Document the Moto G60 XT2135-2 hardware facts and unknowns.
4. Propose small, independently reviewable changes only when evidence supports them.
5. Validate patch applicability and build feasibility in a non-device test environment before considering any hardware experiments.

## Current limitations

The Snapdragon 732G platform and the Moto G60 board require platform-specific support. No such support is implied by this scaffold. This project does not currently claim a bootable kernel or compatible driver set.
