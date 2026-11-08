# XNU Additional Source Files

This directory is reserved for original MotoDarwin18 source files proposed for addition to an upstream XNU source tree.

**Current status:** no kernel source files are implemented here.

## Required record for every file

Document the following before adding a source file:

| Field | Required information |
|---|---|
| File name | Repository-relative path |
| Intended upstream destination | Proposed XNU path |
| Purpose | Problem the file is intended to address |
| Author and origin | Original author and any source material |
| Dependencies | Headers, APIs, configuration, or other components |
| Target scope | Exact device evidence or generic architecture scope |
| License | Applicable license and required notices |
| Validation | Checks completed and outstanding |
| Limitations | Known assumptions and unsupported behavior |

## Rules

- Keep original project files distinct from copied upstream files.
- Do not copy vendor or third-party source without documented permission and provenance.
- Preserve applicable copyright and license notices.
- Do not add proprietary firmware, restore images, keys, credentials, or personal device data.
- Do not claim a driver works because a matching component name appears in a SoC specification.
- Keep proposed changes small enough to review independently.

Use [the compatibility matrix](../COMPATIBILITY_MATRIX.md) to link each proposed file to the evidence and subsystem it addresses.
