# Moto G60 Pre-Android Display and Touch Research

**Status:** source research and architecture assessment only. No display or touchscreen driver is implemented. No phone firmware or boot configuration has been inspected or changed.

## 1. Research question

Can a future phone-resident MotoDarwin18 XNULoader display its own interface and accept touchscreen input before Android starts?

The answer depends on two independent services being available in the loader's execution environment:

1. a display service that lets the loader draw pixels;
2. an input service that reports touch contact and coordinates.

A display working in Android does not prove either service is available before Android.

## 2. What is known about the Moto G60 family

The project’s shared Hanoip/SDMMAGPIE source review found:

- a candidate Tianma ILI7807S 678-class 1080x2460 MIPI-DSI panel description in a Hanoi panel include;
- an Ilitek SPI touchscreen node in a Hanoi touchscreen device-tree include;
- family-level display, touch, and platform descriptions that may vary by board revision.

These are **device-family clues**, not a confirmed component inventory for every XT2135-2. They do not establish that the exact phone has that panel/controller combination, nor do they establish the electrical configuration, firmware ownership, or pre-Android driver availability.

The display panel controller and touch controller are separate functional components. The ILI7807S display-panel lead must not be treated as proof that the touch controller is ILI7807S.

The exact XT2135-2 board revision and the touch/display bill of materials remain unresolved.

## 3. The two pre-OS service interfaces

### 3.1 Display: UEFI Graphics Output Protocol (GOP)

The UEFI specification defines Graphics Output Protocol (GOP) as a pre-OS graphics abstraction. It exposes information about the current graphics mode and a framebuffer, and provides basic drawing operations.

If a platform firmware or an earlier firmware layer has already initialized the display and publishes GOP, a loader can render its UI through that service without implementing a complete display-controller driver itself.

Important limits:

- GOP is a protocol contract, not proof that a particular phone firmware implements it.
- GOP does not prove that the Moto G60 panel is initialized in the required environment.
- A framebuffer's reported mode, pixel format, stride, and lifetime must be treated as reported platform data and independently validated.
- If GOP is absent, a platform-specific display implementation would be a separate and substantial research task. This document does not specify register programming or panel initialization sequences.

**Moto G60 status:** GOP availability before Android is unknown.

### 3.2 Touch: UEFI Absolute Pointer Protocol

The UEFI specification defines Absolute Pointer Protocol for absolute-position devices such as touchscreens and digitizers. It reports pointer capabilities and current state, including touch-active status and coordinates.

This is the natural interface for a touchscreen-driven pre-OS menu. A loader using this service could translate reported coordinates into UI hit-testing and menu selection.

Important limits:

- The protocol is available only if the firmware environment actually publishes it for the touch device.
- The UEFI specification does not make a touchscreen appear automatically; the platform needs a functioning controller driver and appropriate platform integration.
- Simple Pointer Protocol is primarily a relative pointer abstraction. Absolute Pointer is the more suitable conceptual match for a touchscreen.
- If Absolute Pointer is absent, the loader cannot assume Android's touchscreen driver or Android input services are available.
- A custom platform driver would require exact hardware identification and a documented platform contract. That work is not specified here.

**Moto G60 status:** Absolute Pointer availability before Android is unknown.

## 4. What HakiOS demonstrates—and what it does not

HakiOS documentation separates the firmware layer, UEFI application loader, XNU kernel and kernel drivers. Its architecture guide describes the firmware layer providing a framebuffer to the loader. Its driver reference lists touch input as a kernel driver, with device-specific controller support for the POCO X5 Pro.

This is an important distinction for MotoDarwin18:

- HakiOS demonstrates a layered architecture in which a loader can use a framebuffer service supplied by an earlier layer.
- HakiOS's documented Goodix/FocalTech touchscreen support is in its XNU driver layer for its supported device.
- That does **not** establish that HakiOS's loader itself has touchscreen input before XNU starts.
- It also does not establish that its touch driver, firmware layer, or device-specific settings can be reused on the Moto G60.

For MotoDarwin18's requested touch-operated loader menu, touchscreen input must be available **before** XNU starts. A touchscreen driver that only starts inside XNU would be too late to operate the loader menu.

## 5. Proposed service architecture

This is a conceptual separation of responsibilities, not an implementation plan for changing device firmware.

