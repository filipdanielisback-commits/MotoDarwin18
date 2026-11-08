#!/usr/bin/env python3
"""Validate MotoDarwin18's research-only platform inventory.

This tool is intentionally offline and read-only. It does not probe devices,
download files, or generate hardware initialization data.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ALLOWED_STATUSES = {"confirmed", "probable", "reported", "unknown"}
ALLOWED_SCOPES = {"exact_model", "platform", "community_family", "secondary"}
REQUIRED_COMPONENTS = {
    "memory",
    "interrupt_controller",
    "timers",
    "storage",
    "display",
    "wireless",
    "power_management",
}


def _is_https_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_inventory(data: Any) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) without changing the supplied data."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["top-level JSON value must be an object"], warnings

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    device = data.get("device")
    if not isinstance(device, dict):
        errors.append("device must be an object")
    else:
        for field in ("manufacturer", "product", "model", "soc"):
            if not isinstance(device.get(field), str) or not device[field].strip():
                errors.append(f"device.{field} must be a non-empty string")
        if device.get("model") != "XT2135-2":
            errors.append("device.model must be the exact project target XT2135-2")

    components = data.get("components")
    if not isinstance(components, list):
        errors.append("components must be an array")
        return errors, warnings

    seen: set[str] = set()
    for index, component in enumerate(components):
        prefix = f"components[{index}]"
        if not isinstance(component, dict):
            errors.append(f"{prefix} must be an object")
            continue

        component_id = component.get("id")
        if not isinstance(component_id, str) or not component_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
            component_id = f"index-{index}"
        elif component_id in seen:
            errors.append(f"duplicate component id: {component_id}")
        seen.add(component_id)

        status = component.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(ALLOWED_STATUSES)}")
            continue

        value = component.get("value")
        evidence = component.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{prefix}.evidence must be an array")
            evidence = []

        if status == "unknown":
            if value is not None:
                errors.append(f"{prefix}: unknown status requires value=null")
            warnings.append(f"{component_id}: status is unknown")
        else:
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}: non-unknown status requires a descriptive value")
            if not evidence:
                errors.append(f"{prefix}: non-unknown status requires at least one evidence item")

        has_exact_model_evidence = False
        for evidence_index, item in enumerate(evidence):
            eprefix = f"{prefix}.evidence[{evidence_index}]"
            if not isinstance(item, dict):
                errors.append(f"{eprefix} must be an object")
                continue
            scope = item.get("scope")
            if scope not in ALLOWED_SCOPES:
                errors.append(f"{eprefix}.scope must be one of {sorted(ALLOWED_SCOPES)}")
            if scope == "exact_model":
                has_exact_model_evidence = True
            if not isinstance(item.get("title"), str) or not item["title"].strip():
                errors.append(f"{eprefix}.title must be a non-empty string")
            if not _is_https_url(item.get("url")):
                errors.append(f"{eprefix}.url must be an HTTPS URL")

        if status == "confirmed" and not has_exact_model_evidence:
            errors.append(
                f"{prefix}: confirmed status requires exact_model evidence; "
                "family or SoC evidence is insufficient"
            )
        if status == "probable" and not has_exact_model_evidence:
            warnings.append(
                f"{component_id}: probable status relies on non-exact-model evidence"
            )

    missing = REQUIRED_COMPONENTS - seen
    for component_id in sorted(missing):
        errors.append(f"required component missing: {component_id}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check MotoDarwin18's research-only hardware inventory."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("platform/xt2135-2.json"),
        help="path to the platform inventory JSON",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERROR: cannot read {args.input}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return 2

    errors, warnings = validate_inventory(data)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(
        "OK: inventory structure and evidence rules passed "
        f"({len(data['components'])} components, {len(warnings)} warning(s))."
    )
    print("NOTE: this validates documentation only; it does not validate hardware.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
