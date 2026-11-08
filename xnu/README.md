# XNU Research Area

This directory contains MotoDarwin18's documentation and, later, project-authored work relating to Apple's open-source XNU kernel.

<badge>Research scaffold</badge>

**Current status:** no Moto G60 kernel port, platform driver, patch series, or device-specific build configuration is implemented here.

## Directory map

| Path | Purpose | Current contents |
|---|---|---|
| [patches/](patches/README.md) | Focused changes against a pinned upstream revision | Policy and review guidance only |
| [files/](files/README.md) | Original files proposed for an upstream XNU tree | Provenance guidance only |
| [scripts/](scripts/README.md) | Reproducible source and patch validation helpers | Safety and design guidance only |
| [COMPATIBILITY_MATRIX.md](COMPATIBILITY_MATRIX.md) | Subsystem evidence and status | Initial unknowns |
| [UPSTREAM.md](UPSTREAM.md) | Upstream source selection and provenance | Provisional `xnu-11215.1.10` baseline |
| [PEXPERT_REVIEW.md](PEXPERT_REVIEW.md) | ARM64 Platform Expert research | Interface and startup overview |
| [PLATFORM_INTERFACE_MATRIX.md](PLATFORM_INTERFACE_MATRIX.md) | XNU-to-platform requirements | Evidence-gated interface map |
| [PLATFORM_PORTING_CHECKLIST.md](PLATFORM_PORTING_CHECKLIST.md) | Research and implementation gates | No device modifications |

## Upstream XNU areas to understand

Apple's upstream README describes these major source areas:

- `osfmk/` — Mach-based kernel subsystems.
- `bsd/` — BSD subsystems.
- `iokit/` and `libkern/` — IOKit and related kernel C++ support.
- `pexpert/` — platform-specific code, including interrupt handling and other platform services.
- `libsa/` — kernel bootstrap code.
- `config/`, `makedefs/`, and `SETUP/` — configuration and build support.
- `tools/` — development, debugging, and profiling utilities.

This is an orientation map, not a statement that each area needs modification for Moto G60.

## Project rules

1. Pin an exact upstream commit before preparing any patch.
2. Keep upstream source separate from MotoDarwin18-authored files.
3. Record the source URL, commit, retrieval date, license, and modifications.
4. Preserve all upstream copyright and license notices.
5. Review each file's own license; the repository's root MIT license does not override third-party or file-level terms.
6. Do not copy third-party patches or drivers without provenance and license review.
7. Keep proprietary firmware, restore images, keys, credentials, and personal device data out of this repository.
8. Treat ARM64 as an architecture prerequisite, not proof of board compatibility.

## Research workflow

1. Record the candidate source in [UPSTREAM.md](UPSTREAM.md).
2. Compare the candidate's documented architecture and platform assumptions with [the platform requirements](../docs/SOC_PLATFORM_REQUIREMENTS.md).
3. Track evidence and unknowns in [COMPATIBILITY_MATRIX.md](COMPATIBILITY_MATRIX.md).
4. Use [PEXPERT_REVIEW.md](PEXPERT_REVIEW.md) and [PLATFORM_INTERFACE_MATRIX.md](PLATFORM_INTERFACE_MATRIX.md) to identify interfaces and missing evidence.
5. Propose a patch only when a specific, evidence-backed gap is identified.
6. Validate source changes in an isolated development environment; this folder does not provide instructions for changing a phone.

## Current assessment

MotoDarwin18 is at the documentation and feasibility stage. There is no supported Moto G60 XNU kernel, boot path, or device driver set at this time. The selected XNU tag is a provisional research baseline, not proof that it is the exact XNU build used by a particular iOS 18 release.

## Primary reference

- Apple, [XNU source repository and README](https://github.com/apple-oss-distributions/xnu/blob/main/README.md).
