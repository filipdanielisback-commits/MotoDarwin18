# XNULoader Interface Design

**Status:** design specification only. This document does not implement a loader, touchscreen driver, display driver, firmware interface, or kernel handoff.

## 1. Goal

The long-term goal is a genuine, phone-resident XNULoader for the Motorola Moto G60 XT2135-2. It should provide a usable on-device interface and, only after the platform contract is established, manage a documented handoff to a compatible kernel.

A desktop-only mock-up is not the project goal. A menu drawing or successful host-side test is not evidence that the phone's firmware, display, or touchscreen is supported.

## 2. Component boundary

Keep these layers distinct:

1. **Device boot firmware:** the device-provided environment and its documented entry contract. The XT2135-2 contract is currently unknown.
2. **Loader application:** the proposed XNULoader program, which would run only in a firmware environment proven to support it.
3. **Input and display services:** the mechanisms required to render the interface and receive touch or button input. Their target drivers and firmware interfaces are not established.
4. **Kernel handoff boundary:** the platform information and ownership contract required by the selected XNU build.
5. **XNU and later operating-system services:** kernel/platform support and userland are separate from the loader. A loader cannot replace missing XNU drivers.

This specification does not prescribe how to alter or enter the phone's firmware environment.

## 3. User-interface requirements

The intended loader interface should be designed for the phone itself:

- Touchscreen is a **primary intended input method**, not a decorative feature.
- Tapping a clearly bounded menu item should select it.
- A visible selected/focused state must remain available for users who navigate without touch.
- Scrolling or swiping should be supported only where the final interface has content that needs it.
- Controls must have sufficiently large targets, readable labels, strong contrast, and clear focus indication.
- The interface must not depend on tiny desktop-style controls or a hardware keyboard.
- The screen should explain unavailable functions instead of presenting them as working options.

Proposed menu labels remain conceptual:
- Boot iOS 18
- Boot Original Android

Neither option is currently implemented. The Android option must not imply that chain-loading, returning to Android, or preserving the existing operating system has been demonstrated.

## 4. Touchscreen support requirements

Touch support is a release requirement for the intended on-device graphical interface. It is not yet an implemented or verified capability.

### 4.1 Evidence currently available

The shared Hanoip-family Android/Linux source review found an Ilitek SPI touchscreen node in a Hanoi touchscreen device-tree include. This is a useful family-level research lead only. It does **not** confirm that every XT2135-2 revision uses that controller, establish the exact touch panel/controller pairing, or provide a usable loader driver.

The exact XT2135-2 board revision, touchscreen component, firmware description, electrical configuration, and low-level input interface remain unverified.

### 4.2 Required capability areas

Before touchscreen support can be called implemented, the project must establish evidence for all of the following:

- **Device identity:** exact touch controller and panel pairing for the target hardware revision.
- **Discovery:** a documented way for the loader environment to identify the input device.
- **Transport:** verified interface and resource ownership for the actual controller. The family-level SPI clue is not sufficient by itself.
- **Initialization:** documented controller state and initialization requirements from lawful, attributable sources.
- **Event model:** a defined representation of contact state and coordinates, including release/cancel and invalid or out-of-range input.
- **Coordinate mapping:** verified relationship between touch coordinates, display resolution, orientation, and any display rotation.
- **Reliability:** handling for absent, unresponsive, or unsupported touch hardware without freezing the interface.
- **Isolation:** input handling must not assume that an Android driver or Android userspace is available in the loader environment.
- **Testing:** host-side tests for the abstract event model, followed by separately documented validation evidence for the exact target. Host tests cannot prove physical touchscreen operation.

No register values, controller command sequences, GPIO assignments, interrupt numbers, or target memory addresses are specified here because the exact hardware and firmware contract have not been established.

### 4.3 Fallback and accessibility

The interface should also define a non-touch navigation path. Volume-button navigation is a candidate because it is part of the proposed UI concept, but the loader's ability to receive those button events is unverified. The final design must document which input sources are actually available rather than assuming them.

If touch is unavailable, the interface should clearly indicate the fallback input method. If no supported input method is available, it should fail visibly and safely rather than silently selecting an option.

## 5. Display and other interface services

Touchscreen operation depends on a working display path, but display and touch are separate subsystems and must be validated independently.

The shared device-family research identified a candidate Tianma ILI7807S 678-class 1080x2460 MIPI DSI panel description. This does not confirm the panel fitted to the exact XT2135-2 unit or establish that a proposed loader can initialize it.

The design should track these capabilities separately:

- framebuffer or other documented display service;
- resolution, orientation, and pixel-format discovery;
- rendering and text output;
- touch input and coordinate mapping;
- volume-button input, if exposed by the environment;
- error display and diagnostic reporting.

