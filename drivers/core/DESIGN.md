# Driver Core Design

**Status: host-side reference implementation. Not an XNU driver framework and not a Moto G60 hardware implementation.**

## Purpose

Provide one small, project-owned vocabulary for driver metadata, capability descriptions, registration, lifecycle state, and error reporting. The first implementation is Python so that its behavior can be tested offline without target hardware.

## Modules

- `model.py`: immutable descriptors, capability metadata, lifecycle states, error records, and snapshots.
- `registry.py`: registration, lookup, listing, initialization, shutdown, and safe unregister rules.
- `__init__.py`: public package exports.

## Lifecycle

```text
REGISTERED -> INITIALIZING -> READY -> STOPPING -> STOPPED
                    |                    |
                    v                    v
                  FAILED <---------------+
```

- Registration validates metadata but does not initialize anything.
- Initialization is permitted from `REGISTERED` or `STOPPED`.
- Shutdown is permitted only from `READY`.
- Initialization and shutdown exceptions become explicit `DriverError` records and put the entry in `FAILED`.
- Failed or active entries cannot be unregistered by this initial API. Recovery policy is intentionally not guessed.
- A stopped driver may be initialized again.

## Capability semantics

Capability state is descriptive metadata:

- `unknown`: no verified availability claim.
- `available`: the author is asserting availability and should provide evidence.
- `unavailable`: evidence indicates the capability is not available in the described context.

The registry does not probe hardware, verify evidence links, or infer capabilities. Moto G60 capabilities must remain `unknown` until exact-model evidence supports a stronger statement.

## Error semantics

Errors are structured by operation (`initialization_failed` or `shutdown_failed`) and include a concise exception summary. The framework does not attempt automatic retries or recovery.

## Concurrency and ownership

This first version is intentionally single-threaded. It has no locks, asynchronous callbacks, dependency graph, interrupt handling, memory mapping, register access, firmware calls, or resource ownership model. Those features must not be added until their requirements and execution environment are established.

## Testing boundary

Unit tests use fake Python driver objects with in-memory counters and controlled exceptions. They validate the model and registry only. Passing host tests does not establish XNU integration, firmware compatibility, or physical-device support.

## Future integration gate

Before adapting this model to C or XNU, specify the target execution environment, allocation rules, concurrency model, ownership/lifetime rules, logging/error transport, and the exact XNU interfaces involved. Do not treat this Python API as an ABI.
