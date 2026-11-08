# XNULoader Platform Services Specification

**Status:** interface specification only. This document defines what a future loader would need from its environment. It does not implement a UEFI application, device driver, firmware component, or kernel handoff.

## 1. Purpose

A phone-resident XNULoader needs documented platform services before it can present an interactive menu. For the planned graphical interface, the two primary service families are:

- display output, preferably through a standard firmware graphics interface;
- pointer/touch input, preferably through a standard firmware input interface.

The loader must discover whether these services are actually present. It must not assume that Android's later drivers or services are available before Android starts.

## 2. Layer boundaries

| Layer | Responsibility | Moto G60 evidence |
|---|---|---|
| Device firmware | Establishes the pre-OS environment and may publish protocols | Exact XT2135-2 contract unknown |
| Platform/UEFI drivers | Initialize hardware and publish supported protocols | No Moto G60 implementation demonstrated |
| XNULoader | Consumes documented protocols and presents UI | Design only |
| XNU | Provides later kernel-level platform and device support | Separate implementation; not demonstrated |

A UEFI application cannot conjure a protocol that the firmware and its drivers do not provide. A missing protocol is a platform-support gap, not a reason to silently assume Android services exist.

## 3. Display service contract

### Preferred interface: UEFI Graphics Output Protocol (GOP)

GOP is the preferred abstract display interface for a UEFI-style loader. The UEFI specification describes it as a basic abstraction for video modes and pixel transfer to/from the graphics controller framebuffer.

A future XNULoader display adapter should consume only documented information reported by the protocol, including:

- whether GOP is available;
- current mode and reported resolution;
- pixel format;
- pixels per scan line / row stride;
- framebuffer information, where exposed;
- whether a requested drawing operation succeeds.

The UI layer should not contain panel-controller assumptions. Rendering should be separated from the platform adapter so that host-side tests can exercise layout and clipping logic without a physical display.

### Important lifecycle limit

GOP is a UEFI Boot Services protocol. Its use is tied to the firmware boot-services environment; the project must not assume that the same protocol remains callable after the OS handoff boundary. The eventual handoff design must separately document display ownership and whether a framebuffer is retained for the next stage.

**Moto G60 status:** no evidence currently establishes that XT2135-2 firmware exposes GOP before Android. The family-level MIPI-DSI panel reference is not evidence of GOP availability.

## 4. Touch and pointer service contract

### Preferred interface: UEFI Absolute Pointer Protocol

Absolute Pointer is the best conceptual match for touchscreen input because it reports absolute pointer position and touch state. A future input adapter should treat the protocol's reported mode and state as authoritative, validate coordinates against its reported range, and normalize events into a project-owned abstract event model.

The abstract event model should represent:

- contact begins;
- contact remains active / position updates;
- contact ends;
- device or read failure;
- coordinates outside the reported range.

The UI layer should receive events, not controller-specific packets. A tap should activate a control only after a valid contact lifecycle and hit-test. An invalid or interrupted event sequence must not trigger a menu action.

### Related interface: UEFI Simple Pointer Protocol

Simple Pointer is a separate UEFI protocol with relative pointer-state semantics. It may be useful for a mouse-like device, but it should not be treated as interchangeable with Absolute Pointer or assumed to provide touchscreen coordinates.

### Driver responsibility

The UEFI protocol is an interface contract, not a touchscreen driver. A platform driver must already have initialized and published the protocol for the physical device. The shared Hanoip-family Ilitek SPI source reference does not prove that such a driver exists in Moto G60 pre-Android firmware.

**Moto G60 status:** no evidence currently establishes that XT2135-2 firmware exposes Absolute Pointer or Simple Pointer before Android.

## 5. Capability discovery and graceful degradation

At startup, a future loader should record capabilities as one of:

- available: protocol discovered and a basic query succeeded;
- unavailable: protocol was not exposed;
- error: protocol was discovered but its query failed;
- not_checked: no discovery evidence is available.

The UI should distinguish these states. It must not label a feature working solely because a family-level device-tree entry exists.

