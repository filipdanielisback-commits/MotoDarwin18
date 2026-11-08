"""Platform-neutral, host-only XNULoader menu state model.

Selection intents are descriptive values only; this module never performs boot actions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class MenuItem:
    item_id: str
    label: str
    enabled: bool = False


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    def contains(self, px: int, py: int) -> bool:
        return self.width > 0 and self.height > 0 and (
            self.x <= px < self.x + self.width
            and self.y <= py < self.y + self.height
        )


@dataclass(frozen=True)
class SelectionIntent:
    """A UI selection notification, not an executable action."""

    item_id: str


class MenuModel:
    def __init__(self, items: Iterable[MenuItem]):
        self.items = tuple(items)
        if not self.items:
            raise ValueError("menu must contain at least one item")
        ids = [item.item_id for item in self.items]
        if any(not isinstance(value, str) or not value.strip() for value in ids):
            raise ValueError("menu item IDs must be non-empty strings")
        if len(set(ids)) != len(ids):
            raise ValueError("menu item IDs must be unique")
        if any(not isinstance(item.label, str) or not item.label.strip() for item in self.items):
            raise ValueError("menu item labels must be non-empty strings")
        if any(not isinstance(item.enabled, bool) for item in self.items):
            raise ValueError("menu item enabled state must be boolean")

        self._focus = self._first_enabled()
        self._contact_item: str | None = None
        self._contact_cancelled = False
        self._rects: dict[str, Rect] = {}

    def _first_enabled(self) -> int | None:
        return next((i for i, item in enumerate(self.items) if item.enabled), None)

    @property
    def focused_item(self) -> str | None:
        if self._focus is None:
            return None
        return self.items[self._focus].item_id

    @property
    def has_enabled_items(self) -> bool:
        return any(item.enabled for item in self.items)

    def set_hit_regions(self, regions: dict[str, Rect]) -> None:
        known = {item.item_id for item in self.items}
        if set(regions) - known:
            raise ValueError("hit regions contain an unknown menu item")
        if any(not isinstance(rect, Rect) for rect in regions.values()):
            raise ValueError("hit regions must contain Rect values")
        self._rects = dict(regions)

    def _enabled_indices(self) -> list[int]:
        return [i for i, item in enumerate(self.items) if item.enabled]

    def navigate(self, direction: str) -> str | None:
        enabled = self._enabled_indices()
        if not enabled:
            self._focus = None
            return None
        if direction not in {"previous", "next"}:
            raise ValueError("direction must be previous or next")
        if self._focus not in enabled:
            self._focus = enabled[0]
        else:
            offset = enabled.index(self._focus)
            step = -1 if direction == "previous" else 1
            self._focus = enabled[(offset + step) % len(enabled)]
        return self.focused_item

    def activate_focused(self) -> SelectionIntent | None:
        if self._focus is None:
            return None
        item = self.items[self._focus]
        return SelectionIntent(item.item_id) if item.enabled else None

    def touch_down(self, x: int, y: int) -> None:
        self._contact_item = None
        self._contact_cancelled = False
        for item in self.items:
            region = self._rects.get(item.item_id)
            if item.enabled and region is not None and region.contains(x, y):
                self._contact_item = item.item_id
                self._focus = self.items.index(item)
                break

    def touch_move(self, x: int, y: int) -> None:
        if self._contact_item is None or self._contact_cancelled:
            return
        region = self._rects.get(self._contact_item)
        if region is None or not region.contains(x, y):
            self._contact_cancelled = True

    def touch_cancel(self) -> None:
        self._contact_item = None
        self._contact_cancelled = False

    def touch_up(self, x: int, y: int) -> SelectionIntent | None:
        item_id = self._contact_item
        cancelled = self._contact_cancelled
        self._contact_item = None
        self._contact_cancelled = False
        if item_id is None or cancelled:
            return None
        region = self._rects.get(item_id)
        if region is None or not region.contains(x, y):
            return None
        return SelectionIntent(item_id)
