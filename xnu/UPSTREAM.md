# XNU Upstream Source Record

**Project:** MotoDarwin18  
**Upstream project:** Apple open-source XNU  
**Repository:** https://github.com/apple-oss-distributions/xnu  
**Status:** Provisional research baseline pinned; target compatibility not established.

## Why upstream provenance matters

MotoDarwin18 must identify exactly which upstream source it studies. A moving branch such as `main` is useful for browsing but is not a reproducible source baseline.

## Provisional source baseline

| Field | Value |
|---|---|
| Upstream repository | https://github.com/apple-oss-distributions/xnu |
| Tag | `xnu-11215.1.10` |
| Tag object | `d95cbeef34d1a9cca097b33d385db3b2aae1a755` |
| Peeled commit | `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585` |
| Tag date | 2024-09-24 |
| Source URL | https://github.com/apple-oss-distributions/xnu/tree/xnu-11215.1.10 |
| README | https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/README.md |
| License file | https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/APPLE_LICENSE |
| Tag signature status | GitHub tag object reports unsigned |
| Project role | Provisional research baseline for an iOS 18-era XNU study |
| MotoDarwin18 modifications | None recorded |

The tag is an official Apple OSS repository tag and its README documents ARM64 among the supported XNU architectures. The tag date and version make it a useful iOS 18-era research candidate. This does **not** prove it is byte-for-byte the XNU build used by any particular iOS 18 device release, nor does ARM64 support imply Motorola platform support.

The tag is unsigned according to GitHub's tag metadata. The peeled commit hash is recorded so source references remain immutable; this record does not claim a cryptographic signature verification.

## Why this baseline is provisional

- The project needs a stable, iOS 18-era XNU source reference before subsystem work can be compared consistently.
- The upstream README's ARM64 statement is architecture-level evidence only.
- The documented build examples refer to Apple SDK/KDK build environments and do not establish a supported cross-build for this Motorola target.
- Private Apple platform drivers, firmware, boot integration, and proprietary iOS userland are not supplied by the public XNU source tree.
- The project has not yet reproduced an upstream build using this exact tag.

## Source tree orientation

The upstream README describes, among others:

- `osfmk/` — Mach kernel subsystems.
- `bsd/` — BSD subsystems.
- `iokit/` and `libkern/` — driver framework and supporting kernel code.
- `pexpert/` — platform-specific code.
- `libsa/` — kernel bootstrap code.
- `config/`, `makedefs/`, and `SETUP/` — configuration and build support.
- `tools/` — development and debugging utilities.

This is a map for reading upstream documentation. It does not identify which components must change for Moto G60.

## Next validation checklist

- [ ] Reproduce the tag's documented build in an appropriate supported host environment.
- [ ] Record exact SDK/KDK, compiler, and tool versions required by this tag.
- [ ] Review ARM64-specific source and configuration boundaries relevant to the intended target.
- [ ] Compare the baseline against the known Snapdragon 732G platform requirements.
- [ ] Decide whether this tag remains the project baseline after build feasibility is understood.
- [ ] Review the license notices for each file considered for reuse.

## License and redistribution

The tag contains an `APPLE_LICENSE` file identifying Apple Public Source License (APSL) 2.0. Individual source files may contain additional or different notices; inspect every file before reuse. Preserve required notices and document modifications. The root MIT license in MotoDarwin18 does not replace upstream file licenses.

No upstream XNU source is copied into this directory by this document.

## References

- Apple, [XNU source tag xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/tree/xnu-11215.1.10).
- Apple, [tag README](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/README.md).
- Apple, [APSL license file](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/APPLE_LICENSE).
- MotoDarwin18, [XNU baseline research](../docs/XNU_BASELINE.md).
- MotoDarwin18, [source provenance policy](../docs/SOURCE_PROVENANCE.md).
