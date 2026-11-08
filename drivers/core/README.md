# Core Platform Support

**Status: host-side reference implementation — not a Moto G60 hardware driver.**

This directory now contains an original Python driver-core model and unit-testable lifecycle registry. It is **not** an XNU driver framework.

## Source

- [`model.py`](model.py) — immutable driver descriptors, capability states, lifecycle states, error records and snapshots.
- [`registry.py`](registry.py) — metadata validation, registration, lookup, initialization, shutdown and unregister rules.
- [`__init__.py`](__init__.py) — public package exports.
- [`DESIGN.md`](DESIGN.md) — lifecycle, semantics, constraints and future integration requirements.

## Tests

Run from the repository root:

```sh
python -m unittest discover -s tests -p "test_driver_core.py" -v
```

## Boundaries

- The registry is single-threaded and host-side.
- Driver methods in tests are fake Python methods; no hardware or firmware is accessed.
- Capabilities default to `unknown`. An available/unavailable assertion requires an evidence reference.
- There is no interrupt handling, register access, memory mapping, device initialization, power sequencing, firmware call, or XNU integration.
- Passing these tests proves only the Python model's behavior. It does not prove that any Moto G60 subsystem works.

See [the driver architecture and evidence rules](../README.md).
