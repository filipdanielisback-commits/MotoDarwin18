# XT2135-2 Firmware and Board-Revision Documentation Follow-up

**Review date:** 2026-11-08  
**Target:** Motorola moto g60 vision, XT2135-2 / MC38C  
**Scope:** Public-source documentation review only  
**Outcome:** Exact board revision and firmware-to-XNU handoff remain undocumented in the reviewed public evidence

## 1. Question

Can public, authoritative documentation identify the physical XT2135-2 motherboard revision, map it to the Hanoip DVT1/DVT2 overlays, or define the firmware-to-OS handoff needed for the pinned XNU baseline?

## 2. Manufacturer documentation located

### 2.1 Motorola model declaration

Motorola's compliance index explicitly lists XT2135-2 as MC38C / moto g60 vision and separately lists XT2135-1 as MC38B / moto g60. This is strong exact-model identity evidence, but it is not a PCB assembly/revision identifier.

Source: [Motorola Declarations of Conformity](https://en-gb.support.motorola.com/app/answers/detail/a_id/167829/~/declarations-of-conformity).

### 2.2 Motorola Right to Repair documentation portal

Motorola's official Right to Repair page states that parts lists, disassembly/assembly manuals and detailed schematics are made available through its repair-document channel. Its FAQ points to the distributor site for device manuals and parts lists.

The linked partner page could not be inspected in this review because it returned a JavaScript/anti-bot interstitial. No XT2135-2-specific service document, board assembly number, PCB revision or DVT mapping was independently verified from that channel.

Sources:
- [Motorola Right to Repair](https://en-emea.support.motorola.com/app/right-to-repair)
- [Motorola-linked repair documents portal](https://www.replacebase.eu/motorola-guide)

This is a credible route by which model-specific service documentation may be catalogued, but the existence of a portal is not evidence of any particular XT2135-2 board revision.

## 3. Public third-party service-document leads

### 3.1 EletrônicaBR listing

A third-party file listing titled “XT2135-X, G60 and G40 Motherboard Service Manual - Schematic” describes a package for the shared Hanoi platform and says it covers XT2135-X / G60 / G40. It lists schematic, component-location and service-manual material, but the actual download is restricted and the listing does not identify MC38C specifically, a physical PCB revision, or a DVT overlay.

Assessment: **unverified family-level lead only**. The listing cannot be used to confirm the target's component population or board revision.

Source: [EletrônicaBR XT2135-X / G60 / G40 listing](https://eletronicabr.com/en/topic/309099-xt2135-x-g60-and-g40-motherboard-service-manual-schematic/).

### 3.2 Other schematic indexes

A separate third-party schematic index advertises an “XT2135-x” component-location item and labels it XT2135-2. The index does not expose a verifiable board revision or the underlying document contents in the reviewed page.

Assessment: **secondary lead only**. A page title or search label is not enough to authenticate the document or map a board assembly to DVT1/DVT2.

Source: [DZKJ XT2135-x component-location listing](https://www.dzkj16888.com/index.php?c=read&desc=0&id=15125&page=1).

## 4. Firmware and source provenance

Motorola's kernel-source tracker issue #574 names an exact XT2135-2 European Android 12 firmware build identifier and a Motorola contributor links the corresponding published `kernel-msm` source release tag `MMI-S2RIS32.32-20-9-9-2-3`.

This is stronger than a generic Hanoip codename: it connects an exact XT2135-2 firmware build to the Android/Linux kernel source publication. It still does not publish the firmware-to-XNU handoff contract, boot CPU state, Apple `boot_args` producer, SecureDT format, exact board assembly revision or complete memory ownership map.

Source: [Motorola kernel-msm issue #574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574).

Android's general device-tree overlay documentation explains that Android bootloaders can combine a base DTB with a device-specific overlay before passing a unified DTB to Linux. This is useful background for why overlay selection matters, but it does not establish which overlay is selected on XT2135-2 or the format passed by its firmware.

Source: [Android Open Source Project — Device tree overlays](https://source.android.com/docs/core/architecture/dto).

## 5. Evidence classification

| Question | Evidence found | Status |
|---|---|---|
| Is XT2135-2 / MC38C the moto g60 vision? | Motorola compliance index | **Confirmed** |
| Is there a Motorola Android kernel-source trail for an exact XT2135-2 build? | Motorola issue #574 and linked source tag | **Confirmed source provenance** |
| Does Motorola publicly state the exact PCB assembly/revision in the reviewed sources? | No such identifier located | **Unknown** |
| Is XT2135-2 mapped to Hanoip DVT1 or DVT2? | No authoritative mapping located | **Unknown** |
| Does the broad third-party service listing prove MC38C board population? | Listing covers XT2135-X / G60 / G40 collectively; document not verified | **No** |
| Does the reviewed evidence define the XT2135-2 firmware-to-XNU entry state? | No | **Unknown** |
| Does it define an Apple-compatible `boot_args` producer? | No | **Unknown** |
| Does it define the exact device-tree handoff format and lifetime? | No | **Unknown** |
| Does it define complete physical RAM and firmware ownership? | No | **Unknown** |

## 6. Decision

The public-source search did not resolve the physical board revision, DVT overlay mapping or XNU firmware handoff.

Do not:
- Select DVT1 or DVT2 for XT2135-2 based on the shared `hanoip` label.
- Treat a broad third-party XT2135-X service listing as an authenticated MC38C board record.
- Infer the boot firmware's handoff format from Linux DTS sources or Android kernel source publication.
- Treat the existence of Android firmware artifacts as proof of UEFI or XNU compatibility.

No executable kernel patch is justified by this evidence. The XNU audit still has no demonstrated source defect or exact producer/consumer mismatch.

## 7. Remaining evidence requirement

The useful missing artifact is a manufacturer-authenticated or otherwise independently verifiable record that links **XT2135-2 / MC38C → motherboard assembly/PCB revision → applicable Hanoip overlay / component population**. A separate authoritative firmware interface specification would be needed to define entry state, memory ownership and device-tree handoff.

If no public document establishes these links, the correct engineering record is “unknown”, not an inferred board revision.

*Documentation and public-source review only. No device inspection, firmware extraction, boot configuration change, boot payload construction or device modification was performed.*
