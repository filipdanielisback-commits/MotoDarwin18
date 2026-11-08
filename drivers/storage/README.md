# Storage

**Status: research only — no Moto G60 storage-driver implementation.**

Scope: storage-controller identity, media type, partition and volume abstractions, and the boundary to XNU's block and filesystem layers.

The exact XT2135-2 storage component and controller configuration are not yet established. Shared Hanoip device-tree aliases are not sufficient to prove the physical storage variant or its firmware contract.

This project will not use this research scaffold to define write operations, partition changes, formatting, or firmware modification. Future documentation should prioritize read-only source analysis, provenance, and host-side models.

See [driver research rules](../README.md).
