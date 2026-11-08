# Proposal 0001 — ARM64 Early Boot Contract Compatibility

> **Status:** Research proposal; no executable kernel patch.
> **Target baseline:** Apple XNU `xnu-11215.1.10`
> **Pinned commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`
> **Target:** Motorola Moto G60 XT2135-2
> **Disposition:** Needs producer-side evidence before a source change can be justified.

## Problem statement

The pinned XNU ARM64 startup path consumes an Apple-defined `boot_args` structure and early platform metadata. The existing source reviews trace the consumers in:

- `pexpert/pexpert/arm64/boot.h`
- `pexpert/arm/pe_init.c`
- `osfmk/arm/arm_init.c`
- `osfmk/arm64/arm_vm_init.c`

The reviewed contract includes revision/version fields, physical and virtual memory metadata, a device-tree pointer and length, video metadata, and a command-line buffer. XNU's early Platform Expert path captures and interprets these values before later startup code consumes device-tree properties.

The compatibility gap is not yet a demonstrated defect in Apple's source. It is that MotoDarwin18 has not established an exact XT2135-2 producer contract that supplies the semantics XNU expects.

## Evidence

- [Pinned XNU baseline](../../UPSTREAM.md): immutable source revision and provenance.
- [Boot handoff field reference](../../../docs/BOOT_HANDOFF_FIELD_REFERENCE.md): fields and consumers reviewed in the pinned source.
- [Boot ABI compatibility gaps](../../../docs/BOOT_ABI_COMPATIBILITY_GAPS.md): producer, memory, device-tree, CPU-state, and platform gaps.
- [Early platform dependency inventory](../../../docs/XNU_EARLY_PLATFORM_DEPENDENCIES.md): startup dependency classifications.
- [Secure device-tree requirements](../../../docs/SECURE_DEVICE_TREE_REQUIREMENTS.md): XNU SecureDT representation and queried properties.

## Compatibility assessment

| Contract area | XNU consumer expectation | XT2135-2 producer evidence | Status |
|---|---|---|---|
| Structure revision/version | Recognized `boot_args` revision and version | No exact producer ABI documented | Unknown |
| Memory fields | Coherent physical/virtual bases, sizes, and kernel-data boundary | No complete exact-target map or producer semantics | Unknown |
| Device tree | Pointer, length, and XNU SecureDT-compatible representation | Linux DTS family clues exist; XNU representation and producer remain unproven | Unknown |
| Machine identity | XNU-recognized machine/platform identity | XT2135-2 regulatory identity known; no XNU machine mapping | Unknown |
| Video metadata | Structurally valid fields when consumed | Pre-OS display service and metadata source unknown | Unknown |
| CPU entry state | Valid ARM64 entry context and CPU state | No exact firmware-to-XNU entry contract | Unknown |

## Proposed compatibility work

The safe next engineering action is a source-level compatibility review, not a change to XNU startup code:

1. Keep the pinned XNU structure definition as the reference contract.
2. Record each producer field's meaning, width, alignment, ownership, and lifetime only when a primary source establishes it.
3. Mark every unproven field as unresolved; do not fill it from a Linux device tree by assumption.
4. Compare the two contracts in a review table before considering any source modification.
5. If a genuine source-level incompatibility is later demonstrated, isolate the smallest affected interface and document why the change is not a workaround for missing producer evidence.

No boot-argument parser, handoff adapter, startup branch, or kernel source modification is included here.

## Acceptance criteria for a future source fix

A future patch proposal must identify a specific incompatible field or semantic, cite both sides of the contract, demonstrate that the mismatch is not merely missing target information, and include a source-only validation plan. It must preserve upstream notices and receive file-level license review.

## Conclusion

**No XNU source compatibility bug has yet been proven.** The documented issue is an unresolved producer/consumer contract. Calling this a completed source fix would be inaccurate. This proposal records the exact evidence needed to justify one.

*Project: MotoDarwin18*

## Follow-up audit

The [ARM64 Boot Contract Compatibility Audit](../../source-reviews/ARM64_BOOT_CONTRACT_AUDIT.md) reviewed the project’s pinned-source records and target evidence on 2026-11-08.

**Decision:** no specific XNU source defect has been demonstrated. The current gap is missing producer-side evidence for XT2135-2. Keep this proposal at **Needs evidence**; do not turn it into an executable source patch until a concrete producer/consumer mismatch is established.


## Evidence reconciliation — 2026-11-08

The [XT2135-2 Confirmed Platform Facts and XNU Compatibility Review](../../../research/firmware/XT2135_2_CONFIRMED_PLATFORM_FACTS.md) has rechecked the target evidence against the pinned XNU consumer requirements.

**Disposition remains: Needs evidence.** The exact-model evidence still does not define the firmware producer's `boot_args`, CPU entry state, memory ownership or SecureDT contract. Do not create an executable source patch based only on shared hanoip Linux descriptions or missing producer documentation.
