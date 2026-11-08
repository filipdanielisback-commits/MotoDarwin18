# Boot Handoff Manifest Validator

An offline, host-side structural validator for **descriptive** MotoDarwin18 boot-handoff research manifests.

## Scope

This tool checks JSON shape and internal consistency only. It does not construct an Apple `boot_args` structure, create a device tree, choose hardware addresses, infer a memory map, or communicate with a phone.

Checks include:
- required top-level and nested fields;
- exact target identifier `XT2135-2`;
- unsigned 64-bit integer bounds for address-like values;
- positive memory-region sizes and power-of-two alignment;
- address-range overflow and overlapping memory regions;
- device-tree metadata consistency;
- HTTPS evidence references and evidence-scope rules;
- rejection of duplicate JSON object keys and non-standard numeric constants.

A value may be `null` when unknown. The example manifest intentionally contains no hardware addresses or populated memory regions.

## Run

From the repository root, with Python 3.10 or newer:

```powershell
py -3 tools/validate_boot_handoff.py
py -3 -m unittest discover -s tests -p "test_boot_handoff*.py" -v
```

To validate a different descriptive manifest:

```powershell
py -3 tools/validate_boot_handoff.py path/to/manifest.json
```

Exit codes: `0` means structurally valid; `1` means validation failed.

## Evidence rules

Evidence scopes are `upstream`, `soc_family`, `device_family`, and `exact_model`. A claim marked `confirmed` must have at least one `exact_model` evidence item. Family-level or SoC-level evidence must not be promoted to exact-model confirmation.

## Important limitations

A passing result is **not** evidence that the manifest matches the real Motorola handset, that an XNU boot ABI has been correctly implemented, or that a kernel can boot. The schema is a project research format, not Apple's official boot ABI specification.

The tool is read-only with respect to the phone and has no ADB, Fastboot, network, firmware, partition, bootloader, or device-write functionality.