Audio, vibration/haptics, battery status, and other conveniences are optional future research topics. They must not be treated as prerequisites for a minimal interface or claimed supported without target evidence.

## 6. Conceptual interface data

The eventual project-owned interface should describe information, not assume undocumented hardware values. Candidate logical records include:

| Record | Purpose | Current status |
|---|---|---|
| Loader identity/version | Identify the loader build and its declared interface version | Design topic |
| Platform identity | Record model and evidence-backed hardware revision | Exact revision unresolved |
| Display capability | Describe whether a display service is available and its reported mode | Unknown on target |
| Input capability | List available input sources and their status | Unknown on target |
| Touch event | Represent contact lifecycle and normalized or display-relative coordinates | Abstract design only |
| Kernel artifact metadata | Describe provenance, architecture, version and integrity metadata | No accepted artifact contract |
| Handoff capability | Describe whether a separately verified platform handoff contract exists | Not demonstrated |
| Diagnostic result | Report a stable error category and human-readable explanation | Design topic |

These are conceptual data categories, not a binary ABI, firmware protocol, or executable implementation.

## 7. Error categories

The interface should distinguish at least:

- unsupported firmware environment;
- platform identity not established;
- display service unavailable;
- touch device not detected;
- touch device detected but unsupported;
- touch input unavailable or stalled;
- fallback input unavailable;
- invalid or incomplete kernel metadata;
- platform handoff contract not established;
- required platform service unavailable.

Errors should state what is known and what remains unknown. They must not suggest that retrying, changing firmware settings, or modifying partitions is an appropriate remedy.

## 8. Relationship to the pinned XNU research

The current research baseline is XNU tag xnu-11215.1.10, used provisionally for source analysis. The project has documented the ARM64 boot_args fields and the Apple-specific SecureDT representation expected by the reviewed XNU source.

Those findings describe kernel-side expectations; they do not prove that Moto firmware supplies them or that a third-party loader can safely construct them. In particular:

- the exact firmware-to-loader entry contract is unknown;
- the exact XT2135-2 display and input services available before Android starts are unknown;
- the Moto device-tree producer format and lifetime contract are unknown;
- the complete memory map and kernel handoff contract are not established;
- no target-specific XNU platform integration has been demonstrated.

The loader design must not silently equate a standard Linux FDT with Apple's SecureDT in-memory representation.

## 9. Verification gates

Use evidence labels consistently:

1. **Specified:** requirement documented.
2. **Source-reviewed:** behavior traced to a pinned, attributable source.
3. **Host-tested:** abstract logic or metadata checks pass on a host; this does not validate phone hardware.
4. **Environment-verified:** the required interface is demonstrated in a documented target firmware environment.
5. **Target-validated:** the exact XT2135-2 hardware revision has evidence for the claimed capability.

Touchscreen support must not be labelled working before the exact target's input path reaches the appropriate target-validation gate. Display success alone is not touch success, and family-level DTS evidence alone is not target validation.

## 10. Safe research boundaries

This document supports source review, interface design, provenance tracking, and host-only tests of abstract data models. It does not provide or authorize instructions or code for changing boot firmware, boot configuration, partitions, or device state; building or executing a boot payload; constructing a device tree for handoff; or testing on an essential personal device.

## 11. Current status

- Genuine phone-resident loader: **long-term goal; not implemented**.
- Touchscreen UI: **required by design; not implemented or verified**.
- Display path: **unknown on exact target**.
- Volume-button fallback: **proposed; availability unverified**.
- XNU handoff: **not demonstrated**.
- Moto G60 boot support: **not demonstrated**.

A future release must describe each capability by its actual evidence level. No loader, touchscreen, Android-return, or iOS 18 boot capability is claimed by this specification.

## References

- [MotoDarwin18 device inventory](../docs/DEVICE_INVENTORY.md)
- [MotoDarwin18 device unknowns](../docs/DEVICE_UNKNOWNS.md)
- [Hanoip platform evidence](../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
- [Secure Device Tree requirements](../docs/SECURE_DEVICE_TREE_REQUIREMENTS.md)
- [Device Tree property compatibility matrix](../docs/DEVICE_TREE_PROPERTY_COMPATIBILITY_MATRIX.md)
- [Boot ABI compatibility gaps](../docs/BOOT_ABI_COMPATIBILITY_GAPS.md)
- [Pinned XNU source verification](../xnu/source-reviews/PINNED_SOURCE_VERIFICATION.md)
- [HakiOS architecture comparison](HAKIOS_ARCHITECTURE_COMPARISON.md)
