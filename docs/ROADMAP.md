# MotoDarwin18 Research Roadmap

This roadmap describes investigation milestones, not a promise that a complete port is technically possible.

## Phase 0 — Project foundations

- [x] Create the repository and establish its scope.
- [x] Add an initial project overview and license boundary.
- [ ] Record project decisions and source references.
- [ ] Add a hardware-facts table with source links and confidence levels.

## Phase 1 — Device and platform research

- [ ] Confirm the exact XT2135-2 hardware configuration from reliable sources.
- [ ] Identify the SoC family, CPU architecture, memory layout information available publicly, and major peripherals.
- [ ] Separate verified facts from estimates and unknowns.
- [ ] Create a subsystem inventory: display, graphics, storage, input, audio, networking, power, and sensors.

## Phase 2 — Operating-system architecture study

- [ ] Document the high-level relationship between firmware, boot environment, kernel, drivers, and user space.
- [ ] Study ARM64 platform requirements and device-description concepts.
- [ ] Review upstream XNU architecture and its applicable license terms.
- [ ] Create a compatibility matrix without claiming unsupported functionality.

## Phase 3 — Non-destructive feasibility work

- [ ] Evaluate what can be learned through source inspection and emulation.
- [ ] Document build prerequisites and reproducible research environments.
- [ ] Keep device-altering experiments out of scope until risks, permissions, and recovery considerations have been independently reviewed.

## Phase 4 — Prototype decision

A prototype should only be proposed after the earlier research establishes a technically and legally sound path. Any proposal must include:

- A precise scope and known limitations.
- A component-by-component license and provenance review.
- A safety and device-integrity review.
- A test plan that does not rely on unsupported claims.

## Definition of done for research claims

Every compatibility claim should include the tested component, environment, date, evidence, limitations, and a reproducible description. “Planned”, “partially understood”, and “working” must never be used interchangeably.
