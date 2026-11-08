## 2026-11-08 — Initial host-side driver core

### Work completed

- Added an original Python package under `drivers/core/` for immutable driver descriptors, evidence-labelled capability metadata, lifecycle states, structured errors and registry snapshots.
- Added a single-threaded registry with registration, lookup, sorted listing, initialization, shutdown, restart after clean shutdown, and guarded unregister behavior.
- Added host-side unit tests using fake in-memory driver objects, including metadata validation, lifecycle transitions, controlled failures, and invalid state transitions.
- Added `drivers/core/DESIGN.md` and updated the driver index to distinguish this host-side reference model from actual hardware driver support.
- Added a dedicated driver-core test step to the offline GitHub Actions workflow for Python 3.10 and 3.12.

### Boundaries

- This code does not access hardware, firmware, registers, memory mappings, interrupts, or XNU internals.
- The registry is not thread-safe and is not a C ABI or kernel driver framework.
- Capabilities default to unknown; non-unknown capability assertions require an evidence reference.
- Host tests can validate Python model behavior only. They do not demonstrate Moto G60 compatibility or device support.

### Next integration gate

Define the target execution environment and exact XNU interfaces before designing any kernel-facing C abstraction. Keep device-specific driver implementation blocked on exact-model component and firmware-interface evidence.

