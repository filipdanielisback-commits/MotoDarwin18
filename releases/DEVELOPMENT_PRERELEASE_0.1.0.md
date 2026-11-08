# MotoDarwin18 — Development Pre-release 0.1.0

<badge>NOT BOOTABLE — NOT FOR INSTALLATION</badge>

Early documentation and feasibility research milestone for Darwin/XNU compatibility research on the Motorola Moto G60 XT2135-2.

## What's included

- Project documentation and source-level research.
- XNU boot ABI, SecureDT, and device-tree compatibility analysis.
- XNULoader menu concept and development pre-release specification.
- Offline source-validation tools and their tests.

## XNULoader menu concept

The proposed future menu labels are:

- Boot iOS 18
- Boot Original Android

These are conceptual labels only. No menu implementation or boot behavior is included.

## Important limitations

- This release does **not** contain XNULoader.
- This release does **not** contain a bootable image or `.img` file.
- This release does **not** contain an XNU kernel port or an iOS 18 implementation.
- Neither iOS 18 nor original Android can be launched through this project at this stage.
- No XT2135-2 target boot or hardware compatibility is claimed.

**Do not attempt to install or flash this release to a device.** It is a source-and-documentation snapshot for development and research only.

## Validation

The repository includes offline validation scripts and a GitHub Actions workflow. Refer to the actual workflow run associated with the selected source commit for CI status. Passing source-level checks does not demonstrate device compatibility.

## Licensing

The repository's license applies only to original project material covered by it. Third-party source, trademarks, firmware, restore images, and proprietary operating-system components remain subject to their respective rights and licenses.

## Source

Create the release from the exact reviewed repository commit/tag. GitHub-generated source archives are source snapshots, not device images.
