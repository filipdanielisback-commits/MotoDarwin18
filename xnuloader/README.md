# XNU Loader Research Area

This directory is reserved for an independently developed loader component for MotoDarwin18.

**Status:** documentation scaffold only. There is no working loader, firmware integration, boot protocol implementation, or Moto G60 boot support in this directory.

## Planned layout

- `src/` — original loader implementation, if and when a design is validated.
- `include/` — project-owned interfaces and shared declarations.
- `scripts/` — non-destructive build, static validation, and packaging helpers.

## Responsibilities to research

The loader's eventual responsibilities and interfaces must be established from authoritative platform documentation. Research topics may include:
- execution environment and firmware interface assumptions;
- memory map and handoff contract;
- kernel image format and metadata;
- serial/logging design for development builds;
- clear separation between generic loader logic and device-specific platform support.

These are research topics, not implemented capabilities.

## Safety boundaries

This repository scaffold does not provide device boot instructions or commands that change boot configuration, unlock a bootloader, write firmware, or modify partitions. Early work should be limited to documentation, code review, static checks, and suitable emulated or otherwise non-destructive test environments.

## Licensing and provenance

Write original code or use dependencies whose licenses have been reviewed. Keep a record of source origins and notices. Do not assume HakiOS's loader license automatically applies to any copied or adapted code; review the exact files and their history before reuse.

## Current limitations

A loader alone cannot make XNU compatible with a device. A supported kernel, platform initialization, memory and interrupt handling, and appropriate drivers would also be required. Moto G60 XT2135-2 support is not established.
