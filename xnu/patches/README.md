# XNU Patch Series

This directory is reserved for MotoDarwin18-authored patch files against one explicitly pinned upstream XNU revision.

**Current status:** no patches are present.

## Before proposing a patch

A patch proposal must include:

- Exact upstream repository and commit hash.
- A concise problem statement and the subsystem affected.
- Evidence that the issue applies to the Moto G60 XT2135-2 rather than merely to another device using a related SoC.
- A description of the proposed change and its limitations.
- File-level provenance and license review.
- Validation performed and validation not yet possible.

## Patch quality rules

- Keep each patch focused and independently reviewable.
- Do not silently mix unrelated changes.
- Preserve upstream copyright and license notices.
- Mark modifications as required by the applicable license.
- Do not import patches from HakiOS or another project without reviewing the exact source, author, license, and compatibility.
- Do not include proprietary firmware, keys, binaries, or personal data.

## Suggested naming convention

Use descriptive names with a stable sequence, for example:

`0001-subsystem-short-description.patch`

The name is illustrative; it does not indicate that a patch exists or has been validated.

## Review status vocabulary

- **Draft:** incomplete proposal.
- **Needs evidence:** target-device applicability is not established.
- **Review required:** technical or license review is pending.
- **Validated in source tests:** specified non-device checks passed.
- **Not device-validated:** no claim of hardware operation.
- **Rejected:** proposal should not be used.

A patch must not be described as Moto G60 support unless evidence and appropriate validation justify that statement.
