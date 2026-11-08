"""Host-only XNULoader display metadata and layout model.

This module computes geometry only. It never draws pixels or accesses a display,
UEFI service, framebuffer, firmware, or connected device.
"""
from __future__ import annotations

from dataclasses import dataclass


KNOWN_PIXEL_FORMATS = {
    "PixelRedGreenBlueReserved8BitPerColor",
    "PixelBlueGreenRedReserved8BitPerColor",
    "PixelBitMask",
    "PixelBltOnly",
}


@dataclass(frozen=True)
class DisplayMode:
    width: int
    height: int
    pixels_per_scan_line: int
    pixel_format: str

    def validate(self) -> None:
        if not isinstance(self.width, int) or isinstance(self.width, bool) or self.width <= 0:
            raise ValueError("width must be a positive integer")
        if not isinstance(self.height, int) or isinstance(self.height, bool) or self.height <= 0:
            raise ValueError("height must be a positive integer")
        if (
            not isinstance(self.pixels_per_scan_line, int)
            or isinstance(self.pixels_per_scan_line, bool)
            or self.pixels_per_scan_line < self.width
        ):
            raise ValueError("pixels_per_scan_line must be an integer >= width")
        if self.pixel_format not in KNOWN_PIXEL_FORMATS:
            raise ValueError("unsupported or unknown pixel format")


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    def inside(self, width: int, height: int) -> bool:
        return (
            self.x >= 0
            and self.y >= 0
            and self.width > 0
            and self.height > 0
            and self.x + self.width <= width
            and self.y + self.height <= height
        )


@dataclass(frozen=True)
class MenuLayout:
    title: Rect
    items: tuple[Rect, ...]
    status: Rect


def calculate_menu_layout(mode: DisplayMode, item_count: int) -> MenuLayout:
    """Return responsive logical rectangles for synthetic display dimensions."""
    mode.validate()
    if not isinstance(item_count, int) or isinstance(item_count, bool) or item_count < 1:
        raise ValueError("item_count must be a positive integer")

    margin = max(12, min(32, mode.width // 16))
    gap = max(8, min(20, mode.height // 80))
    title_height = max(36, min(64, mode.height // 12))
    status_height = max(28, min(48, mode.height // 16))
    available_width = mode.width - 2 * margin
    if available_width < 80:
        raise ValueError("display is too narrow for the minimum layout")

    content_top = margin + title_height + gap
    content_bottom = mode.height - margin - status_height - gap
    content_height = content_bottom - content_top
    item_gap_total = gap * (item_count - 1)
    item_height = (content_height - item_gap_total) // item_count
    if item_height < 44:
        raise ValueError("display is too small for the requested menu")

    item_width = min(available_width, max(80, int(mode.width * 0.84)))
    item_x = (mode.width - item_width) // 2
    title_width = min(available_width, max(80, int(mode.width * 0.88)))
    title = Rect((mode.width - title_width) // 2, margin, title_width, title_height)

    items = tuple(
        Rect(item_x, content_top + index * (item_height + gap), item_width, item_height)
        for index in range(item_count)
    )
    status_y = mode.height - margin - status_height
    status = Rect(margin, status_y, available_width, status_height)

    result = MenuLayout(title=title, items=items, status=status)
    rects = (result.title, *result.items, result.status)
    if not all(rect.inside(mode.width, mode.height) for rect in rects):
        raise ValueError("calculated layout falls outside the visible display area")
    return result
