# Source provenance and licensing policy

MotoDarwin18 is an independent research project. Every source file, binary, firmware component, document, and dataset considered for the project must have a known origin and a clear basis for use.

## Core principles

1. **Prefer primary sources.** Use upstream repositories, vendor documentation, standards, and official release notes where possible.
2. **Record provenance.** Note where an artifact came from, who published it, its version or commit, and its license or terms.
3. **Do not assume public availability means unrestricted reuse.** A downloadable file may still be copyrighted or subject to contractual restrictions.
4. **Keep proprietary inputs out of this repository.** Do not commit restore images, firmware blobs, private keys, credentials, or other materials unless redistribution rights are explicit and verified.
5. **Separate source code from binary inputs.** Open-source XNU does not make every component of an Apple operating system open source.
6. **Preserve notices.** When reuse is permitted, retain required copyright notices, license texts, and attribution.

## Provenance record template

Use this template when evaluating a new input:

| Field | Value |
|---|---|
| Name | |
| Publisher / author | |
| Original URL | |
| Version / release / commit | |
| Date accessed | |
| Artifact type | Source / binary / firmware / documentation / dataset |
| License or terms | |
| Redistribution permitted? | Yes / No / Unclear |
| Modifications made | |
| Project use | |
| Review notes | |

## License review questions

- Is the license included with the exact version being used?
- Does it permit modification and redistribution?
- Are attribution, notice, source-disclosure, or patent terms relevant?
- Are there separate terms for firmware, trademarks, SDKs, or bundled components?
- Is the project allowed to publish the resulting artifact, or only describe the research?
- Are any third-party contributions governed by different terms?

If any answer is unclear, mark the item **Unreviewed** and do not redistribute it.

## Repository boundary

This repository may contain original documentation, original code, and third-party material only when its license permits the intended use. It should not become a mirror for proprietary iOS files or device firmware.

## Useful starting points

- Apple, [Open Source releases](https://opensource.apple.com/).
- Apple, [XNU source repository](https://github.com/apple-oss-distributions/xnu).
- GitHub, [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

This policy is project guidance, not legal advice. When rights are uncertain, omit the material and seek qualified guidance.
