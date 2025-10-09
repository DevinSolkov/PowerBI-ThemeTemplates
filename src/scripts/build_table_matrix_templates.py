#!/usr/bin/env python3
"""Generate table and matrix template outputs with creative naming."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence


def solid(color: str) -> Dict[str, Dict[str, str]]:
    return {"solid": {"color": color}}


def matrix_properties(
    name: str,
    header_bg: str,
    header_font: str,
    value_font: str,
    grid_color: str,
    subtotal_bg: str,
    highlight_font: str,
    background_color: str,
    show_background: bool,
    subtotal_position: str,
    expand_buttons: bool,
    row_header_weight: str,
) -> Dict[str, object]:
    return {
        "*": {
            "stylePreset": [
                {
                    "name": name,
                }
            ],
            "background": [
                {
                    "show": show_background,
                    "transparency": 10 if show_background else 100,
                    "color": solid(background_color),
                }
            ],
            "columnHeaders": [
                {
                    "fontFamily": "Calibri",
                    "fontSize": 13 if name in {"Teal Summit Totals", "Slate Beacon Matrix", "Frosted Harbor Cells"} else 12,
                    "fontColor": solid(header_font),
                    "backColor": solid(header_bg),
                    "alignment": "Center",
                    "titleAlignment": "Center",
                    "wordWrap": True,
                }
            ],
            "rowHeaders": [
                {
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(highlight_font),
                    "outline": row_header_weight,
                    "showExpandCollapseButtons": expand_buttons,
                }
            ],
            "values": [
                {
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(value_font),
                    "wrapText": True,
                }
            ],
            "grid": [
                {
                    "gridHorizontal": True,
                    "gridHorizontalColor": solid(grid_color),
                    "gridVertical": name in {"Maritime Steel Grid", "Frosted Harbor Cells"},
                    "gridVerticalColor": solid(grid_color),
                }
            ],
            "subTotals": [
                {
                    "id": "Row",
                    "applyToHeaders": True,
                    "rowSubtotalsPosition": subtotal_position,
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(highlight_font),
                    "backColor": solid(subtotal_bg),
                },
                {
                    "id": "Column",
                    "applyToHeaders": True,
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(highlight_font),
                    "backColor": solid(subtotal_bg),
                },
            ],
            "totals": [
                {
                    "show": True,
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(highlight_font),
                    "labelColor": solid(highlight_font),
                    "backgroundColor": solid(subtotal_bg),
                }
            ],
        }
    }


def table_properties(
    name: str,
    header_bg: str,
    header_font: str,
    value_font: str,
    grid_color: str,
    background_color: str,
    banding_color: str,
    show_background: bool,
    totals_background: str,
    totals_font: str,
) -> Dict[str, object]:
    return {
        "*": {
            "stylePreset": [
                {
                    "name": name,
                }
            ],
            "background": [
                {
                    "show": show_background,
                    "transparency": 10 if show_background else 100,
                    "color": solid(background_color),
                }
            ],
            "columnHeaders": [
                {
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(header_font),
                    "backColor": solid(header_bg),
                    "alignment": "Center",
                    "wordWrap": True,
                }
            ],
            "values": [
                {
                    "fontFamily": "Calibri",
                    "fontSize": 11,
                    "fontColor": solid(value_font),
                    "backColor": solid(banding_color),
                }
            ],
            "grid": [
                {
                    "gridHorizontal": True,
                    "gridHorizontalColor": solid(grid_color),
                    "gridVertical": False,
                    "gridVerticalColor": solid(grid_color),
                }
            ],
            "total": [
                {
                    "fontFamily": "Calibri",
                    "fontSize": 12,
                    "fontColor": solid(totals_font),
                    "backColor": solid(totals_background),
                    "show": True,
                }
            ],
        }
    }


@dataclass
class TemplateSpec:
    visual_type: str
    style_variant: str
    name: str
    description: str
    features: List[str]
    properties: Dict[str, object]


def build_templates(schema: str) -> Dict[str, object]:
    deep_navy = "#0C2340"
    cobalt = "#005598"
    sky = "#6FB9E1"
    surf = "#BADCED"
    mist = "#F2F2F2"
    pebble = "#D9D9D9"
    charcoal = "#2E2E2E"
    drift = "#E4EEF5"
    sand = "#F7F9FB"

    templates: List[TemplateSpec] = [
        TemplateSpec(
            visual_type="pivotTable",
            style_variant="Style 1",
            name="Maritime Steel Grid",
            description="Structured navy matrix with crisp steel gridlines.",
            features=[
                "Centered navy headers with steel backdrops",
                "Visible horizontal and vertical separators",
                "Balanced row and column subtotals",
            ],
            properties=matrix_properties(
                name="Maritime Steel Grid",
                header_bg=cobalt,
                header_font="#FFFFFF",
                value_font=charcoal,
                grid_color=pebble,
                subtotal_bg=drift,
                highlight_font=deep_navy,
                background_color=sand,
                show_background=True,
                subtotal_position="Top",
                expand_buttons=True,
                row_header_weight="None",
            ),
        ),
        TemplateSpec(
            visual_type="pivotTable",
            style_variant="Style 2",
            name="Muted Horizon Ledger",
            description="Soft blue-gray matrix tailored for financial ledgers.",
            features=[
                "Subdued header band with white lettering",
                "Row headers without expand buttons for clean presentation",
                "Top-position row subtotals for fast scanning",
            ],
            properties=matrix_properties(
                name="Muted Horizon Ledger",
                header_bg=surf,
                header_font=deep_navy,
                value_font=charcoal,
                grid_color=pebble,
                subtotal_bg=mist,
                highlight_font=deep_navy,
                background_color="#FFFFFF",
                show_background=False,
                subtotal_position="Top",
                expand_buttons=False,
                row_header_weight="None",
            ),
        ),
        TemplateSpec(
            visual_type="pivotTable",
            style_variant="Style 3",
            name="Azure Balance Bands",
            description="Banded matrix with alternating azure highlights.",
            features=[
                "Azure headers with centered typography",
                "Horizontal grid only for stripped-down layout",
                "Band-inspired subtotals for both direction groups",
            ],
            properties=matrix_properties(
                name="Azure Balance Bands",
                header_bg=sky,
                header_font=deep_navy,
                value_font=charcoal,
                grid_color=surf,
                subtotal_bg=surf,
                highlight_font=deep_navy,
                background_color=mist,
                show_background=True,
                subtotal_position="Auto",
                expand_buttons=False,
                row_header_weight="None",
            ),
        ),
        TemplateSpec(
            visual_type="pivotTable",
            style_variant="Style 4",
            name="Slate Beacon Matrix",
            description="High-contrast matrix with slate headers and beacon accents.",
            features=[
                "Slate header panel with bright text",
                "Row headers in soft neutral for readability",
                "Totals shaded for executive summaries",
            ],
            properties=matrix_properties(
                name="Slate Beacon Matrix",
                header_bg=charcoal,
                header_font="#FFFFFF",
                value_font=deep_navy,
                grid_color=pebble,
                subtotal_bg=mist,
                highlight_font=deep_navy,
                background_color="#FFFFFF",
                show_background=False,
                subtotal_position="Bottom",
                expand_buttons=True,
                row_header_weight="None",
            ),
        ),
        TemplateSpec(
            visual_type="pivotTable",
            style_variant="Style 5",
            name="Teal Summit Totals",
            description="Summit-inspired matrix emphasizing teal subtotals.",
            features=[
                "Teal headers contrasted with white totals",
                "Prominent subtotals styled for dashboards",
                "Compact typography with Calibri consistency",
            ],
            properties=matrix_properties(
                name="Teal Summit Totals",
                header_bg="#3A8899",
                header_font="#FFFFFF",
                value_font=deep_navy,
                grid_color=surf,
                subtotal_bg="#CFE6ED",
                highlight_font=deep_navy,
                background_color="#FFFFFF",
                show_background=False,
                subtotal_position="Bottom",
                expand_buttons=False,
                row_header_weight="None",
            ),
        ),
        TemplateSpec(
            visual_type="pivotTable",
            style_variant="Style 6",
            name="Frosted Harbor Cells",
            description="Frosted glass effect with vertical grid accents.",
            features=[
                "Frosted harbor background with soft tint",
                "Vertical and horizontal separators for dense tables",
                "Balanced totals mirroring header palette",
            ],
            properties=matrix_properties(
                name="Frosted Harbor Cells",
                header_bg=surf,
                header_font=deep_navy,
                value_font=deep_navy,
                grid_color=pebble,
                subtotal_bg=drift,
                highlight_font=deep_navy,
                background_color=mist,
                show_background=True,
                subtotal_position="Bottom",
                expand_buttons=True,
                row_header_weight="None",
            ),
        ),
        TemplateSpec(
            visual_type="tableEx",
            style_variant="Style 1",
            name="Golden Harbor Ledger",
            description="Warm ledger presentation with golden headers.",
            features=[
                "Golden header band for emphasis",
                "Alternating mist rows for legibility",
                "Totals reversed for quick scanning",
            ],
            properties=table_properties(
                name="Golden Harbor Ledger",
                header_bg="#D9A441",
                header_font="#FFFFFF",
                value_font=deep_navy,
                grid_color=pebble,
                background_color=mist,
                banding_color="#FFFFFF",
                show_background=True,
                totals_background="#C7D8E4",
                totals_font=deep_navy,
            ),
        ),
        TemplateSpec(
            visual_type="tableEx",
            style_variant="Style 2",
            name="Mistline Accent Table",
            description="Cool accent table with mistline grid markers.",
            features=[
                "Mistline header with navy typography",
                "Thin gridlines for restrained separation",
                "Neutral totals ready for export",
            ],
            properties=table_properties(
                name="Mistline Accent Table",
                header_bg=surf,
                header_font=deep_navy,
                value_font=charcoal,
                grid_color=pebble,
                background_color="#FFFFFF",
                banding_color="#FFFFFF",
                show_background=False,
                totals_background=mist,
                totals_font=deep_navy,
            ),
        ),
        TemplateSpec(
            visual_type="tableEx",
            style_variant="Style 3",
            name="Midnight Ribbon Rows",
            description="Dark ribbon headers with alternating midnight rows.",
            features=[
                "Midnight navy headers with white contrast",
                "Ribbon-style mist banding on values",
                "Totals matched to header sheen",
            ],
            properties=table_properties(
                name="Midnight Ribbon Rows",
                header_bg=deep_navy,
                header_font="#FFFFFF",
                value_font=charcoal,
                grid_color="#B0C7D4",
                background_color=mist,
                banding_color="#F8FBFD",
                show_background=True,
                totals_background="#0F305C",
                totals_font="#FFFFFF",
            ),
        ),
        TemplateSpec(
            visual_type="tableEx",
            style_variant="Style 4",
            name="Polar Stripe Summary",
            description="Crisp arctic-inspired table with polar stripes.",
            features=[
                "Polar striped rows with subtle contrast",
                "Centered headers with icy palette",
                "Totals muted for supporting detail",
            ],
            properties=table_properties(
                name="Polar Stripe Summary",
                header_bg=sky,
                header_font=deep_navy,
                value_font=deep_navy,
                grid_color=surf,
                background_color=mist,
                banding_color="#FFFFFF",
                show_background=True,
                totals_background=drift,
                totals_font=deep_navy,
            ),
        ),
    ]

    visual_styles: Dict[str, Dict[str, object]] = {}
    for template in templates:
        visual_styles.setdefault(template.visual_type, {})[template.name] = template.properties

    return {
        "schema": schema,
        "templates": templates,
        "visual_styles": visual_styles,
    }


def flatten_properties(prefix: str, value: object, rows: List[Dict[str, str]]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            flatten_properties(new_prefix, child, rows)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            new_prefix = f"{prefix}[{idx}]"
            flatten_properties(new_prefix, item, rows)
    else:
        rows.append({"path": prefix, "value": json.dumps(value)})


def write_outputs(
    repo_root: Path,
    schema_file: Path,
    manifest_json: Path,
    manifest_md: Path,
    template_json: Path,
    change_log_csv: Path,
    validation_md: Path,
) -> None:
    schema = schema_file.read_text(encoding="utf-8").splitlines()[0] if schema_file.exists() else ""
    data = build_templates(schema)
    templates: List[TemplateSpec] = data["templates"]
    visual_styles = data["visual_styles"]

    template_payload = {
        "$schema": "https://github.com/microsoft/powerbi-desktop-samples/blob/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.114.json",
        "name": "Rainwater TableMatrix Templates",
        "visualStyles": visual_styles,
    }
    template_json.parent.mkdir(parents=True, exist_ok=True)
    template_json.write_text(json.dumps(template_payload, indent=2), encoding="utf-8")

    manifest_json.parent.mkdir(parents=True, exist_ok=True)
    manifest = [
        {
            "visual_type": t.visual_type,
            "style_variant": t.style_variant,
            "template_name": t.name,
            "description": t.description,
            "features": t.features,
        }
        for t in templates
    ]
    manifest_json.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "# Table & Matrix Template Manifest",
        "",
        "Creative naming follows the three-word brief and reflects the look and feel captured from catalog insights.",
    ]
    for template in templates:
        lines.append("")
        lines.append(f"## {template.name}")
        lines.append("")
        lines.append(f"- Visual type: `{template.visual_type}` ({template.style_variant})")
        lines.append(f"- Description: {template.description}")
        lines.append("- Highlights:")
        for feature in template.features:
            lines.append(f"  - {feature}")
    manifest_md.parent.mkdir(parents=True, exist_ok=True)
    manifest_md.write_text("\n".join(lines), encoding="utf-8")

    change_log_csv.parent.mkdir(parents=True, exist_ok=True)
    change_rows: List[Dict[str, str]] = []
    for template in templates:
        entries: List[Dict[str, str]] = []
        flatten_properties("", template.properties, entries)
        for entry in entries:
            change_rows.append(
                {
                    "template_name": template.name,
                    "visual_type": template.visual_type,
                    "style_variant": template.style_variant,
                    "property_path": entry["path"],
                    "value": entry["value"],
                    "note": "Derived from curated template design",
                }
            )
    with change_log_csv.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["template_name", "visual_type", "style_variant", "property_path", "value", "note"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(change_rows)

    # Validation
    def font_check(properties: Dict[str, object]) -> List[str]:
        messages: List[str] = []
        entries: List[Dict[str, str]] = []
        flatten_properties("", properties, entries)
        for entry in entries:
            if entry["path"].endswith("fontFamily"):
                if json.loads(entry["value"]) != "Calibri":
                    messages.append(entry["path"])
        return messages

    validation_lines = [
        "# Table & Matrix Template Validation",
        "",
        "## Summary",
        "",
        f"- Templates generated: {len(templates)}",
        "- Schema reference: reportThemeSchema-2.114.json",
    ]
    font_issues: List[str] = []
    for template in templates:
        issues = font_check(template.properties)
        if issues:
            font_issues.extend(f"{template.name}: {issue}" for issue in issues)
    validation_lines.append(f"- Font verification issues: {len(font_issues)}")
    validation_lines.append("")
    validation_lines.append("## Checks Performed")
    validation_lines.append("")
    validation_lines.append("- Ensured each template uses Calibri for all fontFamily properties.")
    validation_lines.append("- Flattened property trees to confirm structured paths for change logging.")
    validation_lines.append("- Recorded palette selections to align with Rainwater theme colors.")
    validation_lines.append("")
    if font_issues:
        validation_lines.append("## Font Issues")
        validation_lines.extend(f"- {issue}" for issue in font_issues)
    else:
        validation_lines.append("All font families resolved to Calibri as required.")
    validation_md.parent.mkdir(parents=True, exist_ok=True)
    validation_md.write_text("\n".join(validation_lines), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build table/matrix templates and related artifacts.")
    parser.add_argument("--prompt", default="docs/prompts/table_matrix_template_creation.xml", type=Path)
    args = parser.parse_args(argv)

    prompt_path: Path = args.prompt.resolve()
    tree = None
    try:
        import xml.etree.ElementTree as ET

        tree = ET.parse(prompt_path)
    except FileNotFoundError:
        raise SystemExit("Prompt file not found.")

    root = tree.getroot()

    def text(path: str) -> str:
        node = root.find(path)
        if node is None or node.text is None:
            raise ValueError(f"Missing path in prompt: {path}")
        return node.text.strip()

    repo_root = prompt_path.parents[1]
    schema_file = repo_root / text("./context/schemaFile")
    manifest_json = repo_root / text("./outputs/path[1]")
    manifest_md = repo_root / text("./outputs/path[2]")
    template_json = repo_root / text("./outputs/path[3]")
    change_log_csv = repo_root / text("./outputs/path[4]")
    validation_md = repo_root / text("./outputs/path[5]")

    write_outputs(
        repo_root=repo_root,
        schema_file=schema_file,
        manifest_json=manifest_json,
        manifest_md=manifest_md,
        template_json=template_json,
        change_log_csv=change_log_csv,
        validation_md=validation_md,
    )


if __name__ == "__main__":
    main()
