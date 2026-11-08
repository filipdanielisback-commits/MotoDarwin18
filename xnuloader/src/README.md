# Loader Source

Reserved for original MotoDarwin18 source code, if a documented and reviewed design is established in the future.

**Current status:** no implementation is present.

## Entry criteria

Before source code is added, the project must have:

- a reviewed architecture document;
- a clearly scoped, documented interface contract;
- evidence for any platform-specific assumptions;
- a source provenance and licensing record;
- a test plan limited to safe, isolated source-level validation;
- an explicit statement of what the implementation does not support.

## Source organization principles

- Separate generic concepts from device-specific code.
- Keep modules small and independently reviewable.
- Document ownership and error handling.
- Avoid undocumented firmware dependencies.
- Never embed credentials, private keys, proprietary firmware, or personal device data.

This directory is not a place for copied third-party loader code. Review the exact file history, author, license, and notices before considering reuse.