| Layer | Display responsibility | Touch responsibility | Evidence status |
|---|---|---|---|
| Device-provided firmware | May initialize display and expose a graphics service | May expose a pointer service if a platform driver exists | Unknown for XT2135-2 |
| Optional platform firmware layer | Could provide GOP/framebuffer abstraction | Could provide Absolute Pointer if supported and integrated | No Moto G60 implementation demonstrated |
| XNULoader application | Draw UI using a documented display service | Consume documented touch events and perform UI hit-testing | Design only |
| XNU kernel | Later OS graphics and display support | Later OS input driver and event delivery | Separate from loader menu |

The loader should depend on documented service interfaces rather than assuming it can directly reuse Android kernel drivers.

## 6. Research evidence matrix

| Question | Current finding | Confidence for exact XT2135-2 |
|---|---|---|
| Is the device family associated with a 1080x2460 MIPI-DSI display? | Yes, a candidate panel description appears in shared source research | Family-level only |
| Is an Ilitek SPI touch node present in reviewed family source? | Yes | Family-level only |
| Is the exact touch controller in this XT2135-2 known? | No | Unknown |
| Does the device firmware expose GOP before Android? | Not established | Unknown |
| Does the device firmware expose UEFI Absolute Pointer? | Not established | Unknown |
| Can the current XNULoader draw on the phone screen? | No implementation or target evidence | Not implemented |
| Can the current XNULoader receive taps? | No implementation or target evidence | Not implemented |
| Does HakiOS prove pre-XNU touch input on its phone? | Its public driver reference documents touch in the XNU driver layer; this does not prove loader-level touch | Not evidence for Moto |

## 7. Validation criteria for future claims

A claim that the loader has a working display requires evidence that the exact target environment exposes a documented display service and that the loader can use it reliably.

A claim that the loader has working touchscreen input requires separate evidence that:

- the exact target touch hardware is identified;
- the pre-OS environment exposes a usable absolute-pointer service or another documented input service;
- contact state and coordinates are delivered correctly;
- coordinate orientation and display mapping are correct;
- touch failure is handled without selecting a menu item accidentally;
- the behavior is validated on the exact hardware revision.

A host-side test of coordinate mapping or UI logic is useful, but it does not prove that the physical touchscreen works.

## 8. Research gaps and next safe work

The remaining research should stay focused on public source documentation and evidence provenance:

1. Trace the exact Hanoip touch and panel source files and record which board variants reference them.
2. Separate display-panel identity from touch-controller identity in the hardware inventory.
3. Identify the exact XT2135-2 revision mapping, if reliable public evidence exists.
4. Review the public UEFI GOP and Absolute Pointer contracts and record the information an application may rely on.
5. Keep the loader's display and touch dependencies separate so each can be independently marked unknown, source-reviewed, or validated.

No phone-specific register values, pin assignments, interrupt configuration, controller command sequences, memory addresses, boot procedures, or firmware modification instructions belong in this research note.

## 9. Current conclusion

A touchscreen-operated XNULoader menu is a valid project requirement, but it is not currently demonstrated on the Moto G60.

The most promising architecture is for an earlier platform firmware layer to provide a framebuffer/GOP service and an absolute-pointer input service to the loader. Whether any existing or future Moto G60 platform environment can provide both remains unknown.

Until those services and the exact hardware are evidenced, the accurate project status is:

- display service before Android: **unknown**;
- touchscreen service before Android: **unknown**;
- XNULoader display implementation: **not implemented**;
- XNULoader touch implementation: **not implemented**.

## References

- [Hanoip device tree (Moto G40 Fusion/Moto G60)](https://github.com/motorola-sm6150-devs/device_motorola_hanoip)
- [MotoDarwin18 Hanoip platform evidence](HANOIP_PLATFORM_EVIDENCE.md)
- [MotoDarwin18 XT2135-2 identity research](XT2135_2_IDENTITY.md)
- [MotoDarwin18 XNULoader interface design](../../xnuloader/INTERFACE_DESIGN.md)
- [UEFI Specification: Graphics Output Protocol](https://uefi.org/specs/UEFI/2.10/12_Protocols_Console_Support.html)
- [UEFI Specification: Absolute Pointer Protocol](https://uefi.org/specs/UEFI/2.10/12_Protocols_Console_Support.html)
- [HakiOS architecture](https://hackios-web.vercel.app/en/docs/concepts/architecture)
- [HakiOS driver reference](https://hackios-web.vercel.app/en/docs/reference/drivers)
- [HakiOS how it works](https://hackios-web.vercel.app/uk/guide/how-it-works)
- [Linux ILI7807S panel driver configuration](https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/panel/Kconfig)
