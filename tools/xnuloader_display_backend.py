"""Host-only XNULoader display-backend contract model.

This module validates abstract requests. It does not render pixels, access a
framebuffer, call UEFI, or communicate with firmware or a device.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from tools.xnuloader_display_layout import DisplayMode, Rect


class ServiceState(str, Enum):
    NOT_CHECKED = "not_checked"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


class TransferMethod(str, Enum):
    GOP_BLT = "gop_blt"
    LINEAR_FRAMEBUFFER = "linear_framebuffer"


class CommandKind(str, Enum):
    CLEAR = "clear"
    FILL_RECT = "fill_rect"
    TEXT = "text"


class PresentStatus(str, Enum):
    ACCEPTED = "accepted"
    UNAVAILABLE = "unavailable"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"


@dataclass(frozen=True)
class DisplayServiceReport:
    state: ServiceState
    mode: DisplayMode | None = None
    transfer_methods: tuple[TransferMethod, ...] = ()
    error_code: str | None = None

    def validate(self) -> None:
        if not isinstance(self.state, ServiceState):
            raise ValueError("state must be a ServiceState")
        if self.state is ServiceState.AVAILABLE:
            if self.mode is None:
                raise ValueError("available service requires mode metadata")
            self.mode.validate()
            if not self.transfer_methods:
                raise ValueError("available service requires a transfer method")
            if any(not isinstance(method, TransferMethod) for method in self.transfer_methods):
                raise ValueError("unknown transfer method")
            if self.error_code is not None:
                raise ValueError("available service cannot carry an error code")
            return
        if self.mode is not None or self.transfer_methods:
            raise ValueError("non-available service cannot expose usable mode or methods")
        if self.state is ServiceState.ERROR:
            if not isinstance(self.error_code, str) or not self.error_code.strip():
                raise ValueError("error state requires an error code")
        elif self.error_code is not None:
            raise ValueError("only error state may carry an error code")


@dataclass(frozen=True)
class DisplayCommand:
    kind: CommandKind
    rect: Rect | None = None
    text: str | None = None


@dataclass(frozen=True)
class DisplayFrame:
    commands: tuple[DisplayCommand, ...]

    def validate(self, mode: DisplayMode) -> None:
        mode.validate()
        if not isinstance(self.commands, tuple) or not self.commands:
            raise ValueError("frame must contain at least one command")
        for command in self.commands:
            if not isinstance(command, DisplayCommand) or not isinstance(command.kind, CommandKind):
                raise ValueError("frame contains an unsupported command")
            if command.kind is CommandKind.CLEAR:
                if command.rect is not None or command.text is not None:
                    raise ValueError("clear command cannot carry geometry or text")
            elif command.kind is CommandKind.FILL_RECT:
                if command.rect is None or command.text is not None:
                    raise ValueError("fill command requires only a rectangle")
                if not command.rect.inside(mode.width, mode.height):
                    raise ValueError("fill rectangle is outside the visible mode")
            elif command.kind is CommandKind.TEXT:
                if command.rect is None or not isinstance(command.text, str) or not command.text.strip():
                    raise ValueError("text command requires an anchor rectangle and non-empty text")
                if not command.rect.inside(mode.width, mode.height):
                    raise ValueError("text anchor rectangle is outside the visible mode")


def validate_presentation(report: DisplayServiceReport, frame: DisplayFrame) -> None:
    """Validate a logical frame against descriptive service metadata only."""
    report.validate()
    if report.state is not ServiceState.AVAILABLE or report.mode is None:
        raise ValueError("display service is not available")
    frame.validate(report.mode)


class DisplayBackend(Protocol):
    """Future adapter contract; no concrete firmware adapter exists."""

    def discover(self) -> DisplayServiceReport:
        """Return verified service metadata without inventing capabilities."""
        ...

    def present(self, frame: DisplayFrame) -> PresentStatus:
        """Submit a logical frame and report the actual result."""
        ...
