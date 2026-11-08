# XNU Source Reviews

This folder contains MotoDarwin18-authored analysis of selected upstream XNU files. It does not contain copied Apple source code.

## Reviews

- [`pexpert/arm/pe_init.c`](PE_INIT_REVIEW.md) — Platform Expert state, device-tree setup, two-phase initialization, and platform services.
- [`pexpert/pexpert/pexpert.h`](PEXPERT_HEADER_REVIEW.md) — Public Platform Expert declarations and platform obligations.
- [`pexpert/pexpert/arm64/boot.h`](ARM64_BOOT_HEADER_REVIEW.md) — ARM64 boot handoff structure and validation requirements.
- [`osfmk/arm/arm_init.c`](ARM_INIT_REVIEW.md) — Boot CPU initialization order and dependencies on pexpert.
- [Pinned XNU source verification](PINNED_SOURCE_VERIFICATION.md) — Exact declarations and selected consumer paths checked at `xnu-11215.1.10`.

## Source-version status

The selected declarations and consumer paths documented in `PINNED_SOURCE_VERIFICATION.md` were fetched at the immutable `xnu-11215.1.10` tag, peeled commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`. File blob hashes are recorded in that verification report.

The earlier individual review notes remain provisional where they contain observations from non-pinned source-browser pages. The pinned verification report supersedes those notes for the specific declarations and use sites it documents. It does not claim a complete audit of every reader, writer, conditional configuration, or producer-side boot contract.

## Research status

- Pinned declarations and selected consumers: verified.
- Full boot ABI producer/consumer audit: incomplete.
- Moto G60 implementation: not started.
- XNU host build, emulator test, or target test: not performed.
