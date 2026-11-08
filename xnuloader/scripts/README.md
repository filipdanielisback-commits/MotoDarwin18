# Loader Scripts

Reserved for reproducible source-only checks and documentation helpers.

**Current status:** no scripts are implemented.

## Suitable future tasks

- Check formatting and repository structure.
- Validate documentation links and required metadata.
- Inventory source files and license notices.
- Verify that local research records refer to the expected source revision.
- Run static checks on project-owned source in an isolated environment.

## Boundaries

Scripts must not interact with a connected phone or alter device state. Do not add automation for unlocking, flashing, erasing, repartitioning, changing protected boot settings, or installing firmware.

Every script must document its inputs, outputs, dependencies, side effects, and limitations. Prefer read-only behavior and deterministic local inputs.

A passing static check does not demonstrate that a loader works or that a device is supported.
