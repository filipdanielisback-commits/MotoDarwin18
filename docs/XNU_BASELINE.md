# XNU Baseline Research

**Status:** Candidate reference identified; project baseline not yet selected.

## Purpose

Record the upstream XNU version that MotoDarwin18 may evaluate. Selecting a source baseline is a research decision, not evidence of compatibility with the Moto G60.

## Candidate reference

The HakiOS project documentation has described its XNU base as **xnu-8796.121.2**. Treat this as a lead for comparison only. Before adopting it, verify the exact upstream Apple source tag or commit, its release context, source availability, and applicable file-level notices.

- Apple open-source distributions: https://github.com/apple-oss-distributions
- XNU source repository: https://github.com/apple-oss-distributions/xnu
- HakiOS XNU repository: https://github.com/oosexgang/hakios-xnu-kernel

## Selection checklist

- [ ] Identify candidate upstream XNU tags and commits.
- [ ] Confirm the source tree and release metadata directly from Apple’s repository.
- [ ] Record the exact commit hash, not only a version label.
- [ ] Review the license and notices for every source component considered.
- [ ] Compare architecture and platform assumptions at a documentation level.
- [ ] Record known gaps between upstream XNU and the target ARM64 platform.
- [ ] Obtain a project review before introducing third-party patches or derived files.

## Licensing and provenance

XNU source files may carry Apple Public Source License (APSL) notices. The repository's root MIT license does not replace or override file-level licenses. Preserve copyright notices and record provenance for any source or patch considered.

Do not copy HakiOS implementation files into MotoDarwin18 without first reviewing the exact file's license, notices, origin, and compatibility with this project's licensing policy.

## Current decision

No XNU baseline is formally selected. No kernel port, patch set, or device support is claimed.

*Project: MotoDarwin18*
