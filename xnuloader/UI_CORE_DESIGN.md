# XNULoader UI Core Design

**Status:** platform-neutral UI design and host-test model only. No graphical interface, UEFI application, boot action, firmware integration, or phone compatibility is implemented.

## 1. Goal

Define a small, testable menu-state model for a future phone-resident XNULoader. The model must remain independent of display hardware and input drivers. It consumes normalized events and emits a selection intent only; it never loads an operating system or changes device state.

## 2. Proposed menu

The initial concept has two entries:

1. **Boot iOS 18**
2. **Boot Original Android**

These are product goals, not working actions. In the host model both entries are disabled by default. A future integration could enable an entry only after a separate, reviewed capability and payload-readiness contract exists. No such contract or boot implementation currently exists.

## 3. Layout principles

- Portrait-first responsive layout; do not hard-code the reported panel dimensions.
- Large, well-separated touch targets with clear labels.
- High-contrast foreground/background combinations and a visible focus/selection indicator.
- Keep the title, menu entries, status text, and error text in separate logical regions.
- Avoid conveying status by color alone; pair status color with text or an icon.
- Support text scaling and clipping-safe layout.
- Treat display dimensions, orientation, and pixel format as runtime inputs, not assumptions about XT2135-2.

This document does not prescribe a panel driver, pixel-writing implementation, or hardware-specific rendering path.

## 4. Input contract

The UI core consumes normalized events from the abstract model in `tools/xnuloader_ui_model.py`:

- `down`, `move`, `up`, `cancel`;
- optional keyboard-like `navigate_previous`, `navigate_next`, and `activate` events from a separately verified input adapter.

A touch activation is accepted only when a valid contact begins and ends on the same enabled menu item without cancellation or leaving that item's hit region. Movement outside the original item cancels activation. A second contact is outside the initial single-pointer model and must not be guessed at.

The UI core must never interpret raw controller packets or assume Android input services exist before Android starts.

## 5. State model

The host model represents:

- current focused item;
- enabled/disabled status of each menu item;
- whether a touch contact is active;
- which item, if any, owns the current contact;
- a one-shot selection intent returned after a valid activation.

Selection intent is informational. It is not a command to boot, chain-load, reboot, or change boot configuration.

## 6. Error and unavailable states

The future UI should distinguish:

- display service unavailable;
- input service unavailable;
- malformed or out-of-range input;
- interrupted contact;
- no enabled menu entries;
- unsupported action / action not implemented.

When input fails during a contact, cancel the pending activation. Never convert an input error into an accidental selection. If display output is unavailable, a graphical menu cannot be claimed to work; a fallback requires its own verified service.

## 7. Host validation scope

Host tests can verify deterministic state transitions, hit-testing, disabled-item behavior, cancellation, and one-shot selection intents. They cannot verify actual rendering, touch latency, panel orientation, firmware protocol availability, or phone behavior.

## 8. Acceptance criteria before any on-device UI claim

A future implementation claim requires, separately:

1. exact-target evidence for the pre-OS display and input services;
2. a documented platform adapter with defined ownership and error behavior;
3. validation of rendering against the actual reported display mode;
4. validation of touch coordinate mapping and event lifecycle on the exact hardware revision;
5. explicit evidence that selected actions are implemented and safe to expose.

Until then, this remains a design and host-test exercise.

## Related documents

- [Platform services specification](PLATFORM_SERVICES.md)
- [Interface design and Moto G60 evidence](INTERFACE_DESIGN.md)
- [Pre-Android display and touch research](../research/display-touch/MOTO_G60_PREANDROID_DISPLAY_TOUCH.md)
