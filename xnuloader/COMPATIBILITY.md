# Loader Compatibility Register

**Target:** Motorola Moto G60 XT2135-2  
**Platform family:** Qualcomm Snapdragon 732G  
**Status:** Initial research register; no loader compatibility is established.

## Compatibility questions

| Area | Evidence required | Status |
|---|---|---|
| Firmware environment | Authoritative documentation for the exact target | Unknown |
| Execution architecture | Exact processor and execution-context facts | Partially documented at SoC level |
| Image format | Documented kernel image expectations for selected XNU revision | Unknown |
| Image metadata | Supported metadata and versioning contract | Unknown |
| Memory description | Exact target memory map and reserved regions | Unknown |
| Platform description | Documented format and exact target contents | Unknown |
| Interrupt context | Platform-specific controller and routing information | Unknown |
| Timer context | Documented timer facilities and configuration | Unknown |
| Diagnostics | Supported early diagnostic interface | Unknown |
| Kernel compatibility | Requirements of a selected immutable XNU source revision | No revision selected |
| Licensing | Provenance and terms for every dependency | Pending per dependency |

## Status definitions

- **Unknown:** insufficient evidence.
- **Partially documented:** some general facts exist, but exact target details are missing.
- **Documented:** primary evidence establishes the stated interface or requirement.
- **Implemented:** original project code exists and has been reviewed.
- **Validated:** a defined test has passed; scope and limitations are recorded.
- **Unsupported:** evidence establishes that the requirement cannot be met.

## Evidence record template

For each resolved item, record:

- Claim and exact scope.
- Source title, publisher, URL, version, and date.
- Whether the evidence describes the SoC family or the exact XT2135-2.
- Confidence and limitations.
- Related project document or source file.
- Review date.

## Current assessment

The available public handset and SoC specifications do not establish the target firmware interface, loader environment, kernel image contract, or handoff data. No compatibility claim should be made until these are documented.
