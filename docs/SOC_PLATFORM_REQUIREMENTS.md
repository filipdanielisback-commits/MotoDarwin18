# Snapdragon 732G Platform Requirements — Research Checklist

**Project:** MotoDarwin18  
**Target handset:** Motorola Moto G60 XT2135-2  
**SoC family:** Qualcomm Snapdragon 732G (SM7150-AC)  
**Status:** Research checklist; no device-specific implementation is established.

## 1. Purpose and scope

This document translates publicly described Snapdragon 732G capabilities and general ARM64 platform concepts into questions that must be answered before meaningful Darwin/XNU platform work can be assessed.

It is not a boot guide, device-modification procedure, driver implementation, or claim of compatibility. A feature listed in a Qualcomm platform brief is not proof that Motorola exposed it in the XT2135-2 handset.

## 2. Evidence categories

Use these labels throughout this document:

- **Platform fact:** explicitly stated in an official SoC or architecture source.
- **Handset fact:** tied by reliable evidence to the exact Moto G60 XT2135-2.
- **Open question:** relevant detail not established by available evidence.
- **Requirement:** a class of information or support a future port would need to evaluate.
- **Not claimed:** no implementation or compatibility evidence exists.

## 3. Processor and execution architecture

### Publicly documented platform facts

Qualcomm's Snapdragon 732G product brief identifies:

- Qualcomm Kryo 470 octa-core CPU
- CPU clock speed up to 2.3 GHz
- 64-bit architecture
- Qualcomm Adreno 618 GPU
- Platform part number SM7150-AC

Source: Qualcomm Snapdragon 732G product brief and product page (see References).

### Research requirements

Before evaluating kernel compatibility, research must establish from authoritative sources:

- The exact CPU core topology and revision exposed by the target handset.
- Which architectural features are implemented and available at the relevant privilege levels.
- The platform's documented exception-level and firmware handoff model.
- Any required CPU initialization and coherency assumptions.
- Whether the chosen XNU source revision supports the required ARM64 execution environment.

**Open:** The Qualcomm marketing brief is not a complete programming reference for CPU initialization, firmware interfaces, or the XT2135-2 board.

## 4. Memory architecture

### Publicly documented platform facts

Qualcomm's product brief lists support for LPDDR4/4X memory, a two-by-16-bit memory interface, and memory speed up to 1866 MHz. These are platform capabilities, not confirmation of the exact memory population or physical address map in this handset.

### Research requirements

A credible platform assessment needs trustworthy information about:

- Installed RAM configuration for the exact unit.
- Physical memory ranges and reserved regions.
- Firmware-reserved memory and shared-memory areas.
- Memory attributes and cache-coherency expectations.
- Any memory-mapped I/O regions relevant to platform support.
- Address translation and I/O memory-management requirements.

**Open:** The exact XT2135-2 physical memory map and reserved regions are not established in this repository.

## 5. Interrupt architecture

### General architecture context

Arm's Generic Interrupt Controller (GIC) architecture describes interrupt prioritization and delivery to processor cores. The exact GIC generation, integration, register interface, interrupt assignments, and routing for this handset must not be guessed from the CPU or SoC family name.

### Research requirements

- Identify the interrupt-controller implementation from reliable platform documentation.
- Establish the supported architecture version and integration details.
- Document interrupt routing and per-core behavior from authoritative evidence.
- Identify how platform devices and timers are represented to the operating system.
- Determine whether the selected XNU baseline has the required interrupt-controller support or would need a separately reviewed platform adaptation.

**Open:** No exact interrupt-controller model or XT2135-2 interrupt map is confirmed.

## 6. Timers and timekeeping

Arm documents a Generic Timer architecture for Arm systems. That general architecture does not prove which timer interfaces, frequencies, or firmware-provided descriptions are available on the Moto G60.

### Research requirements

- Identify the timer facilities actually exposed by the platform.
- Establish documented timer frequency and counter properties.
- Understand per-core timer behavior and interrupt integration.
- Determine the timekeeping and scheduling assumptions of the selected XNU revision.

**Open:** The target handset's exact timer configuration and platform description are not documented here.

## 7. Firmware and platform description

A kernel requires an accurate description of the hardware and a well-defined relationship with the platform firmware. ARM64 capability alone does not identify the boot firmware, handoff protocol, memory reservations, or device description used by this handset.

### Research requirements

- Find authoritative public documentation for the platform firmware interfaces.
- Identify the format and provenance of any hardware description used by the operating system.
- Establish which devices and memory regions are described and how interrupts are represented.
- Record which services remain owned by firmware or vendor components.
- Distinguish documented interfaces from assumptions based on other Snapdragon devices.

**Open:** No supported Moto G60 Darwin/XNU firmware handoff or boot path has been established.

## 8. Storage and peripheral buses

