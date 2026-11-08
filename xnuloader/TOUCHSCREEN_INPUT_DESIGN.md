# XNULoader Touchscreen Input Design

**Status:** host-side input model and interface specification only. No Moto G60 touchscreen driver, firmware adapter, or physical touch validation is implemented.

## Goal

Touch is the intended primary input for the phone-resident XNULoader interface. This milestone defines the platform-neutral event boundary and tests its behavior independently of any particular controller.

The implementation in `tools/xnuloader_touch_model.py` consumes synthetic samples. It does not open a device, access GPIO/SPI/I²C, call UEFI, read controller registers, or interact with a phone.

## Evidence and unresolved target facts

Shared Hanoip-family source research contains an Ilitek SPI touchscreen node. That is a family-level lead only. It does not establish the touch controller fitted to the exact Moto G60 XT2135-2 revision, its panel pairing, firmware description, transport ownership, or pre-Android driver availability.

UEFI Absolute Pointer is a plausible standard abstraction for absolute-position input when firmware provides it. Its presence on the XT2135-2 has not been demonstrated. A protocol specification is not a hardware driver.

The following remain **unknown** for the target:
- exact touchscreen controller and hardware revision;
- whether a pre-Android input service exists;
- coordinate range and axis orientation;
- display-to-touch alignment and any rotation or inversion;
- contact sampling rate, latency, and error behavior;
- whether the input device is available at the stage where XNULoader would run.

No controller-specific initialization details or hardware access sequence are included.

## Project-owned event contract

The host model represents a single absolute-pointer contact using these event kinds:

| Event | Meaning |
|---|---|
| `down` | A valid contact begins within the declared coordinate range |
| `move` | An active contact reports a new valid point |
| `up` | The active contact ends |
| `cancel` | An active contact is interrupted or an invalid sample is received |

Coordinates are retained in the source coordinate space. They are not silently scaled, rotated, inverted, or clamped. Display mapping must be a separate operation based on verified ranges and orientation.

### State and safety rules

- A contact cannot begin with missing, boolean, or out-of-range coordinates.
- A valid first contact emits `down`; later valid contact samples emit `move`.
- A release ends an active contact with `up`; an idle release emits no event.
- A read failure or invalid point during an active contact emits `cancel` and clears contact state.
- A failed read while idle emits no event.
- A new contact is not inferred from a release or failure sample.
- The model represents one contact only; it makes no multi-touch or gesture claim.
- Event delivery never activates a menu item by itself. The existing UI model must still validate a complete down/up interaction within the same enabled hit region.

## Separation from menu behavior

The touch adapter should translate a documented platform input source into this event contract. UI logic then consumes the abstract events and performs hit-testing. The touch layer must not choose an operating system, execute a boot action, reboot, or change device state.

The existing UI model requires a contact to begin and end within the same enabled menu item's hit region. Leaving that region or receiving cancellation prevents selection. Menu entries remain disabled by default.

## Coordinate mapping policy

The host model deliberately does not guess a relationship between touch coordinates and display pixels. A later mapping layer can be specified only after reliable source evidence establishes:
1. the actual coordinate minimum and maximum on both axes;
2. the display's reported dimensions;
3. orientation, axis direction, and any required rotation;
4. whether the touch and display coordinate spaces are aligned.

Until then, raw coordinates remain raw coordinates. Unknown orientation must not be guessed from the panel family or screen shape.

## Error and capability states

A future platform adapter should distinguish at least:
- input service not present;
- service present but device not identified;
- device identified but unsupported;
- input read failed;
- coordinate data invalid;
- contact cancelled;
- coordinate mapping unavailable.

No touch input must be treated as a normal capability limitation, not as permission to assume Android drivers are active or to silently trigger a fallback selection.

## Host-side validation

The unit tests use synthetic coordinate ranges and samples. They cover the contact lifecycle, invalid input, cancellation, recovery after cancellation, and single-contact behavior.

Passing these tests establishes only the behavior of this abstract Python model. It does not establish:
- a working UEFI Absolute Pointer service;
- the exact XT2135-2 touch controller;
- a functioning hardware driver;
- physical coordinate calibration;
- touchscreen operation before Android.

## Completion criteria for this research milestone

The host-side touchscreen event model milestone is complete when:
- the event contract is documented;
- the pure state model is implemented;
- lifecycle, invalid-sample, and cancellation tests pass;
- repository CI passes on its supported Python versions;
- documentation explicitly preserves all unknown target hardware facts.

**Physical touchscreen support remains incomplete** until the exact target input path and full UI interaction are independently validated on the XT2135-2. This repository milestone must not be described as a working phone touchscreen driver.

## References

- [UEFI Specification 2.11 — Console Support Protocols](https://uefi.org/specs/UEFI/2.11/12_Protocols_Console_Support.html)
- [Moto G60 pre-Android display and touch research](../research/display-touch/MOTO_G60_PREANDROID_DISPLAY_TOUCH.md)
- [XNULoader platform services](PLATFORM_SERVICES.md)
- [XNULoader interface design](INTERFACE_DESIGN.md)
- [XNULoader UI core design](UI_CORE_DESIGN.md)
