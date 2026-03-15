#!/usr/bin/env python3
"""
Work artifact validation for Agentic Enterprise framework.

Validates decision records, governance exceptions, retrospectives,
and technical designs have required sections and fields.

Also validates **work continuity** — ensuring every work item is either
in a terminal state, clearly waiting for a human decision, or picked up
by the next agent cycle.  Nothing should silently stall.

Extends validate_schema.py coverage (which handles signals, missions, releases).

Closes #113.

Usage:
  python3 scripts/validate_work_artifacts.py [--root <path>]

  --root <path>   Validate against an alternate root directory
                  (e.g., examples/e2e-loop) instead of the repo root.
                  The directory must contain a work/ subdirectory.

Exit codes:
  0  All validations passed
  1  One or more validation failures
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent.resolve()


# ── Helpers ──────────────────────────────────────────────────────────────────

def is_template(path: Path) -> bool:
    return "_TEMPLATE" in path.name


def get_sections(text: str) -> set[str]:
    """Return set of second-level heading titles (## ...)."""
    return {m.group(1).strip() for m in re.finditer(r"^##\s+(.+)", text, re.MULTILINE)}


def has_field(text: str, field_name: str) -> bool:
    """Check if a bold field exists in text."""
    return bool(re.search(rf"\*\*{re.escape(field_name)}[:\*]", text))


def validate_file(
    path: Path,
    required_sections: list[str],
    required_fields: list[str],
    artifact_type: str,
    root: Path | None = None,
) -> list[str]:
    """Validate a single work artifact file."""
    errors: list[str] = []
    base = root or REPO
    rel = str(path.relative_to(base))

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{rel}: cannot read — {exc}"]

    sections = get_sections(text)

    for section in required_sections:
        # Flexible match: section name may appear as substring
        found = any(section.lower() in s.lower() for s in sections)
        if not found:
            errors.append(f"{rel}: missing required section '## {section}' ({artifact_type})")

    for field in required_fields:
        if not has_field(text, field):
            errors.append(f"{rel}: missing required field '**{field}**' ({artifact_type})")

    return errors


# ── Artifact type definitions ────────────────────────────────────────────────

DECISION_RECORD = {
    "glob": "work/decisions/*.md",
    "type": "decision record",
    "required_sections": ["Context", "Decision", "Alternatives Considered", "Consequences"],
    "required_fields": ["Decision ID", "Status"],
}

GOVERNANCE_EXCEPTION = {
    "glob": "work/decisions/EXC-*.md",
    "type": "governance exception",
    "required_sections": ["Summary", "Details"],
    "required_fields": ["Exception ID", "Risk", "Mitigation"],
}

RETROSPECTIVE = {
    "glob": "work/retrospectives/*.md",
    "type": "retrospective/postmortem",
    "required_sections": ["Timeline", "Root Cause", "Follow-Up"],
    "required_fields": ["Incident ID", "Severity", "Status"],
}

TECHNICAL_DESIGN = {
    "glob": "work/missions/*/technical-design.md",
    "type": "technical design",
    "required_sections": ["Context", "Observability Design", "Architecture Decisions"],
    "required_fields": ["Mission ID", "Status"],
}

# Also check for Observability Design in any file named *technical-design*
TECHNICAL_DESIGN_ALT = {
    "glob": "work/missions/**/technical-design*.md",
    "type": "technical design",
    "required_sections": ["Observability Design"],
    "required_fields": [],
}


# ── Discovery ────────────────────────────────────────────────────────────────

def discover_artifacts(base_dir: Path, glob_pattern: str) -> list[Path]:
    """Find non-template, non-README markdown files matching pattern."""
    return [
        p for p in base_dir.glob(glob_pattern)
        if p.is_file()
        and not is_template(p)
        and p.name != "README.md"
    ]


# ── Work continuity helpers ──────────────────────────────────────────────────


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _extract_status(text: str) -> str | None:
    """Extract **Status:** value from markdown metadata."""
    m = re.search(r"\*\*Status:\*\*\s*(\S+)", text)
    return m.group(1).strip().lower() if m else None


def _signal_has_proceed(text: str) -> bool:
    """Return True if the signal has 'Proceed to opportunity validation' checked."""
    return bool(re.search(r"\[x\]\s*Proceed to opportunity validation", text, re.IGNORECASE))


def _signal_has_any_disposition(text: str) -> bool:
    """Return True if at least one disposition checkbox is checked."""
    return bool(re.search(r"\[x\]", text))


def _extract_retro_signal_refs(text: str) -> list[str]:
    """Extract signal file paths referenced in Signals Filed section."""
    refs: list[str] = []
    in_section = False
    for line in text.splitlines():
        if re.match(r"^##\s+Signals Filed", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+", line):
            break
        if in_section:
            # Match backtick-wrapped paths like `work/signals/foo.md`
            for m in re.finditer(r"`(work/signals/[^`]+\.md)`", line):
                refs.append(m.group(1))
    return refs


def validate_work_continuity(root: Path) -> list[str]:
    """Validate that all non-terminal work items are picked up or in human-to-decide state.

    Checks:
    1. Every signal has a disposition (no undecided signals).
    2. Signals with 'Proceed' are referenced by at least one mission brief.
    3. Signals filed in retrospectives exist as actual files.
    4. Active missions have STATUS.md for progress tracking.
    """
    errors: list[str] = []

    signals_dir = root / "work" / "signals"
    missions_dir = root / "work" / "missions"
    retros_dir = root / "work" / "retrospectives"

    # ── Collect all signal files and their dispositions ────────────────────
    signal_files: dict[str, str] = {}  # filename -> text
    if signals_dir.exists():
        for p in signals_dir.glob("*.md"):
            if p.name == "README.md" or "_TEMPLATE" in p.name:
                continue
            text = _read_text(p)
            if text:
                signal_files[p.name] = text

    # ── Collect all mission briefs and what signals they reference ─────────
    mission_texts: dict[str, str] = {}  # relative path -> text
    if missions_dir.exists():
        for p in missions_dir.rglob("BRIEF.md"):
            if "_TEMPLATE" in str(p):
                continue
            text = _read_text(p)
            if text:
                mission_texts[str(p.relative_to(root))] = text
        for p in missions_dir.rglob("mission-brief.md"):
            if "_TEMPLATE" in str(p):
                continue
            text = _read_text(p)
            if text:
                mission_texts[str(p.relative_to(root))] = text

    # Build set of signal filenames referenced by any mission
    referenced_signals: set[str] = set()
    for mtext in mission_texts.values():
        for m in re.finditer(r"(work/signals/)?(\d{4}-\d{2}-\d{2}-[^\s`)]+\.md)", mtext):
            referenced_signals.add(m.group(2))

    # ── Check 1: Every signal must have a checked disposition ─────────────
    for fname, text in signal_files.items():
        if not _signal_has_any_disposition(text):
            errors.append(
                f"work/signals/{fname}: no disposition checked — signal has no clear "
                f"next action (stalled). Must check one of: Proceed / Defer / Monitor / Archive"
            )

    # ── Check 2: Proceed signals must be referenced by a mission ──────────
    for fname, text in signal_files.items():
        if _signal_has_proceed(text) and fname not in referenced_signals:
            errors.append(
                f"work/signals/{fname}: disposition is 'Proceed to opportunity validation' "
                f"but no mission brief references this signal — work fell through the cracks"
            )

    # ── Check 3: Retro-filed signals must exist ───────────────────────────
    if retros_dir.exists():
        for p in retros_dir.glob("*.md"):
            if p.name == "README.md" or "_TEMPLATE" in p.name:
                continue
            text = _read_text(p)
            if not text:
                continue
            rel_retro = str(p.relative_to(root))
            for signal_path in _extract_retro_signal_refs(text):
                full_path = root / signal_path
                if not full_path.exists():
                    errors.append(
                        f"{rel_retro}: references signal '{signal_path}' in "
                        f"Signals Filed section but the file does not exist — "
                        f"consequential work was not created"
                    )

    # ── Check 4: Active missions must have STATUS.md ──────────────────────
    for mpath, mtext in mission_texts.items():
        status = _extract_status(mtext)
        if status == "active":
            mission_dir = (root / mpath).parent
            status_file = mission_dir / "STATUS.md"
            if not status_file.exists():
                errors.append(
                    f"{mpath}: mission is 'active' but has no STATUS.md — "
                    f"no progress tracking means work may be stalled"
                )

    return errors


# ── Main ─────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate work artifact structure")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Alternate root directory containing a work/ subdirectory (e.g., examples/e2e-loop)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve() if args.root else REPO

    if not (root / "work").exists():
        print(f"ERROR: No work/ directory found in {root}")
        return 1

    all_errors: list[str] = []
    all_ok: list[str] = []

    artifact_configs = [
        ("Decision records", "work/decisions/*.md", DECISION_RECORD, ["EXC-", "DPA-", "DPIA-", "RISK-"]),
        ("Governance exceptions", "work/decisions/EXC-*.md", GOVERNANCE_EXCEPTION, []),
        ("Retrospectives", "work/retrospectives/*.md", RETROSPECTIVE, []),
    ]

    for label, glob_pattern, config, exclude_prefixes in artifact_configs:
        files = discover_artifacts(root, glob_pattern)

        # For decision records, exclude governance exceptions and other sub-types
        if exclude_prefixes:
            files = [
                f for f in files
                if not any(f.name.startswith(prefix) for prefix in exclude_prefixes)
            ]

        if not files:
            print(f"INFO: No {label.lower()} found — skipping.")
            continue

        print(f"Validating {label}...")
        for f in files:
            errors = validate_file(
                f,
                config["required_sections"],
                config["required_fields"],
                config["type"],
                root=root,
            )
            rel = str(f.relative_to(root))
            if errors:
                all_errors.extend(errors)
            else:
                all_ok.append(rel)
                print(f"  ✓  {rel}")

    # Technical designs (search recursively under work/missions/ only)
    missions_dir = root / "work" / "missions"
    all_tech = []
    if missions_dir.exists():
        all_tech = [
            p for p in missions_dir.rglob("technical-design*.md")
            if p.is_file() and not is_template(p)
        ]

    if all_tech:
        print("Validating technical designs...")
        for f in all_tech:
            errors = validate_file(
                f,
                TECHNICAL_DESIGN["required_sections"],
                TECHNICAL_DESIGN["required_fields"],
                TECHNICAL_DESIGN["type"],
                root=root,
            )
            rel = str(f.relative_to(root))
            if errors:
                all_errors.extend(errors)
            else:
                all_ok.append(rel)
                print(f"  ✓  {rel}")
    else:
        print("INFO: No technical designs found — skipping.")

    # ── Template structure validation ─────────────────────────────────────
    # Validate that templates themselves have required sections
    # (ensures new instances will be guided correctly)
    # Skipped when using --root (templates live in the main repo root)
    if root == REPO:
        print("Validating work artifact templates...")
        template_checks = [
            (
                REPO / "work" / "decisions" / "_TEMPLATE-decision-record.md",
                DECISION_RECORD,
            ),
            (
                REPO / "work" / "decisions" / "_TEMPLATE-governance-exception.md",
                GOVERNANCE_EXCEPTION,
            ),
            (
                REPO / "work" / "retrospectives" / "_TEMPLATE-postmortem.md",
                RETROSPECTIVE,
            ),
            (
                REPO / "work" / "missions" / "_TEMPLATE-technical-design.md",
                TECHNICAL_DESIGN,
            ),
        ]

        for template_path, config in template_checks:
            if not template_path.exists():
                print(f"  ⚠  Template not found: {template_path.relative_to(REPO)}")
                continue

            errors = validate_file(
                template_path,
                config["required_sections"],
                config["required_fields"],
                f"{config['type']} template",
            )
            rel = str(template_path.relative_to(REPO))
            if errors:
                all_errors.extend(errors)
            else:
                all_ok.append(rel)
                print(f"  ✓  {rel}")

    # ── Work continuity validation ────────────────────────────────────────
    print("Validating work continuity (stalled work detection)...")
    continuity_errors = validate_work_continuity(root)
    if continuity_errors:
        all_errors.extend(continuity_errors)
    else:
        print("  ✓  All work items have clear next-actor or are in terminal state")

    # ── Report ────────────────────────────────────────────────────────────
    if all_errors:
        print(f"\n{len(all_errors)} work artifact error(s):")
        for err in all_errors:
            print(f"  ✗  {err}")
        return 1

    total = len(all_ok)
    print(f"\nWork artifact validation passed ({total} artifact(s) checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
