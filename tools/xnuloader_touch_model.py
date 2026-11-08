"""Host-only XNULoader absolute-touch event state model.

Consumes synthetic samples only. It never accesses hardware, firmware, or a phone.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TouchRange:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def __post_init__(self) -> None:
        values = (self.min_x, self.max_x, self.min_y, self.max_y)
        if any(not isinstance(v, int) or isinstance(v, bool) for v in values):
            raise ValueError("coordinate bounds must be integers")
        if self.min_x >= self.max_x or self.min_y >= self.max_y:
            raise ValueError("coordinate ranges must have min less than max")


@dataclass(frozen=True)
class TouchSample:
    contact: bool
    x: int | None = None
    y: int | None = None
    failed: bool = False


@dataclass(frozen=True)
class TouchEvent:
    kind: str
    x: int
    y: int


class TouchEventModel:
    """Convert synthetic absolute-pointer samples into down/move/up/cancel events."""

    def __init__(self, coordinate_range: TouchRange):
        if not isinstance(coordinate_range, TouchRange):
            raise TypeError("coordinate_range must be a TouchRange")
        self.coordinate_range = coordinate_range
        self._active = False
        self._last: tuple[int, int] | None = None

    @property
    def contact_active(self) -> bool:
        return self._active

    def _valid_point(self, x: object, y: object) -> bool:
        r = self.coordinate_range
        return (
            isinstance(x, int) and not isinstance(x, bool)
            and isinstance(y, int) and not isinstance(y, bool)
            and r.min_x <= x <= r.max_x
            and r.min_y <= y <= r.max_y
        )

    def _cancel(self) -> TouchEvent | None:
        if not self._active or self._last is None:
            self._active = False
            self._last = None
            return None
        x, y = self._last
        self._active = False
        self._last = None
        return TouchEvent("cancel", x, y)

    def process(self, sample: TouchSample) -> TouchEvent | None:
        if not isinstance(sample, TouchSample):
            raise TypeError("sample must be a TouchSample")
        if not isinstance(sample.contact, bool) or not isinstance(sample.failed, bool):
            raise ValueError("contact and failed flags must be boolean")
        if sample.failed:
            return self._cancel()

        if sample.contact:
            if not self._valid_point(sample.x, sample.y):
                if self._active:
                    return self._cancel()
                raise ValueError("contact sample has invalid or out-of-range coordinates")
            point = (sample.x, sample.y)
            kind = "move" if self._active else "down"
            self._active = True
            self._last = point
            return TouchEvent(kind, *point)

        if self._active and self._last is not None:
            x, y = self._last
            self._active = False
            self._last = None
            return TouchEvent("up", x, y)
        return None
