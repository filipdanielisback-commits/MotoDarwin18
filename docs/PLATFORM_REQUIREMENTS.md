# Platform integration requirements

This document describes the broad classes of platform support a Darwin/XNU-based system would need. It is an architectural checklist, not a device-modification or boot procedure.

**Project status:** research only. MotoDarwin18 does not currently claim a working kernel, boot path, or iOS userland on Moto G60 XT2135-2.

## Why CPU compatibility is not enough

ARM64 support at the instruction-set level is only one prerequisite. A usable operating-system port also needs a compatible platform description, early platform initialization, memory and interrupt management, timers, storage, input/output, power management, and drivers for the target board.

Apple's XNU source tree separates generic kernel subsystems from platform-specific code. Its README identifies areas such as Mach subsystems, BSD subsystems, bootstrap code, IOKit, and platform-expert code. See the references below.

## Platform areas to investigate

| Area | Research question | Why it matters |
|---|---|---|
| CPU and execution state | Which ARM64 features and execution assumptions are required? | Establishes the processor-level baseline. |
| Memory map | What RAM ranges and reserved regions exist? | The kernel must understand usable and reserved memory. |
| Interrupts | Which interrupt controller and routing model are present? | Devices and timers rely on interrupt delivery. |
| Timers and clocks | Which architectural and platform timers are available? | Scheduling and timekeeping depend on reliable clocks. |
| Platform description | What authoritative board description exists? | Hardware resources must be described accurately. |
| Storage | Which controller and storage interfaces are present? | Persistent data and system volumes need a supported path. |
| Display and input | Which display, touch and button components are fitted? | A usable system needs output and input support. |
| Power and thermal | Which controllers manage power, charging and temperature? | Incorrect assumptions can cause instability or unsafe operation. |
| Connectivity | Which wireless and modem components are fitted? | Connectivity depends on device-specific firmware and interfaces. |
| Audio and sensors | Which codecs, sensors and buses are used? | These are separate integration tasks, not automatic SoC features. |

## Evidence rules

For every entry, record:
- whether the evidence is for the exact XT2135-2 board or only the Snapdragon 732G family;
- source title, publisher, version/date and URL;
- confidence level and any contradictory evidence;
- whether the interface is documented publicly;
- whether proprietary firmware or other restricted inputs are involved.

Do not infer a complete board design from a chipset product brief.

## Architecture reference

The public XNU repository describes platform-specific code in the platform-expert area and documents distinct kernel subsystems. Independent ARM64 porting documentation also illustrates that device-specific configuration and drivers are separate from shared kernel code. These sources are useful architectural context, not evidence that Moto G60 is supported.

## References

- Apple, [XNU source repository and README](https://github.com/apple-oss-distributions/xnu).
- UniXNU, [Port a device: input inventory overview](https://unixnu.com/porting/steps).
- UniXNU, [Architecture overview](https://unixnu.com/porting/).

