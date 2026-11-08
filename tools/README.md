# Tools

## Platform inventory validator

`validate_platform.py` is the first executable MotoDarwin18 research utility. It checks the structure and evidence discipline of the XT2135-2 platform inventory.

### Requirements

- Python 3.10 or newer
- Python standard library only
- No phone connection, ADB, Fastboot, network access, or elevated permissions

### Run

From the repository root:

```sh
python3 tools/validate_platform.py
```

Windows PowerShell:

```powershell
py -3 tools/validate_platform.py
```

### Run tests

```sh
python3 -m unittest discover -s tests -v
```

Windows PowerShell:

```powershell
py -3 -m unittest discover -s tests -v
```

### Validation rules

- Requires the exact project target identifier, XT2135-2.
- Requires entries for memory, interrupts, timers, storage, display, wireless, and power management.
- Requires non-unknown entries to include a description and source evidence.
- Accepts only documented evidence scopes and HTTPS source links.
- Does not allow a component to be marked **confirmed** using only family-level or SoC-level evidence.
- Requires unknown entries to use a null value rather than an unsupported claim.

Warnings are expected where evidence is based on a shared community device tree rather than exact-model documentation.

### Limitations

This tool validates documentation structure and evidence labels only. It does not inspect hardware, resolve board revisions, infer register addresses, build XNU, or establish device compatibility. It is offline and read-only.

## Boot handoff manifest validator

The descriptive, offline manifest validator is documented in [boot-handoff/README.md](../boot-handoff/README.md).

Run it from the repository root:

```powershell
py -3 tools/validate_boot_handoff.py
py -3 -m unittest discover -s tests -p "test_boot_handoff*.py" -v
```

It checks manifest structure and consistency only. It does not generate boot arguments, infer device memory, or interact with a phone.

## XNULoader platform-services validator

The host-only platform-services validator checks descriptive metadata for the planned display and touch interfaces. Its example manifest intentionally records the Moto G60 services as unknown.

Run from the repository root:

```powershell
py -3 tools/validate_platform_services.py
py -3 -m unittest discover -s tests -p "test_platform_services.py" -v
```

It also contains a pure touch-event model tested with synthetic samples. The validator and model do not access firmware, a touchscreen, a display, ADB, Fastboot, or any connected device. Passing tests do not establish that GOP or UEFI Absolute Pointer is available on the XT2135-2.
