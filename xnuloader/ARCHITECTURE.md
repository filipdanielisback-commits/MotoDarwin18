# Loader Architecture — Conceptual Overview

**Project:** MotoDarwin18  
**Status:** Documentation and feasibility research only  
**Target:** Motorola Moto G60 XT2135-2

## Purpose

This document describes the conceptual responsibilities and boundaries of a loader in an operating-system research project. It is not an implementation specification, executable boot procedure, or guide to changing a device.

## Conceptual layers

| Layer | Responsibility | MotoDarwin18 status |
|---|---|---|
| Platform firmware | Provides the documented execution environment and platform services | Exact target interface unknown |
| Loader environment | Represents the loader's own execution context and available services | Not established |
| Image description | Describes the kernel artifact and its metadata | No supported target image contract established |
| Platform information | Represents hardware and memory information expected by the kernel | Target information incomplete |
| Handoff boundary | Defines which component owns which resources and information | No target handoff contract established |
| XNU kernel | Initializes its own subsystems and platform support | No Moto G60 kernel support claimed |
| User space | Provides services and applications above the kernel | Separate compatibility research required |

## Separation of concerns

A future architecture review should keep these topics distinct:

1. **Generic loader concepts:** image metadata, validation results, error reporting, and documented interface boundaries.
2. **Firmware-specific behavior:** services and conventions defined by the actual firmware environment.
3. **Device-specific information:** board identity, memory description, peripheral inventory, and platform configuration.
4. **Kernel expectations:** information and services required by the exact XNU source revision being evaluated.
5. **User-space requirements:** components outside the loader and kernel boundary.

A design that works in one firmware environment cannot be assumed to work in another.

## Information ownership

A conceptual design must identify which component is authoritative for each item of information, who may modify it, and how its lifetime is defined. This is especially important for memory descriptions, device descriptions, image metadata, and diagnostic output.

No Moto G60-specific ownership or handoff behavior has been verified.

## Error reporting

Research documentation should distinguish at least these categories:

- unsupported environment;
- missing or incomplete platform information;
- unsupported image format;
- incompatible interface version;
- validation failure;
- insufficient documented capability;
- unknown or unclassified condition.

These are documentation categories, not implemented error codes.

## Relationship to XNU

Apple's XNU README identifies `libsa` as kernel bootstrap code and `pexpert` as platform-specific code. These are internal XNU source areas; their existence does not define an external loader ABI for an unrelated handset.

Reference: [Apple XNU source repository](https://github.com/apple-oss-distributions/xnu).

## Current conclusion

The loader's actual firmware environment, image contract, platform-information format, and relationship to the target kernel remain unknown. The project is not ready to claim or publish a working loader.
