# XNU Source Reviews

This folder contains MotoDarwin18-authored analysis of selected upstream XNU files. It does not contain copied Apple source code.

## Reviews

- [`pexpert/arm/pe_init.c`](PE_INIT_REVIEW.md) — Platform Expert state, device-tree setup, two-phase initialization, and platform services.
- [`pexpert/pexpert/pexpert.h`](PEXPERT_HEADER_REVIEW.md) — Public Platform Expert declarations and platform obligations.
- [`pexpert/pexpert/arm64/boot.h`](ARM64_BOOT_HEADER_REVIEW.md) — ARM64 boot handoff structure and validation requirements.
- [`osfmk/arm/arm_init.c`](ARM_INIT_REVIEW.md) — Boot CPU initialization order and dependencies on pexpert.

## Source-version warning

MotoDarwin18's provisional source baseline is `xnu-11215.1.10`, recorded in [UPSTREAM.md](../UPSTREAM.md). The source-browser pages used for this initial reading are not all pinned to that exact tag. Therefore these notes are **provisional source observations**, not a claim that every declaration and line is identical in the pinned tag.

Before authoring a patch, compare all four files directly against the pinned tag, record the exact commit and file-level licenses, and update any differences here. No upstream source is copied into this repository.

## Research status

- Source-reading notes: documented, provisional.
- Exact pinned-tag line-by-line verification: pending.
- Moto G60 implementation: not started.
- Host tests or target tests of XNU: not performed.
