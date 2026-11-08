# Glossary

Short definitions for terms used in MotoDarwin18 documentation.

| Term | Meaning |
|---|---|
| ARM64 / AArch64 | The 64-bit execution state and instruction-set architecture used by many modern ARM processors. |
| Boot chain | The sequence of software stages that starts a device and transfers control toward its operating system. |
| Device tree | A structured description of hardware devices and resources, commonly used by some operating-system boot environments. |
| Driver | Software that controls or communicates with a hardware device or controller. |
| Firmware | Low-level software associated with a device or hardware component; it may be proprietary and subject to separate licensing. |
| HAL | Hardware Abstraction Layer: interfaces that help software use hardware without depending on every implementation detail. |
| IPSW | Apple's software package format used for certain Apple-device software and restore images. Its contents may include proprietary material. |
| Kernel | The core part of an operating system responsible for low-level resource and hardware management. |
| Mach | The kernel architecture and abstractions that form part of XNU. |
| SoC | System on a Chip: an integrated package containing major computing and platform components. |
| XNU | The open-source kernel used by Apple's operating systems; the name is commonly expanded as “X is Not Unix.” |
| Userland | Programs, libraries, services and tools that run outside the kernel. |
| DriverKit | Apple's framework for developing certain device drivers in a more isolated environment; it does not mean arbitrary Android drivers can run under XNU. |
| Secure boot | A process that checks software authenticity or integrity during startup. Details vary by device and implementation. |

## Important distinctions

- **XNU is not all of iOS.** iOS also contains proprietary frameworks, services, drivers, firmware and applications.
- **A chipset datasheet is not a board description.** It documents platform capabilities, not necessarily the exact components or wiring in one phone.
- **A successful build is not a successful boot.** Build compatibility, boot compatibility, hardware support and userland compatibility are separate milestones.
- **An IPSW is not a generic source-code archive.** It may contain proprietary binaries and other material governed by Apple's terms and applicable law.
