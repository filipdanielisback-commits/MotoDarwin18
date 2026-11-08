# Qualcomm Snapdragon 732G — Research Note

**Target handset:** Motorola Moto G60 XT2135-2  
**Status:** Platform-level overview; not a board inventory.

## Purpose

Collect platform facts relevant to later compatibility research while avoiding assumptions about the exact phone implementation.

## Public platform references

- Qualcomm product information: https://www.qualcomm.com/
- Snapdragon 732G product page: https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-7-series-mobile-platforms/snapdragon-732g-mobile-platform
- MotoDarwin18 device inventory: ../../docs/DEVICE_INVENTORY.md

## Reported platform components

The Snapdragon 732G is publicly described as an ARM64-capable mobile platform and is associated with:

- Qualcomm Kryo 470 CPU
- Qualcomm Adreno 618 GPU
- Qualcomm Hexagon 688 processing components
- Qualcomm X15 LTE modem
- Qualcomm FastConnect connectivity subsystem
- Qualcomm Spectra image signal processor

Exact feature availability can depend on the OEM design and selected configuration.

## Relevance to Darwin/XNU research

The SoC name and CPU architecture are only a starting point. A platform assessment also needs reliable information about:

- Boot and firmware interfaces
- CPU topology and initialization assumptions
- Interrupt controller and timer interfaces
- Physical memory layout
- Power and clock management
- Storage and peripheral controllers
- Device-specific firmware dependencies

This note does not identify all components on the Moto G60 motherboard and does not establish XNU support.

## Evidence policy

For every additional platform claim, record the exact Qualcomm document or other primary source supporting it. Avoid copying maximum platform capabilities into the handset inventory as if they were confirmed phone specifications.

*Project: MotoDarwin18*
