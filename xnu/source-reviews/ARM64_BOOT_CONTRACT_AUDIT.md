# ARM64 Boot Contract Compatibility Audit

**Project:** MotoDarwin18  
**Target:** Motorola Moto G60 XT2135-2 / MC38C  
**XNU baseline:** `xnu-11215.1.10`  
**Pinned commit:** `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`  
**Audit date:** 2026-11-08  
**Status:** Documentation/source audit; no executable kernel patch and no target handoff validation.

## 1. Audit question

Does the available evidence demonstrate a defect in the pinned XNU source that requires a source compatibility patch for XT2135-2?

**Finding: No.** The reviewed material demonstrates an unresolved producer/consumer contract. It does not yet demonstrate that a particular XNU source statement is incorrect or that a known XT2135-2 producer supplies a conflicting value or format.

The correct status for proposal 0001 is therefore **Needs evidence**, not “fix identified”.

## 2. Evidence reviewed

Project records reviewed for this audit:

- [Boot handoff field reference](../../docs/BOOT_HANDOFF_FIELD_REFERENCE.md)
- [Boot ABI compatibility gaps](../../docs/BOOT_ABI_COMPATIBILITY_GAPS.md)
- [Secure device-tree requirements](../../docs/SECURE_DEVICE_TREE_REQUIREMENTS.md)
- [Device-tree property compatibility matrix](../../docs/DEVICE_TREE_PROPERTY_COMPATIBILITY_MATRIX.md)
- [Early platform service dependency inventory](../../docs/XNU_EARLY_PLATFORM_DEPENDENCIES.md)
- [Pinned source verification](PINNED_SOURCE_VERIFICATION.md)
- [ARM64 boot header review](ARM64_BOOT_HEADER_REVIEW.md)
- [Platform Expert initialization review](PE_INIT_REVIEW.md)
- [ARM startup review](ARM_INIT_REVIEW.md)
- [XT2135-2 identity evidence](../../research/soc/XT2135_2_IDENTITY.md)
- [Hanoip / SDMMAGPIE platform evidence](../../research/soc/HANOIP_PLATFORM_EVIDENCE.md)

The pinned source record identifies the exact tag and peeled commit. The boot handoff reference records declarations and selected consumer paths checked against that baseline. Some older source-review notes still contain “provisional” and “exact comparison pending” caveats; use the newer pinned verification and boot handoff reference for the recorded declaration/consumer facts, while retaining the older notes as historical review records until they are individually reconciled.

## 3. Contract comparison

| Contract area | Pinned XNU-side fact | XT2135-2-side evidence | Audit result |
|---|---|---|---|
| ABI revision/version | Header declares revision and version fields; a consumer gates `bootFlags` on revision | No exact Motorola producer ABI documented | Producer contract unknown |
| Physical/virtual memory | VM and startup consumers use base/size/boundary fields with distinct semantics | Shared Linux carveouts are not a complete physical map or XNU producer contract | No mismatch demonstrated |
| Actual memory size | Pinned VM path distinguishes nonzero `memSizeActual` from fallback behavior | Exact target producer semantics unavailable | Unknown |
| Machine identity | Early Platform Expert calls machine identification using boot arguments/platform data | Regulatory model identity is known; no XNU machine mapping established | Unknown |
| Device-tree pointer/length | Early PE captures pointer and length and initializes SecureDT | Exact firmware tree format, lifetime, addressability and ownership unknown | Unknown |
| SecureDT representation | Pinned SecureDT uses XNU-specific node/property records | Reviewed Moto sources are Linux DTS/FDT-family material; exact firmware handoff not established | Format compatibility unproven |
| DRAM properties | Reviewed ARM64 startup consumes `/chosen/dram-base` and `/chosen/dram-size` | Not documented in reviewed family source; actual target handoff unexamined | Producer evidence missing |
| CPU topology | Startup parses CPU/device-tree information | Shared family source offers clues, not exact handoff proof | Unknown |
| Video metadata | PE records boot video fields | Pre-OS display service and producer metadata unknown | Unknown |
| Command line/flags | Fixed command-line buffer and revisioned flags exist | No exact producer semantics established | Unknown |
| Entry CPU state | Startup depends on valid ARM64 entry context and platform state | No exact firmware-to-XNU entry contract | Unknown |

## 4. SecureDT finding

The pinned XNU SecureDT representation and standard Linux FDT are distinct binary formats. Similar logical concepts (nodes and properties) do not establish binary compatibility.

The reviewed Moto G60 family source tree is useful hardware-description evidence. It does not prove which representation the exact XT2135-2 firmware exposes to a hypothetical consumer, whether any intermediate component transforms it, or whether required XNU-style properties are present.

The absence of a property in the reviewed Linux source is not proof that it is absent from the phone's firmware handoff.

## 5. Source-fix decision

No patch to `boot.h`, `pe_init.c`, `arm_init.c`, SecureDT, or ARM64 VM startup is justified by the current evidence.

Changing XNU consumers to compensate for an unknown producer would be speculative. It could also conceal a missing platform contract rather than solve a demonstrated source compatibility defect.

The audit therefore does **not** create a C diff, alter an ABI, add platform conditionals, or define a phone-specific handoff implementation.

## 6. Evidence needed to reopen the patch decision

A future source-fix proposal must supply all of the following:

1. A specific pinned XNU declaration or consumer, identified by path and immutable source revision.
2. An authoritative description of the corresponding producer-side contract for exact XT2135-2 hardware/revision.
3. A precise, reproducible semantic or format mismatch between those two contracts.
4. Evidence that the mismatch is not merely an unknown, missing, or unverified producer capability.
5. A narrowly scoped proposed correction, with file-level provenance and license review.
6. A source-only validation plan that does not imply phone compatibility.

Until then, keep the source-fix proposal at **Needs evidence**.

## 7. Recommended next research task

Continue with the producer-side evidence inventory: identify public, authoritative documentation for the exact XT2135-2 firmware/OS handoff format, board revision, and memory ownership contract. Keep family-level Android/Linux sources clearly separated from exact-model evidence.

This is a documentation and source-review task only. It does not involve obtaining protected firmware, changing device configuration, constructing a handoff, building a boot payload, or modifying the handset.

## 8. Conclusion

The audit confirms that the largest blocker is not a proven bug in upstream XNU. It is the absence of an established XT2135-2 producer contract that can be compared with XNU's documented consumer requirements.

**Decision: no executable kernel compatibility patch at this stage.** The next milestone is stronger exact-model producer evidence.

*Project: MotoDarwin18*


## Follow-up: confirmed platform evidence reconciliation — 2026-11-08

The [XT2135-2 Confirmed Platform Facts and XNU Compatibility Review](../../research/firmware/XT2135_2_CONFIRMED_PLATFORM_FACTS.md) reconciles the exact-model Motorola declaration, Android kernel-source provenance and shared hanoip-family evidence against the pinned XNU requirements.

The new review does not change the audit decision: no exact XT2135-2 producer contract has been established for the Apple `boot_args` ABI, entry CPU state, memory ownership or SecureDT representation. GICv3/PDC and timer descriptions remain family-level clues, not an XNU implementation. No executable XNU source patch is justified.
