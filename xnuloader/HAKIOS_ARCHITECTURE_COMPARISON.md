# HakiOS XNULoader Architecture Comparison

**Project:** MotoDarwin18  
**Target under study:** Motorola Moto G60 XT2135-2  
**Status:** Source and documentation analysis only  
**Implementation status:** No MotoDarwin18 loader implementation exists

## Purpose

This document studies the public architecture of HakiOS to identify reusable *design concepts* for an independently authored MotoDarwin18 loader. It does not copy HakiOS source, define a device boot procedure, or establish that HakiOS firmware or loader components are compatible with the Moto G60.

The project goal is a genuine, phone-resident loader if feasibility can eventually be demonstrated. A mock-up must never be presented as an operational loader.

## HakiOS architecture observed

The public HakiOS documentation describes distinct responsibilities:

| Layer | HakiOS role | MotoDarwin18 assessment |
|---|---|---|
| Device startup environment | Device-specific firmware environment | Moto G60 environment and supported interfaces are not established |
| Firmware integration | HakiOS changes around a Mu-Silicium-based UEFI environment, with device-specific platform material | No Moto G60 firmware integration exists |
| Loader application | A UEFI application commonly referred to as XNULoader | No MotoDarwin18 loader implementation exists |
| Kernel | HakiOS's XNU port and platform drivers | MotoDarwin18 has source research, not a port |
| User space | Separate Darwin user-space components | iOS 18 user-space compatibility is not established |

HakiOS's documentation also describes a U-Boot alternative to its UEFI environment. This demonstrates that the firmware/loader boundary is a separate architectural choice, not something that can be assumed for another handset.

## Loader responsibilities identified in the public reference

At a conceptual level, HakiOS's loader is responsible for more than drawing a menu. Its documentation and source identify work in these areas:

- recognizing and validating the loader's input payload;
- understanding the kernel image and its metadata;
- preparing the platform description expected by its XNU build;
- defining the kernel handoff information;
- coordinating the transition from the loader environment to the kernel;
- reporting failures and retaining useful diagnostics.

These are observations about HakiOS, not an implementation checklist or instructions for reproducing its phone boot path.

## What is generic and what is device-specific

### Potentially reusable design principles

- Keep the loader, firmware integration, kernel, and user space as separate components.
- Define explicit interfaces between components.
- Treat image metadata and platform information as separately validated inputs.
- Make unsupported states visible rather than silently assuming compatibility.
- Keep diagnostics and provenance reviewable.
- Maintain a clear distinction between a conceptual UI and a functioning loader.

### Not portable by assumption

- Firmware implementation, UEFI protocols, and vendor extensions.
- Device memory layout and resource descriptions.
- Board identity and platform configuration.
- Kernel image conventions and exact handoff contract.
- Device-tree representation and lifetime.
- Interrupt, timer, storage, display, and power services.
- Any firmware binary or proprietary driver.

The HakiOS reference targets a different device and uses its own kernel and platform assumptions. Its implementation is not evidence of Moto G60 compatibility.

## Comparison with MotoDarwin18 research

MotoDarwin18 has already established a provisional XNU source baseline, reviewed selected ARM64 startup consumers, and documented the Apple SecureDT representation expected by that source revision.

The remaining gap is substantial: no exact Moto G60 firmware-to-loader contract has been demonstrated, no complete exact-model memory/platform description is available, and no Moto-specific XNU platform implementation exists.

The shared hanoip/SDMMAGPIE source evidence is useful for research but remains family-level evidence. It does not establish the exact firmware services or board configuration of every XT2135-2 unit.

## Proposed research sequence

1. Maintain a source-cited comparison of the HakiOS component boundaries and MotoDarwin18's existing research.
2. Reconcile the loader's conceptual responsibilities with the pinned XNU source requirements already documented in this repository.
3. Keep each unresolved Moto G60 firmware and hardware assumption explicitly marked unknown.
4. Review source provenance and licensing before considering any implementation.
5. Do not describe a loader as implemented, runnable, or device-compatible without independent evidence for those claims.

This sequence is documentation and source review. It does not involve changing device firmware, boot configuration, partitions, or other device state.

## References

- [HakiOS XNU kernel repository](https://github.com/oosexgang/hakios-xnu-kernel)
- [HakiOS UEFI repository](https://github.com/oosexgang/hakios-uefi)
- [HakiOS device repository for the POCO X5 Pro 5G](https://github.com/oosexgang/hakios-sm7325)
- [HakiOS architecture guide](https://hackios-web.vercel.app/en/docs/concepts/architecture)
- [HakiOS boot-chain overview](https://hackios-web.vercel.app/uk/guide/how-it-works)
- [MotoDarwin18 XNU early platform dependencies](../docs/XNU_EARLY_PLATFORM_DEPENDENCIES.md)
- [MotoDarwin18 Secure Device Tree requirements](../docs/SECURE_DEVICE_TREE_REQUIREMENTS.md)
- [MotoDarwin18 boot ABI compatibility gaps](../docs/BOOT_ABI_COMPATIBILITY_GAPS.md)

## Conclusion

MotoDarwin18 should pursue an original, genuine XNULoader design rather than a fake implementation or a copied HakiOS binary. The HakiOS project is a useful architectural reference, but the Moto G60's firmware and XNU platform contract remain unproven. The current milestone is to close those evidence gaps, not to claim a working loader.
