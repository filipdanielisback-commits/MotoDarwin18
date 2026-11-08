# Research and experiment policy

MotoDarwin18 is documentation-first. This policy keeps investigations reproducible, non-destructive, and honest about what has actually been demonstrated.

## Allowed research activities

- Read public technical documentation and source code.
- Compare documented hardware capabilities with documented operating-system requirements.
- Create diagrams, inventories, compatibility matrices, and written analyses.
- Review licenses and provenance before referencing or reusing third-party work.
- Use non-destructive observations and already-published device information.
- Record uncertainties rather than filling gaps with guesses.

## Out of scope for this project documentation

This repository does not provide instructions for bypassing device security, defeating verified boot, changing protected boot configuration, flashing partitions, or modifying a daily-use phone. Do not treat a research note as authorization to alter a device.

## Before recording an experiment

Document the following at a high level:

| Item | What to record |
|---|---|
| Objective | The question the experiment is intended to answer |
| Scope | Whether it is literature research, static analysis, or a non-destructive observation |
| Target | Exact model and software version, if known |
| Evidence | Source documents, observations, and dates |
| Risks | Potential data loss, device instability, privacy, or legal concerns |
| Authorization | Confirm that any device or data involved is used with the owner's permission |
| Outcome | What was actually observed, including failures |
| Limitations | What the result does not prove |

## Reproducibility

A useful report should identify versions and sources, distinguish facts from inference, and avoid publishing personal data, credentials, private keys, or proprietary files.

## Reporting results

Use precise language:
- “Documented” means supported by a cited source.
- “Observed” means directly seen in a clearly described, non-destructive observation.
- “Inferred” means a reasoned conclusion that has not been directly demonstrated.
- “Unknown” means evidence is not currently available.
- “Demonstrated” should be reserved for repeatable evidence of the exact stated result.

A successful source-code build, by itself, does not demonstrate that a kernel boots on the target device or that a complete operating system works.

## Safety and project status

Do not use a personal or essential device as an experimental target. Keep this repository focused on research records and safe, authorized work. Update the README if the project's scope or status changes.
