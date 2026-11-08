# XNU Baseline Research

**Status:** Provisional research baseline pinned; build feasibility and target compatibility not yet demonstrated.

## Purpose

Record the upstream XNU revision MotoDarwin18 will evaluate first. Selecting a source baseline is a research decision, not evidence of compatibility with the Motorola Moto G60 XT2135-2.

## Primary upstream source

- Apple open-source XNU repository: https://github.com/apple-oss-distributions/xnu
- Candidate tag: [xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/tree/xnu-11215.1.10)
- Immutable peeled commit: `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`
- Tag object: `d95cbeef34d1a9cca097b33d385db3b2aae1a755`
- Tag date: 2024-09-24

The tag's upstream README describes XNU as a hybrid kernel combining Mach, BSD components, and IOKit. It explicitly lists ARM64 among the supported architectures. These are upstream source facts; they do not establish support for the target handset.

## Why this is the first research baseline

The `xnu-11215.1.10` tag is a useful iOS 18-era source candidate: it is an immutable Apple OSS release tag dated 2024-09-24, close to the iOS 18 release period, and its README documents ARM64 support. It gives the project a reproducible source reference for initial review.

**Important limitation:** This is a project research baseline, not a claim that this exact tag is the kernel build used by a specific iOS 18 release or device. The GitHub tag metadata reports the tag as unsigned. The peeled commit hash is recorded to identify the source tree precisely.

## Build feasibility

The upstream README documents XNU build concepts and Apple SDK/KDK-related build settings. It does not document a supported cross-build or boot path for the Snapdragon 732G / Motorola platform.

Before any target-specific code is attempted, the project must establish:
- A supported host environment for this exact tag.
- Exact SDK/KDK and toolchain prerequisites.
- A reproducible upstream build result or a clear blocker report.
- Which ARM64 source/configuration paths are relevant.
- Which platform interfaces and proprietary dependencies are missing for a non-Apple device.

A successful host build would not mean the kernel can boot on the Moto G60.

## Related project reference

HakiOS project materials have described their XNU base as `xnu-8796.121.2`. This remains a comparison lead only. It is not the selected MotoDarwin18 baseline and does not imply that HakiOS patches or device support are compatible with this project.

- HakiOS repository: https://github.com/oosexgang/hakios-xnu-kernel

## Licensing and provenance

The candidate tag contains an `APPLE_LICENSE` file identifying Apple Public Source License (APSL) 2.0. Check the actual notice in every file being considered; individual files may carry notices that require separate review. The repository's root MIT license does not replace or override file-level licenses.

Do not copy HakiOS implementation files into MotoDarwin18 without reviewing the exact file's origin, license, notices, and compatibility.

## Current decision

Use `xnu-11215.1.10` as the **provisional research baseline** for source review and build-feasibility investigation. Reconsider it if the documented build prerequisites or later compatibility analysis show it is unsuitable.

No MotoDarwin18 kernel implementation, patch set, device boot, or iOS 18 compatibility is claimed.

*Project: MotoDarwin18*
