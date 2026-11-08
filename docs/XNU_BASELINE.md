# XNU Baseline Research

**Status:** upstream source repository identified; exact project baseline not selected.

## Purpose

Record the upstream XNU revision that MotoDarwin18 may evaluate. Selecting a source baseline is a research decision, not evidence of compatibility with the Moto G60 XT2135-2.

## Primary upstream source

- Apple open-source XNU repository: https://github.com/apple-oss-distributions/xnu
- Upstream README: https://github.com/apple-oss-distributions/xnu/blob/main/README.md

The upstream README describes XNU as a hybrid kernel combining Mach, BSD components, and IOKit. It identifies major source areas including `osfmk`, `bsd`, `iokit`, `pexpert`, and `libsa`. These descriptions are useful for orientation; they do not establish support for the target handset.

## Related project reference

HakiOS project materials have described their XNU base as `xnu-8796.121.2`. This is a comparison lead only. It is not selected as MotoDarwin18's baseline and does not imply that HakiOS patches or device support are compatible with this project.

- HakiOS repository: https://github.com/oosexgang/hakios-xnu-kernel

## Selection checklist

- [ ] Identify candidate Apple source tags and commits.
- [ ] Confirm release metadata directly from Apple's repository.
- [ ] Record the exact immutable commit hash, not only a version label or moving branch.
- [ ] Record retrieval date and source URL.
- [ ] Review the license and notices for every component considered.
- [ ] Compare documented architecture and platform assumptions.
- [ ] Record known gaps against the Snapdragon 732G platform requirements.
- [ ] Review any third-party patch or derived file separately.
- [ ] Approve the proposed baseline in project documentation before treating it as selected.

## Licensing and provenance

XNU files may carry Apple Public Source License (APSL) notices. The repository's root MIT license does not replace or override file-level licenses. Preserve copyright notices and review the terms applicable to the exact files being used.

Do not copy HakiOS implementation files into MotoDarwin18 without reviewing the exact file's origin, license, notices, and compatibility.

## Current decision

No exact XNU commit is formally selected. No kernel port, patch set, or device support is claimed.

*Project: MotoDarwin18*
