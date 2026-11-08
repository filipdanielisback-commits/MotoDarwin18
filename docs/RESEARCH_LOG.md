# Research log

A concise record of research decisions and evidence. Add new entries at the top. Keep observations separate from assumptions and conclusions.

## 2026-11-08 — Documentation foundation expanded

### Work recorded

- Added a device hardware inventory for Moto G60 XT2135-2.
- Added a compatibility matrix for major Darwin/XNU platform areas.
- Added a references index and technical glossary.
- Added this log, a platform integration checklist, a source provenance policy, and an experiment review policy.

### Findings and limits

- The public XNU repository describes XNU as part of Darwin and documents ARM64 among its supported architectures in the current repository README.
- XNU's source tree includes both general kernel subsystems and platform-specific areas. This supports the project's emphasis on platform integration rather than CPU compatibility alone.
- Independent ARM64 porting documentation highlights the need to collect board-specific details such as memory reservations, interrupt controllers, storage, display, touch, wireless components and firmware versions.
- These general references do not demonstrate Moto G60 XT2135-2 support.

### Current project conclusion

**No working Moto G60 Darwin/XNU port is claimed.** Hardware inventory and compatibility status remain incomplete. All device-specific claims must be supported by exact-model evidence.

### Sources

- [Apple XNU repository](https://github.com/apple-oss-distributions/xnu)
- [UniXNU: Port a device](https://unixnu.com/porting/steps)
- [UniXNU: Architecture overview](https://unixnu.com/porting/)

## Entry template

### YYYY-MM-DD — Short title

**Question:** What was being investigated?

**Sources:** Link primary sources and record versions or dates.

**Verified facts:**
- 

**Observations:**
- 

**Inferences (labelled):**
- 

**Unknowns / contradictions:**
- 

**Conclusion:** What can and cannot be claimed?

**Next research task:**
- 
