# Input

**Status: research only — no Moto G60 input-driver implementation.**

Scope: touchscreen, physical buttons, input-event representation, and the boundary between platform input and the UI model.

The exact XT2135-2 touchscreen controller, panel pairing, board revision, and availability of pre-OS input services remain unconfirmed. A Hanoip-family touchscreen node is not proof of the target's exact controller.

The existing host-side touch model is not a hardware driver. No bus transactions, controller register sequences, firmware interaction, or device-specific calibration are specified here.

See [driver research rules](../README.md).
