# XNULoader Display Backend Interface

**Status:** platform-neutral interface design and host-side contract validation only. No UEFI GOP adapter, graphics driver, framebuffer access, pixel renderer, or Moto G60 display support is implemented.

## Purpose

Define the boundary between the XNULoader presentation layer and a future, evidence-backed display service. The interface must be testable without pretending that a host test is a physical display.

## Layering

1. **UI/layout:** produces logical rectangles and presentation intent.
2. **Display backend contract:** reports service state and accepts a frame description.
3. **Platform adapter:** a future implementation for a specifically verified service, such as GOP.
4. **Firmware/hardware:** owns the actual display path.

Only layers 1 and the descriptive parts of layer 2 are represented in the current host model. Layer 3 is not implemented.

## Contract records

The host model defines:

- `DisplayServiceReport`: discovery state, optional mode metadata, supported transfer method labels, and an optional error code;
- `DisplayFrame`: a sequence of logical drawing commands (clear, fill rectangle, or text);
- `DisplayCommand`: a command kind, optional rectangle, and optional text;
- `PresentStatus`: accepted, unavailable, unsupported, or failed;
- `DisplayBackend`: a Python protocol describing the future `discover()` and `present(frame)` boundary.

These are project-owned host contracts, not UEFI ABI structures. They contain no physical addresses, memory mappings, register values, device handles, or firmware function pointers.

## Discovery states and invariants

| State | Required information | Meaning |
|---|---|---|
| `not_checked` | no mode, no methods, no error | No discovery has been performed |
| `available` | valid mode and at least one known transfer method | A caller has evidence that the service can be queried |
| `unavailable` | no mode, no methods, no error | The service was not exposed |
| `error` | error code, no usable mode or methods | Discovery failed |

A report marked available is still only a report. The project must attach exact-target evidence before making a Moto G60 capability claim. A synthetic report in a unit test is not target evidence.

## Frame and command validation

The host validator checks that:
- frames contain supported command kinds;
- fill commands have a positive rectangle fully inside the reported visible mode;
- text commands contain non-empty text and a valid in-bounds anchor rectangle;
- clear commands do not carry irrelevant geometry or text;
- a frame cannot be validated without an available service report and valid mode.

This validation does not rasterize text, blend colors, pack pixels, transfer a BLT buffer, or write to a framebuffer. It only checks the shape and bounds of the abstract request.

## Error behavior

A future adapter must return an explicit status. It must not silently treat unavailable services, unsupported formats, rejected transfers, or firmware errors as successful presentation. The UI should retain a textual diagnostic path in its state model; this document does not assume that a text console exists.

## GOP-specific boundary

UEFI GOP is a candidate standard backend, not a confirmed Moto G60 service. A future GOP adapter would need to be designed against the actual UEFI protocol contract and only after exact-target firmware evidence exists. GOP mode metadata and transfer semantics must be preserved; BLT-only modes must not be treated as linear framebuffers.

No GOP calls or firmware interactions are implemented here.

## Host validation

Run:

```sh
python -m unittest discover -s tests -p "test_xnuloader_display_backend.py" -v
```

Tests use synthetic metadata and an in-memory test double. They validate contract invariants only. They do not establish firmware availability, display output, pixel correctness, panel compatibility, or phone support.

## Acceptance criteria for a future real backend

A real backend claim requires all of the following:
1. exact XT2135-2 hardware/revision and firmware evidence;
2. evidence that the target pre-OS environment exposes the selected display service;
3. an adapter reviewed against that service's published specification;
4. explicit handling of mode, format, transfer, and error semantics;
5. independent target evidence that output is visible and correct.

Until then, Moto G60 display service availability and physical rendering remain **unknown / not implemented**.

## Related documents

- [Display rendering design](DISPLAY_RENDERING_DESIGN.md)
- [Platform services specification](PLATFORM_SERVICES.md)
- [Moto G60 pre-Android display and touch research](../research/display-touch/MOTO_G60_PREANDROID_DISPLAY_TOUCH.md)
- [UI core design](UI_CORE_DESIGN.md)
