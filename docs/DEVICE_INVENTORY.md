Moto G60 XT2135-2 — Device Hardware Inventory

Project: MotoDarwin18
Target device: Motorola Moto G60
Exact model: XT2135-2
Platform: Qualcomm Snapdragon 732G
Status: Initial research — not all components independently verified

1. Purpose

This document records publicly documented hardware information for the Motorola Moto G60 XT2135-2.

The inventory will help identify which hardware components and platform interfaces would need investigation for Darwin/XNU compatibility research.

A specification listed here does not mean that a working XNU driver exists.

2. Main Platform

Component| Reported specification| Research status
SoC| Qualcomm Snapdragon 732G| Publicly documented
CPU| Qualcomm Kryo 470, up to 2.3 GHz| SoC-level specification
GPU| Qualcomm Adreno 618| SoC-level specification
AI/DSP| Qualcomm Hexagon 688| SoC-level specification
Cellular platform| Qualcomm X15 LTE modem| SoC-level specification
Memory support| LPDDR4/LPDDR4X platform support| SoC-level capability; device configuration needs verification
Operating system at launch| Android 11| Publicly documented

3. Display

Component| Reported specification| Research status
Display size| 6.8 inches| Publicly documented
Display technology| IPS LCD| Publicly documented
Resolution| 1080 × 2460| Publicly documented
Display controller| Unknown| Requires investigation
Panel identification| Unknown| Requires investigation
Display interface| Unknown| Requires investigation

4. Memory and Storage

Component| Reported specification| Research status
RAM configuration| 6 GB configuration reported| Verify exact regional variant
Internal storage| 128 GB configuration reported| Verify exact regional variant
microSD support| Reported| Publicly documented
Storage controller| Unknown| Requires investigation
Storage component manufacturer| Unknown| Requires investigation

5. Cameras

Camera| Reported specification
Main rear camera| 108 MP
Ultra-wide rear camera| 8 MP
Macro rear camera| 2 MP
Front camera| 32 MP

The exact camera sensor models, camera interfaces, ISP configuration, and firmware dependencies remain unverified.

6. Wireless Connectivity

Component| Reported specification| Research status
Cellular| LTE| Publicly documented
Wi-Fi| Wi-Fi 5 reported for the handset| Device-level specification
Bluetooth| Bluetooth 5.0 reported for the handset| Device-level specification
NFC| Reported| Verify regional configuration
GPS/GNSS| Supported| Exact implementation unknown

Important: Snapdragon platform capability lists may advertise features that a particular handset does not implement. Device-level specifications must take priority when documenting the actual XT2135-2.

7. Power and Battery

Component| Reported specification| Research status
Battery capacity| 6000 mAh| Publicly documented
Charging| Fast charging support reported| Exact implementation needs verification
PMIC| Unknown| Requires investigation
Power-management interfaces| Unknown| Requires investigation

8. Sensors and Other Components

The following components require exact identification from reliable device-specific sources:

- Accelerometer
- Gyroscope
- Magnetometer
- Proximity sensor
- Ambient-light sensor
- Fingerprint reader
- Audio codec
- Speakers and microphones
- Vibration motor
- USB controller
- Touchscreen controller

No specific chip model should be assumed until it is supported by evidence.

9. XNU Compatibility Research Areas

The following areas are research targets, not completed implementations:

Area| Research objective
CPU initialization| Understand the ARM64 platform requirements
Interrupt controller| Identify the interrupt architecture
Device tree| Investigate available hardware descriptions
Memory management| Document physical memory layout requirements
Timers| Identify platform timer interfaces
Storage| Identify the storage controller and access requirements
Display| Research display hardware and initialization requirements
USB| Identify controller and platform interfaces
Audio| Identify audio hardware and software dependencies
Wireless| Research Wi-Fi and Bluetooth hardware dependencies
Power management| Document power and thermal-management requirements

10. Unknown Hardware Information

The following information is not yet confirmed for the exact XT2135-2:

- Motherboard revision
- Exact display panel and controller
- Exact touchscreen controller
- Wi-Fi/Bluetooth chip identification
- Camera sensor part numbers
- Audio codec identification
- PMIC model
- Storage component model
- Sensor chip models
- GPIO and pin configuration
- Interrupt assignments
- Clock configuration
- Detailed memory map
- Device-specific firmware interfaces

These details should remain marked as unknown until reliable evidence is found.

11. Research Sources

Use primary sources wherever possible:

- "Motorola Support" (https://en-us.support.motorola.com/)
- "Qualcomm Snapdragon 732G" (https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-7-series-mobile-platforms/snapdragon-732g-mobile-platform)
- "Qualcomm Product Information" (https://www.qualcomm.com/)
- "Android Open Source Project" (https://source.android.com/)
- "Apple XNU Source Code" (https://github.com/apple-oss-distributions/xnu)

Additional sources should be recorded with their URLs, publication dates where available, and the claims they support.

12. Current Assessment

The Snapdragon 732G provides an ARM64-capable platform, but that alone does not establish compatibility with Darwin/XNU.

The exact motherboard configuration, hardware interfaces, boot architecture, firmware dependencies, and required drivers remain research topics.

Current project status: Hardware research and documentation only. No working Moto G60 Darwin/XNU port or device-specific driver support is claimed.

---

Last updated: 2026-11-08
Project: MotoDarwin18
Document: DEVICE_INVENTORY.md
