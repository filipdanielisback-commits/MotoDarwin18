# XNULoader Display Rendering Design

**Status:** research and host-side layout model only. No graphics driver, UEFI application, framebuffer writer, or Moto G60 display support is implemented.

## Purpose

Define a small, platform-neutral presentation layer for the proposed XNULoader menu. The design separates:

1. **Display discovery** — determine whether a documented pre-OS graphics service exists.
2. **Mode description** — record dimensions, scan-line stride, and pixel format without assuming a particular panel.
3. **Layout** — calculate logical rectangles for the title, menu entries, and status text.
4. **Rendering backend** — a future, separately reviewed adapter that could translate drawing operations to a verified firmware service.
5. **UI state** — continue to use the existing UI model; rendering must not trigger boot or device-control actions.

This document does not specify how to access or modify Moto G60 firmware, initialize its display hardware, or write to physical memory.

## Evidence and platform assumptions

UEFI 2.11 defines the Graphics Output Protocol (GOP) as a pre-boot graphics abstraction. It exposes mode information and operations for setting a mode and transferring pixel blocks. Mode metadata includes horizontal and vertical resolution, pixel format, and pixels per scan line. PixelBltOnly is a valid format designation and means a linear framebuffer is not available for that mode. See the [UEFI 2.11 specification, section 12.9](https://uefi.org/specs/UEFI/2.11/12_Protocols_Console_Support.html).

That standard describes what a UEFI implementation may provide; it is not evidence that a specific phone firmware implements GOP. **GOP availability on the Moto G60 XT2135-2 is unknown.** The shared Hanoip family panel references are not sufficient to identify the exact XT2135-2 display controller or prove a usable pre-OS display path.

The design therefore treats all display capabilities as unknown until supported by exact-model evidence. It does not assume a 1080×2460 mode, a particular panel, a pixel format, or a linear framebuffer.

## Display mode contract

A future display adapter must report, rather than guess:

- width and height in pixels;
- pixels per scan line (stride), which may differ from visible width;
- the exact pixel format identifier;
- whether the service is usable for the current pre-OS phase;
- whether output is available through a block-transfer interface or a directly addressable framebuffer.

The host model validates only descriptive metadata. It does not retain physical addresses or attempt to access a framebuffer.

### Pixel-format handling

The UEFI GOP model distinguishes RGB-reserved, BGR-reserved, bit-mask, and BLT-only formats. These formats are not interchangeable. A future backend must explicitly support the reported format or return an unsupported-format status; it must never silently reinterpret channel order or assume that stride equals width.

The initial host model accepts known format names as metadata but intentionally performs no pixel packing or framebuffer writes. Bit-mask channel layouts, byte ordering, and backend-specific transfer semantics remain future adapter responsibilities.

## Logical coordinate and layout rules

- Use a top-left origin for logical screen coordinates.
- Keep layout coordinates independent of physical memory addresses.
- Use the reported visible width and height as the clipping bounds.
- Keep all generated rectangles non-negative and entirely inside the visible area.
- Compute a responsive, centered menu column; do not hard-code portrait resolution.
- Keep generous spacing and large touch targets, with readable title and status regions.
- Never communicate state using color alone. Pair status colors with text and/or symbols.
- Keep text scaling and localization in mind; long labels must not be clipped by fixed-width assumptions.
- Orientation is not inferred from the panel model. A future platform adapter must provide reliable orientation evidence or leave orientation unspecified.

## Rendering command boundary

The layout layer produces geometry only: title bounds, menu-item bounds, and status bounds. A future renderer may consume these values and draw backgrounds, focus outlines, labels, and status messages through a separately verified backend.

The renderer must not:
- load or execute a kernel;
- alter boot configuration or firmware state;
- reboot, chain-load, or select an operating system;
- assume that menu selection is a bootable action;
- access hardware directly from the host layout model.

The conceptual “Boot iOS 18” and “Boot Original Android” entries remain disabled by default under the existing UI design.

## Error and fallback states

The UI should be able to display a clear status when:
- no graphics service is discovered;
- mode metadata is invalid;
- the pixel format is unsupported by a future backend;
- a drawing operation is rejected by the backend;
- display output is unavailable.

A failure must not be represented as a successful render. If no verified graphical path exists, the project must report that limitation rather than claim a working on-device menu. A text console is a separate possible service and must not be assumed either.

## Host-side model and tests

The file tools/xnuloader_display_layout.py is a pure Python model for validating display-mode metadata and calculating menu geometry from synthetic dimensions. It does not draw pixels, open a display, access UEFI, or communicate with a phone.

The tests cover:
- accepted and invalid dimensions/stride;
- known pixel-format labels versus unknown labels;
- responsive layout on portrait and landscape synthetic modes;
- bounds containment and invalidly small surfaces.

Passing these tests proves only that the host-side metadata/layout model behaves as tested. It does not prove GOP presence, display output, touch support, panel compatibility, or boot capability on the XT2135-2.

## Acceptance criteria for any future display-support claim

A future claim must identify:
1. the exact XT2135-2 hardware/revision evidence;
2. the actual pre-OS display service and its source of evidence;
3. the mode and pixel format actually reported by that service;
4. the backend path and its error handling;
5. independent evidence that the intended output is visible on the target.

Until then, display service availability and on-device rendering remain **unknown / not implemented**.

## References

- [UEFI Specification 2.11 — Graphics Output Protocol](https://uefi.org/specs/UEFI/2.11/12_Protocols_Console_Support.html)
- [Moto G60 pre-Android display and touch research](../research/display-touch/MOTO_G60_PREANDROID_DISPLAY_TOUCH.md)
- [XNULoader platform services](PLATFORM_SERVICES.md)
- [XNULoader UI core design](UI_CORE_DESIGN.md)
- [XNULoader interface design](INTERFACE_DESIGN.md)
