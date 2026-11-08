#!/usr/bin/env python3
"""Validate descriptive XNULoader platform-service metadata and pure touch events.

This module is host-only. It does not discover firmware protocols or access hardware.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_MANIFEST = Path("xnuloader/platform-services.example.json")
MAX_FILE_BYTES = 262_144
STATUSES = {"available", "unavailable", "error", "not_checked", "unknown"}
EVIDENCE_SCOPES = {"upstream", "soc_family", "device_family", "exact_model"}


class ValidationError(Exception):
    """Raised when descriptive platform-service metadata is invalid."""


def _object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    return value


def _keys(value: dict[str, Any], expected: set[str], where: str) -> None:
    missing = sorted(expected - value.keys())
    extra = sorted(value.keys() - expected)
    if missing:
        raise ValidationError(f"{where} missing keys: {', '.join(missing)}")
    if extra:
        raise ValidationError(f"{where} unexpected keys: {', '.join(extra)}")


def _text(value: Any, where: str, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{where} must be a non-empty string" + (" or null" if nullable else ""))


def _evidence(value: Any, where: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValidationError(f"{where} must be an array")
    result = []
    for index, entry in enumerate(value):
        label = f"{where}[{index}]"
        item = _object(entry, label)
        _keys(item, {"claim", "scope", "url"}, label)
        _text(item["claim"], f"{label}.claim")
        scope = item["scope"]
        if scope not in EVIDENCE_SCOPES:
            raise ValidationError(f"{label}.scope is not recognized")
        url = item["url"]
        _text(url, f"{label}.url")
        if not url.startswith("https://"):
            raise ValidationError(f"{label}.url must use HTTPS")
        result.append(item)
    return result


def _status(value: Any, where: str) -> str:
    _text(value, where)
    if value not in STATUSES:
        raise ValidationError(f"{where} is not recognized")
    return value


def _validate_display(value: Any) -> None:
    item = _object(value, "display")
    _keys(item, {"protocol", "status", "mode", "evidence"}, "display")
    if item["protocol"] != "UEFI Graphics Output Protocol":
        raise ValidationError("display.protocol must name UEFI Graphics Output Protocol")
    status = _status(item["status"], "display.status")
    evidence = _evidence(item["evidence"], "display.evidence")
    mode = item["mode"]

    if status == "available":
        if not any(entry["scope"] == "exact_model" for entry in evidence):
            raise ValidationError("available display requires exact_model evidence")
        mode = _object(mode, "display.mode")
        _keys(mode, {"width", "height", "pixel_format", "pixels_per_scan_line"}, "display.mode")
        for key in ("width", "height", "pixels_per_scan_line"):
            number = mode[key]
            if isinstance(number, bool) or not isinstance(number, int) or number <= 0:
                raise ValidationError(f"display.mode.{key} must be a positive integer")
        if mode["pixels_per_scan_line"] < mode["width"]:
            raise ValidationError("display stride cannot be smaller than display width")
        _text(mode["pixel_format"], "display.mode.pixel_format")
    elif mode is not None:
        raise ValidationError("display.mode must be null unless display.status is available")


def _validate_touch(value: Any) -> None:
    item = _object(value, "touch")
    _keys(item, {"protocol", "status", "coordinate_range", "evidence"}, "touch")
    if item["protocol"] != "UEFI Absolute Pointer Protocol":
        raise ValidationError("touch.protocol must name UEFI Absolute Pointer Protocol")
    status = _status(item["status"], "touch.status")
    evidence = _evidence(item["evidence"], "touch.evidence")
    coord = item["coordinate_range"]

    if status == "available":
        if not any(entry["scope"] == "exact_model" for entry in evidence):
            raise ValidationError("available touch requires exact_model evidence")
        coord = _object(coord, "touch.coordinate_range")
        _keys(coord, {"min_x", "max_x", "min_y", "max_y"}, "touch.coordinate_range")
        for key, number in coord.items():
            if isinstance(number, bool) or not isinstance(number, int):
                raise ValidationError(f"touch.coordinate_range.{key} must be an integer")
        if coord["min_x"] >= coord["max_x"] or coord["min_y"] >= coord["max_y"]:
            raise ValidationError("touch coordinate ranges must have min less than max")
    elif coord is not None:
        raise ValidationError("touch.coordinate_range must be null unless touch.status is available")


def _validate_fallback(value: Any) -> None:
    item = _object(value, "fallback_pointer")
    _keys(item, {"protocol", "status", "evidence"}, "fallback_pointer")
    _text(item["protocol"], "fallback_pointer.protocol", nullable=True)
    _status(item["status"], "fallback_pointer.status")
    _evidence(item["evidence"], "fallback_pointer.evidence")
    if item["status"] == "available" and item["protocol"] is None:
        raise ValidationError("available fallback pointer requires a protocol name")


def validate_manifest(data: Any) -> None:
    item = _object(data, "manifest")
    _keys(item, {"schema_version", "target", "environment", "display", "touch", "fallback_pointer"}, "manifest")
    if item["schema_version"] != "1.0":
        raise ValidationError("schema_version must be '1.0'")

    target = _object(item["target"], "target")
    _keys(target, {"model", "identity_status"}, "target")
    if target["model"] != "XT2135-2":
        raise ValidationError("target.model must be XT2135-2")
    if target["identity_status"] not in {"unknown", "documented", "confirmed"}:
        raise ValidationError("target.identity_status is not recognized")

    environment = _object(item["environment"], "environment")
    _keys(environment, {"name", "status"}, "environment")
    _text(environment["name"], "environment.name", nullable=True)
    if environment["status"] not in {"unknown", "identified"}:
        raise ValidationError("environment.status must be unknown or identified")
    if environment["status"] == "identified" and environment["name"] is None:
        raise ValidationError("identified environment requires a name")

    _validate_display(item["display"])
    _validate_touch(item["touch"])
    _validate_fallback(item["fallback_pointer"])


def load_manifest(path: Path) -> Any:
    raw = path.read_bytes()
    if len(raw) > MAX_FILE_BYTES:
        raise ValidationError(f"manifest exceeds {MAX_FILE_BYTES} byte size limit")
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid UTF-8 JSON: {exc}") from exc


@dataclass(frozen=True)
class TouchSample:
    """Synthetic sample used by host tests; not a hardware input structure."""

    contact: bool
    x: int | None = None
    y: int | None = None
    failed: bool = False


@dataclass(frozen=True)
class TouchEvent:
    kind: str
    x: int | None = None
    y: int | None = None


class TouchEventModel:
    """Convert validated synthetic absolute-pointer samples into UI-level events."""

    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int):
        if min_x >= max_x or min_y >= max_y:
            raise ValueError("coordinate ranges must have min less than max")
        self.min_x, self.max_x = min_x, max_x
        self.min_y, self.max_y = min_y, max_y
        self._active = False
        self._last: tuple[int, int] | None = None

    def _valid_point(self, x: Any, y: Any) -> bool:
        return (
            isinstance(x, int) and not isinstance(x, bool)
            and isinstance(y, int) and not isinstance(y, bool)
            and self.min_x <= x <= self.max_x
            and self.min_y <= y <= self.max_y
        )

    def process(self, sample: TouchSample) -> TouchEvent | None:
        if sample.failed:
            if self._active and self._last is not None:
                x, y = self._last
                self._active = False
                self._last = None
                return TouchEvent("cancel", x, y)
            return None

        if sample.contact:
            if not self._valid_point(sample.x, sample.y):
                if self._active and self._last is not None:
                    x, y = self._last
                    self._active = False
                    self._last = None
                    return TouchEvent("cancel", x, y)
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


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print("Usage: python tools/validate_platform_services.py [manifest.json]", file=sys.stderr)
        return 1
    path = Path(args[0]) if args else DEFAULT_MANIFEST
    try:
        validate_manifest(load_manifest(path))
    except (OSError, ValidationError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"VALID: {path} (metadata only; no firmware or hardware was accessed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