Expected behavior at the design level:

| Display | Touch | UI behavior |
|---|---|---|
| Available | Available | Graphical touch interface may be offered |
| Available | Unavailable | Graphical interface may use a separately verified fallback input |
| Unavailable | Available | No graphical menu; do not claim touch UI works |
| Unavailable | Unavailable | Report that the required interactive services are unavailable |
| Error | Any state | Report the display-service error without pretending the UI is operational |

A text console or volume-button fallback is also conditional on a documented service being exposed. Neither should be presumed.

## 6. Project-owned abstraction boundary

Keep three layers separate:

1. **Firmware adapter:** protocol discovery and calls, implemented only when a supported firmware environment is established.
2. **Platform-neutral model:** capability records, display mode metadata, pointer ranges, and abstract input events. This layer can be validated on a host.
3. **UI logic:** hit-testing, selection state, accessibility, and error presentation. This layer can also be tested on a host with synthetic events.

Host tests can validate data handling and UI logic. They cannot prove firmware protocol availability, panel initialization, touch-controller operation, or physical coordinate accuracy.

## 7. Proposed metadata model (not a firmware ABI)

The project may use a descriptive manifest for research and host validation. It should record:

- exact target model and evidence scope;
- firmware environment identity, if known;
- display protocol name and availability status;
- reported display dimensions and pixel format, only when actually observed;
- pointer protocol name and availability status;
- reported coordinate range, only when actually observed;
- source references and evidence scope for every non-unknown claim.

Unknown values must remain explicitly unknown. The manifest is documentation/test input only; it must not be interpreted as a device configuration, binary protocol, driver table, or boot payload.

## 8. Moto G60 evidence status

| Item | Evidence | Status |
|---|---|---|
| Candidate 1080x2460 MIPI-DSI panel in shared Hanoi source | Family-level source review | Candidate; exact XT2135-2 panel unconfirmed |
| Ilitek SPI touchscreen node in shared Hanoi source | Family-level source review | Candidate; exact XT2135-2 controller unconfirmed |
| GOP in pre-Android environment | No exact-model evidence | Unknown |
| Absolute Pointer in pre-Android environment | No exact-model evidence | Unknown |
| Simple Pointer in pre-Android environment | No exact-model evidence | Unknown |
| Loader display adapter | No implementation | Not implemented |
| Loader touch adapter | No implementation | Not implemented |
| Physical touchscreen UI | No target validation | Not demonstrated |

## 9. Acceptance criteria for future implementation claims

**Display service available** may be claimed only when the exact target environment is shown to expose a documented graphics service and the loader-side consumer is validated against its reported mode and error behavior.

**Touch service available** may be claimed only when the exact target environment is shown to expose a documented pointer service and event delivery, contact lifecycle, coordinate range, and failure handling are validated.

**Touchscreen working in XNULoader** additionally requires the complete UI path to be validated on the exact XT2135-2 hardware revision. A host test or a working Android touchscreen is not sufficient.

## 10. Safe scope for the next engineering step

The next step may implement a host-only validator for the descriptive capability manifest and pure tests for the abstract touch-event model. Such code must not discover or access phone hardware, call firmware protocols, build a UEFI executable, create a boot payload, construct a kernel handoff, or change device state.

## References

- [UEFI Specification 2.10](https://uefi.org/specs/UEFI/2.10/)
- [UEFI Console Support: Absolute Pointer, Simple Pointer, and GOP](https://uefi.org/specs/UEFI/2.10/12_Protocols_Console_Support.html)
- [UEFI Overview: platform-specific protocol requirements](https://uefi.org/specs/UEFI/2.10/02_Overview.html)
- [MotoDarwin18 pre-Android display and touch research](../research/display-touch/MOTO_G60_PREANDROID_DISPLAY_TOUCH.md)
- [MotoDarwin18 XNULoader interface design](INTERFACE_DESIGN.md)
- [MotoDarwin18 Hanoip platform evidence](../research/soc/HANOIP_PLATFORM_EVIDENCE.md)
