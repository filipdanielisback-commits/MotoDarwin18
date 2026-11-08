# XNU Upstream Source Record

**Project:** MotoDarwin18  
**Upstream project:** Apple open-source XNU  
**Repository:** https://github.com/apple-oss-distributions/xnu  
**Status:** Repository identified; no immutable baseline commit selected.

## Why upstream provenance matters

MotoDarwin18 must be able to identify exactly which upstream source it studies. A moving branch name such as `main` is useful for browsing but is not a reproducible source baseline.

The Apple XNU README describes the kernel's major source areas and general architecture. The README and repository metadata should be checked again when selecting a specific revision.

## Baseline record

| Field | Value |
|---|---|
| Upstream repository | https://github.com/apple-oss-distributions/xnu |
| Branch used for discovery | main |
| Exact commit | Not selected |
| Release/tag | Not selected |
| Retrieval date | 2026-11-08 (research record date) |
| Source archive/checksum | Not recorded |
| License review | Pending for any specific files to be reused |
| MotoDarwin18 modifications | None recorded |

Do not treat this discovery record as a pin or as a vendored copy of upstream source.

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

## Revision selection checklist

- [ ] Review candidate Apple release tags and source commits.
- [ ] Confirm that the candidate is an official Apple source release.
- [ ] Record an immutable commit hash and tag, if applicable.
- [ ] Record retrieval date and source archive identity.
- [ ] Review the license notices for each file considered.
- [ ] Compare the candidate's documented architecture support with project requirements.
- [ ] Record why this revision is preferable to alternatives.
- [ ] Update this file and `docs/XNU_BASELINE.md` before treating it as selected.

## License and redistribution

XNU source files may have file-level Apple Public Source License notices. Check the actual notice in every file being considered. Preserve required notices and document modifications. The root MIT license in MotoDarwin18 does not replace upstream file licenses.

No upstream XNU source is copied into this directory by this document.

## References

- Apple, [XNU source repository](https://github.com/apple-oss-distributions/xnu).
- Apple, [XNU README](https://github.com/apple-oss-distributions/xnu/blob/main/README.md).
- MotoDarwin18, [XNU baseline research](../docs/XNU_BASELINE.md).
- MotoDarwin18, [source provenance policy](../docs/SOURCE_PROVENANCE.md).
