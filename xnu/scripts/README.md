# XNU Research Scripts

This directory is reserved for reproducible source-management and non-device validation helpers.

**Current status:** no executable scripts are included.

## Appropriate future scope

Scripts may eventually help with:

- Checking that a local source checkout matches a recorded upstream commit.
- Listing patch files in deterministic order.
- Checking patch formatting or whether a patch applies to a local source tree.
- Producing a source inventory and license-notice report.
- Running static checks that do not interact with a connected device.

## Requirements

Every script must document:

- Purpose and expected result.
- Inputs, outputs, and supported host environment.
- Whether it changes files; default to read-only behavior.
- How errors are reported.
- How its result can be independently checked.
- Any external tools and their versions.

## Safety and integrity boundaries

- Do not interact with a connected phone.
- Do not unlock, flash, erase, repartition, or otherwise change device state.
- Do not retrieve proprietary firmware, operating-system images, keys, or credentials.
- Do not disable host security controls.
- Do not execute downloaded code as part of a validation check.
- Prefer explicit paths and deterministic inputs over implicit environment assumptions.

A successful source-level check does not establish that a kernel boots or that a device is supported.
