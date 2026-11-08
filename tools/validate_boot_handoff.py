#!/usr/bin/env python3
"""Validate descriptive boot-handoff research manifests; never talks to a device."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_MANIFEST = Path("boot-handoff/manifest.example.json")
MAX_FILE_BYTES = 1_048_576
U64_MAX = (1 << 64) - 1
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
EVIDENCE_SCOPES = {"upstream", "soc_family", "device_family", "exact_model"}
EVIDENCE_STATUSES = {"unknown", "candidate", "documented", "confirmed"}


class ValidationError(Exception):
    """Raised when a manifest is structurally invalid."""


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValidationError(f"non-standard JSON numeric constant: {value}")


def _require_object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    return value


def _require_keys(obj: dict[str, Any], keys: set[str], where: str) -> None:
    missing = sorted(keys - obj.keys())
    extra = sorted(obj.keys() - keys)
    if missing:
        raise ValidationError(f"{where} missing keys: {', '.join(missing)}")
    if extra:
        raise ValidationError(f"{where} has unexpected keys: {', '.join(extra)}")


def _require_text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{where} must be a non-empty string")
    return value


def _optional_u64(value: Any, where: str) -> None:
    if value is None:
        return
    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{where} must be an integer or null")
    if not 0 <= value <= U64_MAX:
        raise ValidationError(f"{where} must be within unsigned 64-bit range")


def _validate_evidence(items: Any, where: str) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise ValidationError(f"{where} must be an array")
    normalized = []
    for index, item in enumerate(items):
        label = f"{where}[{index}]"
        obj = _require_object(item, label)
        _require_keys(obj, {"claim", "status", "scope", "url"}, label)
        _require_text(obj["claim"], f"{label}.claim")
        status = _require_text(obj["status"], f"{label}.status")
        scope = _require_text(obj["scope"], f"{label}.scope")
        url = _require_text(obj["url"], f"{label}.url")
        if status not in EVIDENCE_STATUSES:
            raise ValidationError(f"{label}.status is not recognized")
        if scope not in EVIDENCE_SCOPES:
            raise ValidationError(f"{label}.scope is not recognized")
        if not url.startswith("https://"):
            raise ValidationError(f"{label}.url must use HTTPS")
        normalized.append(obj)
    return normalized


def _validate_device_tree(value: Any) -> None:
    obj = _require_object(value, "device_tree")
    _require_keys(obj, {"status", "format", "length", "sha256", "evidence"}, "device_tree")
    status = _require_text(obj["status"], "device_tree.status")
    if status not in {"unknown", "described"}:
        raise ValidationError("device_tree.status must be 'unknown' or 'described'")
    _validate_evidence(obj["evidence"], "device_tree.evidence")

    if status == "unknown":
        if any(obj[key] is not None for key in ("format", "length", "sha256")):
            raise ValidationError("unknown device_tree must have null format, length, and sha256")
        return

    if obj["format"] != "dtb":
        raise ValidationError("described device_tree.format must be 'dtb'")
    length = obj["length"]
    if isinstance(length, bool) or not isinstance(length, int) or length <= 0:
        raise ValidationError("described device_tree.length must be a positive integer")
    digest = obj["sha256"]
    if not isinstance(digest, str) or not HEX_SHA256.fullmatch(digest):
        raise ValidationError("described device_tree.sha256 must be 64 lowercase hexadecimal characters")
    if not obj["evidence"]:
        raise ValidationError("described device_tree requires at least one evidence item")


def _validate_memory_regions(value: Any) -> None:
    if not isinstance(value, list):
        raise ValidationError("memory_regions must be an array")

    ranges: list[tuple[int, int, str]] = []
    names: set[str] = set()
    for index, item in enumerate(value):
        where = f"memory_regions[{index}]"
        obj = _require_object(item, where)
        _require_keys(obj, {"name", "base", "size", "alignment", "status", "evidence"}, where)
        name = _require_text(obj["name"], f"{where}.name")
        if name in names:
            raise ValidationError(f"duplicate memory region name: {name}")
        names.add(name)

        base, size, alignment = obj["base"], obj["size"], obj["alignment"]
        for field, number in (("base", base), ("size", size), ("alignment", alignment)):
            if isinstance(number, bool) or not isinstance(number, int):
                raise ValidationError(f"{where}.{field} must be an integer")
        if not 0 <= base <= U64_MAX:
            raise ValidationError(f"{where}.base is outside unsigned 64-bit range")
        if not 0 < size <= U64_MAX:
            raise ValidationError(f"{where}.size must be positive and within unsigned 64-bit range")
        if not 0 < alignment <= U64_MAX or alignment & (alignment - 1):
            raise ValidationError(f"{where}.alignment must be a positive power of two")
        if base % alignment:
            raise ValidationError(f"{where}.base is not aligned to {alignment}")
        end = base + size
        if end > U64_MAX + 1:
            raise ValidationError(f"{where} range overflows unsigned 64-bit address space")

        status = _require_text(obj["status"], f"{where}.status")
        if status not in EVIDENCE_STATUSES - {"unknown"}:
            raise ValidationError(f"{where}.status is not a supported known-value status")
        evidence = _validate_evidence(obj["evidence"], f"{where}.evidence")
        if not evidence:
            raise ValidationError(f"{where} requires evidence")
        if status == "confirmed" and not any(e["scope"] == "exact_model" for e in evidence):
            raise ValidationError(f"{where} cannot be confirmed using family-level evidence")

        ranges.append((base, end, name))

    ranges.sort()
    for previous, current in zip(ranges, ranges[1:]):
        if current[0] < previous[1]:
            raise ValidationError(
                f"memory regions overlap: {previous[2]} and {current[2]}"
            )


def validate_manifest(data: Any) -> None:
    obj = _require_object(data, "manifest")
    _require_keys(
        obj,
        {"manifest_version", "target", "boot_handoff", "device_tree", "memory_regions", "evidence"},
        "manifest",
    )
    if _require_text(obj["manifest_version"], "manifest_version") != "1.0":
        raise ValidationError("manifest_version must be '1.0'")

    target = _require_object(obj["target"], "target")
    _require_keys(target, {"model", "codename", "identity_status"}, "target")
    if target["model"] != "XT2135-2":
        raise ValidationError("target.model must be XT2135-2")
    _require_text(target["codename"], "target.codename")
    identity_status = _require_text(target["identity_status"], "target.identity_status")
    if identity_status not in {"unknown", "documented", "confirmed"}:
        raise ValidationError("target.identity_status is not recognized")

    handoff = _require_object(obj["boot_handoff"], "boot_handoff")
    handoff_keys = {
        "revision", "version", "phys_base", "virt_base", "mem_size", "top_of_kernel_data"
    }
    _require_keys(handoff, handoff_keys, "boot_handoff")
    for key, value in handoff.items():
        _optional_u64(value, f"boot_handoff.{key}")

    _validate_device_tree(obj["device_tree"])
    _validate_memory_regions(obj["memory_regions"])
    top_evidence = _validate_evidence(obj["evidence"], "evidence")
    if identity_status == "confirmed" and not any(e["scope"] == "exact_model" for e in top_evidence):
        raise ValidationError("target identity cannot be confirmed using family-level evidence")


def load_manifest(path: Path) -> Any:
    raw = path.read_bytes()
    if len(raw) > MAX_FILE_BYTES:
        raise ValidationError(f"manifest exceeds {MAX_FILE_BYTES} byte size limit")
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid UTF-8 JSON: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print("Usage: python tools/validate_boot_handoff.py [manifest.json]", file=sys.stderr)
        return 1
    path = Path(args[0]) if args else DEFAULT_MANIFEST
    try:
        data = load_manifest(path)
        validate_manifest(data)
    except (OSError, ValidationError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"VALID: {path} (structure only; no hardware compatibility is implied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
