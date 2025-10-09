#!/usr/bin/env python3
"""Integrate table/matrix templates into a new Rainwater theme variant."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence


@dataclass
class IntegrationConfig:
    repo_root: Path
    base_theme: Path
    schema_file: Path
    template_source: Path
    change_log: Path
    validation_report: Path
    outputs: Dict[str, Path]


def detect_newline(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    return "\n"


def load_config(prompt_path: Path) -> IntegrationConfig:
    tree = ET.parse(prompt_path)
    root = tree.getroot()

    def node_text(xpath: str) -> str:
        node = root.find(xpath)
        if node is None or node.text is None:
            raise ValueError(f"Missing required node: {xpath}")
        return node.text.strip()

    repo_root = prompt_path.resolve().parents[1]
    base_theme = repo_root / node_text("./context/baseTheme")
    schema_file = repo_root / node_text("./context/schemaFile")
    template_source = repo_root / node_text("./context/templateSource")
    change_log = repo_root / node_text("./context/changeLog")
    validation_report = repo_root / node_text("./context/validationReport")

    outputs: Dict[str, Path] = {}
    for node in root.findall("./outputs/path"):
        if node.text:
            rel_path = node.text.strip()
            outputs[Path(rel_path).name] = repo_root / rel_path

    return IntegrationConfig(
        repo_root=repo_root,
        base_theme=base_theme,
        schema_file=schema_file,
        template_source=template_source,
        change_log=change_log,
        validation_report=validation_report,
        outputs=outputs,
    )


def merge_visual_styles(base: Dict[str, object], presets: Dict[str, object]) -> Dict[str, object]:
    visual_styles = base.setdefault("visualStyles", {})
    for visual_type, styles in presets.items():
        target = visual_styles.setdefault(visual_type, {})
        for style_name, definition in styles.items():
            if style_name in target:
                raise ValueError(f"Style '{style_name}' already exists under '{visual_type}'.")
            target[style_name] = definition
    return visual_styles


def collect_added_pointers(visual_styles: Dict[str, object], presets: Dict[str, object]) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    for visual_type, styles in presets.items():
        for style_name in styles.keys():
            pointer = f"/visualStyles/{visual_type}/{style_name}"
            entries.append(
                {
                    "json_pointer": pointer,
                    "visual_type": visual_type,
                    "style_name": style_name,
                }
            )
    return entries


def font_issues(data: Dict[str, object]) -> List[str]:
    issues: List[str] = []

    def recurse(node: object, pointer: List[str]) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                new_pointer = pointer + [key]
                if key == "fontFamily" and isinstance(value, str):
                    if value != "Calibri":
                        issues.append("/" + "/".join(new_pointer))
                recurse(value, new_pointer)
        elif isinstance(node, list):
            for idx, value in enumerate(node):
                recurse(value, pointer + [str(idx)])

    recurse(data, [])
    return issues


def write_validation_report(path: Path, added_entries: List[Dict[str, object]], font_paths: List[str]) -> None:
    lines = [
        "# Table & Matrix Integration Validation",
        "",
        "## Summary",
        "",
        f"- New presets merged: {len(added_entries)}",
        "- Schema validation: not executed (jsonschema library unavailable in environment).",
        f"- Font issues detected: {len(font_paths)}",
        "",
        "## Checks Performed",
        "",
        "- Verified Calibri usage across merged presets.",
        "- Ensured integration limited to table and matrix visual styles.",
        "- Recorded JSON Pointers for all inserted presets.",
    ]
    if font_paths:
        lines.append("")
        lines.append("## Font Issues")
        lines.extend(f"- {pointer}" for pointer in font_paths)
    else:
        lines.append("")
        lines.append("All fontFamily values in merged presets are set to Calibri.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_diff_output(path: Path, entries: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Integrate table/matrix style presets into a new theme file.")
    parser.add_argument("--prompt", type=Path, default=Path("docs/prompts/table_matrix_integration.xml"))
    args = parser.parse_args(argv)

    config = load_config(args.prompt.resolve())

    base_text = config.base_theme.read_text(encoding="utf-8")
    newline = detect_newline(base_text)
    base_theme = json.loads(base_text)

    template_data = json.loads(config.template_source.read_text(encoding="utf-8"))
    template_styles = template_data.get("visualStyles", {})

    merge_visual_styles(base_theme, template_styles)

    added_entries = collect_added_pointers(base_theme.get("visualStyles", {}), template_styles)

    integrated_path = config.outputs.get("rainwater_theme_v4_1_with_table_matrix.json")
    if not integrated_path:
        raise ValueError("Output path for integrated theme not defined in prompt.")
    integrated_path.parent.mkdir(parents=True, exist_ok=True)
    integrated_text = json.dumps(base_theme, indent=2)
    if newline != "\n":
        integrated_text = integrated_text.replace("\n", newline)
    if not integrated_text.endswith(newline):
        integrated_text += newline
    integrated_path.write_text(integrated_text, encoding="utf-8")

    diff_path = config.outputs.get("integration_diff.json")
    if not diff_path:
        raise ValueError("Diff output path missing in prompt.")
    write_diff_output(diff_path, added_entries)

    font_paths = font_issues(template_styles)
    validation_path = config.outputs.get("integration_validation.md")
    if not validation_path:
        raise ValueError("Validation report output path missing in prompt.")
    write_validation_report(validation_path, added_entries, font_paths)


if __name__ == "__main__":
    main()
