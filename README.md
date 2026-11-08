# MotoDarwin18

**Independent research into Darwin/XNU compatibility on the Motorola Moto G60 (XT2135-2), with iOS 18-era compatibility as a long-term research target.**

> **Project status: early-stage research.** This repository does not currently contain a working port, a bootable image, or an iOS 18 implementation. No compatibility claims are made until they are demonstrated and documented.

## Project goals

MotoDarwin18 is a research project to understand what would be required for Darwin/XNU-related software to run on the Motorola Moto G60 (XT2135-2).

The initial goals are to:

- Document the phone's publicly documented hardware characteristics.
- Study the relevant ARM64, kernel, device-tree, and operating-system interfaces at a high level.
- Map the major subsystems that a hypothetical device port would need to support.
- Keep research notes, references, and compatibility claims verifiable.
- Build a clear separation between original project work and third-party material.

## What this project is — and is not

- **It is** an independent learning and compatibility-research project.
- **It is not** an official Apple project, an Apple product, or an endorsement by Apple or Motorola.
- **It is not currently** a working iOS 18 port or a replacement operating system.
- It does not include Apple's proprietary iOS binaries, restore images, keys, firmware, or other restricted materials.
- It does not claim that Apple's proprietary iOS components are open source.

The open-source XNU kernel and proprietary iOS components are different things. Any future work must respect the original license and notices of every upstream component. The MIT license in this repository applies only to original project files that we have the right to license under MIT.

## Device

| Item | Target |
|---|---|
| Manufacturer | Motorola |
| Model | Moto G60 |
| Model identifier | XT2135-2 |
| CPU architecture | ARM64 (to be confirmed against primary device documentation) |
| Port status | Not started / research only |

Hardware details will be added only when supported by reliable documentation or reproducible observations. Unknown values will remain marked as unknown rather than guessed.

## Research areas

1. **Platform inventory** — identify hardware blocks and document trusted sources.
2. **Architecture study** — understand the boundaries between boot firmware, kernel, drivers, and user space.
3. **Compatibility matrix** — record what is known, unknown, and not yet investigated.
4. **Licensing and provenance** — track upstream code, notices, and third-party licenses.
5. **Emulation and documentation** — prefer non-destructive, reproducible research before considering any device-specific experiments.

## Safety and device integrity

This repository is documentation-first. It does not provide instructions for bypassing device security, modifying protected firmware, or performing risky device-altering procedures. Do not run unreviewed images or scripts on a personal device. Early research should use documentation, source review, and appropriate emulated environments.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
└── docs/
    ├── ARCHITECTURE.md
    └── ROADMAP.md
```

## Current status

See [docs/ROADMAP.md](docs/ROADMAP.md) for milestones and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the initial system model.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request. Please include sources for hardware facts and clearly label assumptions.

## License

Original project documentation and code are licensed under the MIT License in [LICENSE](LICENSE), unless a file states otherwise. Third-party and upstream components retain their own licenses. Do not assume that MIT applies to Apple's code, vendor files, firmware, or other third-party materials.

## Disclaimer

“Apple”, “iOS”, “Darwin”, “XNU”, and “Motorola” are referenced only to identify technologies and the target device. All respective names and marks belong to their owners. MotoDarwin18 is independent and is not affiliated with, sponsored by, or endorsed by Apple or Motorola.