The handset inventory lists storage, USB, display, touch, audio, wireless, camera, and sensor areas whose exact controller and component details remain unknown.

### Research requirements

For each subsystem, record:

- Exact controller or component identity, if verified.
- Bus/interface type and publicly documented integration details.
- Required firmware or vendor-specific dependencies.
- Whether a suitable upstream XNU driver or documented interface exists.
- Whether the feature is essential for initial platform evaluation or can be deferred.

Do not infer the handset's controller from a general SoC feature list. Do not treat a Qualcomm platform capability as evidence that a specific external component is fitted.

## 9. Power, clocks, and thermal management

A mobile platform depends on coordinated power, clock, reset, and thermal management. The exact PMIC, regulators, clock tree, power domains, and thermal sensors for XT2135-2 remain unknown.

### Research requirements

- Identify publicly documented power-management interfaces.
- Determine which platform components manage clocks and power states.
- Record thermal-monitoring and throttling dependencies.
- Identify firmware-owned services and vendor-specific interfaces.
- Avoid assuming that a generic ARM64 kernel can safely manage handset power states without board-specific evidence.

## 10. Graphics and display

Qualcomm lists Adreno 618 graphics and platform-level display capabilities. The Moto G60 inventory separately records a 6.8-inch 1080 × 2460 display. Neither fact establishes a usable XNU graphics or display path.

### Research requirements

- Separate display-panel output from GPU acceleration.
- Identify the actual panel, display controller, and interface.
- Determine which initialization and firmware dependencies are documented.
- Assess graphics support independently from basic display output.
- Record proprietary driver or firmware dependencies without copying restricted binaries into this repository.

## 11. XNU evaluation checklist

The following are evaluation questions, not claims of existing support:

| Area | Requirement to investigate | Current status |
|---|---|---|
| ARM64 CPU | Confirm supported execution features and platform assumptions | Open |
| Early platform setup | Identify documented firmware handoff and platform description | Open |
| Memory | Establish physical map and reserved regions | Open |
| Interrupts | Identify controller architecture and routing | Open |
| Timers | Identify counter, timer, and interrupt interfaces | Open |
| Console/output | Determine whether any documented early output path exists | Open |
| Storage | Identify controller and required dependencies | Open |
| Display | Identify panel and display pipeline | Open |
| Power/thermal | Identify power, clock, and thermal interfaces | Open |
| Peripherals | Inventory buses, controllers, and firmware dependencies | Open |
| User space | Separately assess open-source and proprietary components | Open |

## 12. Research priorities

Recommended documentation-first order:

1. Verify the exact target model and SoC identity.
2. Find primary Qualcomm documentation for the platform and distinguish it from handset-specific facts.
3. Identify authoritative public information about the ARM64 platform architecture.
4. Keep all unverified board-level details in `DEVICE_UNKNOWNS.md`.
5. Select and pin an upstream XNU source revision only after reviewing its architecture and licensing.
6. Compare requirements against source documentation without claiming support from an architectural match alone.

## 13. Sources

1. Qualcomm, [Snapdragon 732G Mobile Platform](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform).
2. Qualcomm, [Snapdragon 732G Mobile Platform Product Brief (PDF)](https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/qualcomm-snapdragon-732g-mobile-platform-product-brief.pdf).
3. Qualcomm, [Snapdragon 732G announcement, 30 August 2020](https://www.qualcomm.com/news/releases/2020/08/qualcomm-announces-snapdragon-732g-improve-high-tier-mobile-gaming).
4. Arm, [Generic Interrupt Controller architecture overview](https://support.arm.com/documentation/den0013/0400/Interrupt-Handling/The-Generic-Interrupt-Controller).
5. Arm, [AArch64 Generic Timer guide (PDF)](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Generic%20Timer.pdf).
6. Apple, [XNU source repository and README](https://github.com/apple-oss-distributions/xnu).
7. MotoDarwin18, [Device Hardware Inventory](DEVICE_INVENTORY.md).
8. MotoDarwin18, [Device Unknowns Register](DEVICE_UNKNOWNS.md).
9. MotoDarwin18, [General Platform Integration Requirements](PLATFORM_REQUIREMENTS.md).

## 14. Current conclusion

The Snapdragon 732G product brief establishes broad platform capabilities, including a 64-bit Kryo 470 CPU, Adreno 618 GPU, LPDDR4/4X support, and related multimedia/connectivity features. It does not provide the complete board-level documentation required for a Moto G60 port.

The exact interrupt controller, timer configuration, memory map, firmware handoff, peripheral controllers, power architecture, and device-specific dependencies remain open research questions.

**Project status:** Documentation and feasibility research only. No Moto G60 XNU kernel, bootloader, device tree, or driver implementation is claimed.

*Last updated: 2026-11-08*  
*Project: MotoDarwin18*  
*Document: SOC_PLATFORM_REQUIREMENTS.md*
