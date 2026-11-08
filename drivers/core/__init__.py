"""MotoDarwin18 host-side driver framework.

This package models driver metadata and lifecycle only. It does not access
hardware, firmware, XNU internals, or a phone.
"""

from .model import (
    CapabilityState,
    DriverCapability,
    DriverDescriptor,
    DriverError,
    DriverErrorCode,
    DriverState,
    DriverSnapshot,
)
from .registry import (
    DriverRegistry,
    DuplicateDriverError,
    InvalidDriverDescriptorError,
    InvalidDriverStateError,
    UnknownDriverError,
)

__all__ = [
    "CapabilityState",
    "DriverCapability",
    "DriverDescriptor",
    "DriverError",
    "DriverErrorCode",
    "DriverState",
    "DriverSnapshot",
    "DriverRegistry",
    "DuplicateDriverError",
    "InvalidDriverDescriptorError",
    "InvalidDriverStateError",
    "UnknownDriverError",
]
