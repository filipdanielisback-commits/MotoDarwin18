# Device Unknowns — Moto G60 XT2135-2

**Status:** Open research register  
**Scope:** Hardware and platform facts not yet established for the exact target model.

## Purpose

Track unknowns that affect a future Darwin/XNU compatibility assessment. An unknown must remain unknown until supported by a reliable source. Do not infer handset implementation from a SoC feature list.

## Open questions

| Area | Unknown | Evidence needed | Status |
|---|---|---|---|
| Board | Exact board revision and component population | Model-specific primary documentation | Open |
| Boot | Documented boot architecture and firmware interfaces | Public platform documentation | Open |
| CPU | Exact CPU topology and exposed platform description | Device-specific evidence | Open |
| Interrupts | Interrupt-controller configuration and routing | Public hardware documentation | Open |
| Timers | Platform timer interfaces | SoC/platform documentation | Open |
| Memory | Physical memory map and reserved regions | Reliable device-specific documentation | Open |
| Display | Panel, controller, interface, initialization dependencies | Panel/board documentation | Open |
| Touch | Touch controller and bus | Component identification evidence | Open |
| Storage | Storage component and controller details | Device-specific documentation | Open |
| Wireless | Wi-Fi/Bluetooth combo-chip and firmware dependencies | Component documentation | Open |
| Audio | Codec, amplifier, and routing | Component documentation | Open |
| Cameras | Sensor part numbers and bus topology | Camera/module documentation | Open |
| Power | PMIC, regulators, clocks, and power domains | Platform documentation | Open |
| Sensors | Exact sensor models and bus connections | Component documentation | Open |
| USB | Controller implementation and supported roles | Platform documentation | Open |
| Thermal | Thermal sensors and cooling policy interfaces | Device-specific evidence | Open |

## Evidence record template

For every resolved item, record:

- **Claim:**
- **Exact model/revision scope:**
- **Source title and URL:**
- **Source date or access date:**
- **Evidence excerpt or summary:**
- **Confidence:** Confirmed / Probable / Unverified
- **Limitations:**

## Evidence rules

1. Prefer Motorola, Qualcomm, Android Open Source Project, and component-vendor documentation.
2. Distinguish SoC capability from what Motorola implemented in this handset.
3. Do not copy specifications from XT2135-1 to XT2135-2 without evidence that they match.
4. Do not treat forum posts or device-tree guesses as confirmed hardware facts.
5. Keep proprietary firmware and undocumented interfaces clearly marked.
6. Do not claim that resolving a hardware unknown establishes XNU compatibility.

## Current conclusion

The public-facing specifications identify the broad Snapdragon 732G platform and several handset features, but they do not provide a complete board-level inventory. This register remains open.

*Project: MotoDarwin18*
