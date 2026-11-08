"""Host-side driver registry and lifecycle manager.

The registry invokes only the abstract initialize/shutdown methods supplied
by a registered Python object. It contains no hardware or firmware operations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from .model import (
    DriverDescriptor,
    DriverError,
    DriverErrorCode,
    DriverSnapshot,
    DriverState,
)


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")


class Driver(Protocol):
    @property
    def descriptor(self) -> DriverDescriptor:
        """Return immutable descriptive metadata."""

    def initialize(self) -> None:
        """Enter the driver's ready state."""

    def shutdown(self) -> None:
        """Leave the driver's ready state."""


class InvalidDriverDescriptorError(ValueError):
    """Raised when driver metadata is malformed."""


class DuplicateDriverError(ValueError):
    """Raised when a driver identifier is already registered."""


class UnknownDriverError(KeyError):
    """Raised when an operation references an unregistered driver."""


class InvalidDriverStateError(RuntimeError):
    """Raised when a lifecycle operation is not valid in the current state."""


@dataclass
class _DriverEntry:
    driver: Driver
    descriptor: DriverDescriptor
    state: DriverState = DriverState.REGISTERED
    last_error: DriverError | None = None

    def snapshot(self) -> DriverSnapshot:
        return DriverSnapshot(self.descriptor, self.state, self.last_error)


def validate_descriptor(descriptor: DriverDescriptor) -> None:
    if not isinstance(descriptor, DriverDescriptor):
        raise InvalidDriverDescriptorError("descriptor must be a DriverDescriptor")
    if not isinstance(descriptor.driver_id, str) or not _IDENTIFIER.fullmatch(descriptor.driver_id):
        raise InvalidDriverDescriptorError("driver_id must be a lowercase identifier")
    if not isinstance(descriptor.name, str) or not descriptor.name.strip():
        raise InvalidDriverDescriptorError("name must be a non-empty string")
    if not isinstance(descriptor.version, str) or not descriptor.version.strip():
        raise InvalidDriverDescriptorError("version must be a non-empty string")
    if not isinstance(descriptor.description, str):
        raise InvalidDriverDescriptorError("description must be a string")
    if not isinstance(descriptor.capabilities, tuple):
        raise InvalidDriverDescriptorError("capabilities must be a tuple")

    seen: set[str] = set()
    for capability in descriptor.capabilities:
        if not isinstance(capability.name, str) or not _IDENTIFIER.fullmatch(capability.name):
            raise InvalidDriverDescriptorError("capability names must be lowercase identifiers")
        if capability.name in seen:
            raise InvalidDriverDescriptorError("capability names must be unique")
        seen.add(capability.name)
        if not isinstance(capability.state, __import__(
            "drivers.core.model", fromlist=["CapabilityState"]
        ).CapabilityState):
            raise InvalidDriverDescriptorError("capability state is invalid")
        if capability.evidence is not None and not isinstance(capability.evidence, str):
            raise InvalidDriverDescriptorError("capability evidence must be a string or None")


class DriverRegistry:
    """Single-threaded registry for abstract driver lifecycle tests.

    Registration does not initialize a driver. Capability metadata is
    descriptive only and is never inferred from the host or a target device.
    """

    def __init__(self) -> None:
        self._entries: dict[str, _DriverEntry] = {}

    def register(self, driver: Driver) -> DriverSnapshot:
        try:
            descriptor = driver.descriptor
        except Exception as exc:
            raise InvalidDriverDescriptorError("driver descriptor could not be read") from exc
        validate_descriptor(descriptor)
        if not callable(getattr(driver, "initialize", None)):
            raise InvalidDriverDescriptorError("driver must provide initialize()")
        if not callable(getattr(driver, "shutdown", None)):
            raise InvalidDriverDescriptorError("driver must provide shutdown()")
        if descriptor.driver_id in self._entries:
            raise DuplicateDriverError(descriptor.driver_id)

        entry = _DriverEntry(driver=driver, descriptor=descriptor)
        self._entries[descriptor.driver_id] = entry
        return entry.snapshot()

    def get(self, driver_id: str) -> DriverSnapshot:
        entry = self._entries.get(driver_id)
        if entry is None:
            raise UnknownDriverError(driver_id)
        return entry.snapshot()

    def list(self) -> tuple[DriverSnapshot, ...]:
        return tuple(
            self._entries[key].snapshot()
            for key in sorted(self._entries)
        )

    def initialize(self, driver_id: str) -> DriverSnapshot:
        entry = self._require(driver_id)
        if entry.state not in (DriverState.REGISTERED, DriverState.STOPPED):
            raise InvalidDriverStateError(
                f"cannot initialize driver in state {entry.state.value}"
            )

        entry.state = DriverState.INITIALIZING
        entry.last_error = None
        try:
            entry.driver.initialize()
        except Exception as exc:
            entry.state = DriverState.FAILED
            entry.last_error = DriverError(
                DriverErrorCode.INITIALIZATION_FAILED,
                f"{type(exc).__name__}: {exc}",
            )
            return entry.snapshot()

        entry.state = DriverState.READY
        return entry.snapshot()

    def shutdown(self, driver_id: str) -> DriverSnapshot:
        entry = self._require(driver_id)
        if entry.state is not DriverState.READY:
            raise InvalidDriverStateError(
                f"cannot shut down driver in state {entry.state.value}"
            )

        entry.state = DriverState.STOPPING
        try:
            entry.driver.shutdown()
        except Exception as exc:
            entry.state = DriverState.FAILED
            entry.last_error = DriverError(
                DriverErrorCode.SHUTDOWN_FAILED,
                f"{type(exc).__name__}: {exc}",
            )
            return entry.snapshot()

        entry.state = DriverState.STOPPED
        entry.last_error = None
        return entry.snapshot()

    def unregister(self, driver_id: str) -> DriverSnapshot:
        entry = self._require(driver_id)
        if entry.state not in (DriverState.REGISTERED, DriverState.STOPPED):
            raise InvalidDriverStateError(
                f"cannot unregister driver in state {entry.state.value}"
            )
        snapshot = entry.snapshot()
        del self._entries[driver_id]
        return snapshot

    def _require(self, driver_id: str) -> _DriverEntry:
        entry = self._entries.get(driver_id)
        if entry is None:
            raise UnknownDriverError(driver_id)
        return entry
