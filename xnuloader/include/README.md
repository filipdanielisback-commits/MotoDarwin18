# Loader Interfaces

Reserved for project-owned interface declarations and shared data definitions.

**Current status:** no interfaces or headers are defined.

## Before adding an interface

Document:

- interface name and purpose;
- producer and consumer;
- ownership and lifetime of data;
- versioning and compatibility expectations;
- error representation;
- assumptions about architecture and platform;
- source provenance and license.

## Design principles

- Prefer explicit, documented contracts over assumptions.
- Keep platform-specific declarations separate from generic interfaces.
- Do not copy third-party headers without checking provenance and license terms.
- Avoid exposing undocumented firmware details as stable interfaces.
- Do not include secrets, proprietary data, or device-specific personal information.

Any future interface must be reviewed against the selected XNU source baseline. No baseline is currently selected.
