# Driver Research and Architecture

MotoDarwin18 keeps driver research separate from the pinned upstream XNU source and from XNULoader platform-service design.

This directory follows the useful organizational idea in HakiOS: group driver work by subsystem. It does **not** copy HakiOS implementation code, imply equivalent hardware support, or establish that any driver works on the Moto G60 XT2135-2.

## Subsystems

| Directory | Responsibility | Initial status |
|---|---|---|
| [wifi](wifi/README.md) | Wireless LAN | Research only |
| [power](power/README.md) | Battery, charging, thermal and power-management boundaries | Research only |
| [bluetooth](bluetooth/README.md) | Bluetooth controller and host-stack boundary | Research only |
| [audio](audio/README.md) | Audio devices and audio subsystem boundary | Research only |
| [gpu](gpu/README.md) | Graphics processor and display-rendering boundary | Research only |
| [camera](camera/README.md) | Camera sensors and imaging subsystem boundary | Research only |
| [storage](storage/README.md) | Persistent storage and block-device boundary | Research only |
| [input](input/README.md) | Touch, buttons and input-event boundary | Research only |
| [modem](modem/README.md) | Cellular modem and telephony boundary | Research only |
| [net](net/README.md) | Network interfaces and common networking boundary | Research only |
| [core](core/README.md) | Shared platform services and driver-independent support | Research only |

## Evidence rules

Every future driver proposal must identify:

1. The exact XT2135-2 / MC38C hardware component, or clearly label evidence as Hanoip-family-only.
2. The exact board revision and component pairing, when known. Do not infer a DVT mapping.
3. Authoritative source provenance for any hardware facts, firmware interface or register-level claim.
4. The relevant upstream XNU interfaces and the boundary between generic XNU and device-specific code.
5. File-level licensing and provenance before importing or adapting any third-party source.
6. A test plan that distinguishes static review, host-side tests, emulation, and actual target validation.

## Current project state

- These directories contain architecture and research notes only.
- No Moto G60 driver implementation is included here.
- No hardware access, firmware interaction, device writes, or boot integration is performed by these documents.
- No HakiOS driver is copied or treated as a drop-in implementation.
- The existing Hanoip evidence remains family-level unless an exact-model source establishes otherwise.

A directory existing does not mean its subsystem is supported. Track evidence and implementation status separately.
