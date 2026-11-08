# Research Build Environment

**Status:** Initial planning document  
**Scope:** Host-side documentation, source review, and non-destructive research.

## Known project requirements

The current project requirements document specifies:

- Windows 10 or Windows 11
- WSL2 managed from Windows PowerShell
- At least 6 GB RAM
- Motorola Moto G60, exact model XT2135-2

These are project planning requirements, not a claim that a complete build environment or device toolchain has been validated.

## Intended early workflow

The initial environment is intended for:

1. Reading upstream source and license notices.
2. Maintaining project documentation.
3. Reviewing source changes and provenance.
4. Running static checks on documentation and project metadata.
5. Exploring architecture concepts without changing a physical device.
6. Using emulation or other isolated research environments where appropriate.

## Environment details to record

| Item | Current status |
|---|---|
| Host OS | Windows 10 or Windows 11 |
| Linux environment | WSL2 |
| RAM | At least 6 GB |
| Target model | Motorola Moto G60 XT2135-2 |
| Compiler/toolchain versions | Not selected |
| SDK versions | Not selected |
| XNU source commit | Not selected |
| Emulator configuration | Not selected |
| Reproducible build procedure | Not established |

## Reproducibility record

When tools are selected, record:

- Tool name and exact version
- Official download or documentation source
- Host and guest OS versions
- Relevant configuration files
- Build or validation command purpose
- Expected output
- Known limitations

Do not record a build as successful unless its output has actually been produced and checked.

## Scope and safety

At this stage, keep work to documentation, source review, static validation, and isolated or emulated experiments. This document does not provide instructions for unlocking, flashing, erasing, or otherwise changing the phone.

## Current status

The host environment is specified at a high level. A validated compiler, SDK, kernel build configuration, and reproducible build have not yet been established.

*Project: MotoDarwin18*
