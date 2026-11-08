"""Project-owned, host-only driver metadata and lifecycle value types."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DriverState(str, Enum):
    REGISTERED = "registered"
    INITIALIZING = "initializing"
    READY = "ready"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class CapabilityState(str, Enum):
    UNKNOWN = "unknown"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class DriverErrorCode(str, Enum):
    INITIALIZATION_FAILED = "initialization_failed"
    SHUTDOWN_FAILED = "shutdown_failed"


@dataclass(frozen=True)
class DriverCapability:
    """Descriptive capability; AVAILABLE is not proof of target hardware support."""

    name: str
    state: CapabilityState = CapabilityState.UNKNOWN
    evidence: str | None = None


@dataclass(frozen=True)
class DriverDescriptor:
    """Stable descriptive metadata supplied by a driver implementation."""

    driver_id: str
    name: str
    version: str
    capabilities: tuple[DriverCapability, ...] = ()
    description: str = ""


@dataclass(frozen=True)
class DriverError:
    code: DriverErrorCode
    message: str


@dataclass(frozen=True)
class DriverSnapshot:
    descriptor: DriverDescriptor
    state: DriverState
    last_error: DriverError | None = None
