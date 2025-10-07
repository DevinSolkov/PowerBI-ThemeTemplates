#!/usr/bin/env python3
"""Generate table/matrix style attribute report from theme and scan artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


TARGET_VISUALS = {
    "tableEx": "Table",
    "pivotTable": "Matrix",
    "matrix": "Matrix",
    "matrixVisual": "Matrix",
    "table": "Table",
}


@dataclass
class PromptConfig:
    repo_root: Path
    theme_path: Path
    schema_path: Path
    catalog_json_path: Path
    catalog_csv_path: Path
    outputs: Dict[str, Path]


def load_prompt(prompt_path: Path) -> PromptConfig:
    tree = ET.parse(prompt_path)
    root = tree.getroot()

    def require_text(xpath: str) -> str:
        node = root.find(xpath)
        if node is None or node.text is None:
            raise ValueError(f"Missing node: {xpath}")
        return node.text.strip()

    repo_root = prompt_path.resolve().parents[1]
    theme_path = repo_root / require_text("./context/themeFile")
    schema_path = repo_root / require_text("./context/schemaFile")
    catalog_json_path = repo_root / require_text("./context/ingestionCatalog")
    catalog_csv_path = repo_root / require_text("./context/ingestionCsv")

    outputs: Dict[str, Path] = {}
    for node in root.findall("./outputs/path"):
        if node.text:
            rel = node.text.strip()
            outputs[Path(rel).name] = repo_root / rel

    return PromptConfig(
        repo_root=repo_root,
        theme_path=theme_path,
        schema_path=schema_path,
        catalog_json_path=catalog_json_path,
        catalog_csv_path=catalog_csv_path,
        outputs=outputs,
    )


def flatten_theme_style(style_node: object) -> Dict[str, object]:
    """Flatten a theme style definition to dotted keys."""
    results: Dict[str, object] = {}

    def recurse(node: object, logical: List[str]) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                recurse(value, logical + [key])
        elif isinstance(node, list):
            for item in node:
                recurse(item, logical)
        else:
            if logical:
                key = ".".join(logical)
                results[key] = node

    recurse(style_node, [])
    return results


def load_catalog_rows(catalog_path: Path) -> List[Dict[str, str]]:
    with catalog_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def family_from_key(key: str) -> str:
    if not key:
        return ""
    if "." in key:
        return key.split(".", 1)[0]
    return key


def normalise_style_name(name: str) -> str:
    return name or "Default"


def gather_styles(
    theme_data: Dict[str, object], catalog_rows: Iterable[Dict[str, str]]
) -> Tuple[Dict[Tuple[str, str], Dict[str, object]], Dict[str, Dict[str, Counter]]]:
    styles: Dict[Tuple[str, str], Dict[str, object]] = defaultdict(
        lambda: {"sources": set(), "attributes": {}, "display_name": ""}
    )
    catalog_attributes: Dict[str, Dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter)
    )

    visual_styles = theme_data.get("visualStyles", {}) if isinstance(theme_data, dict) else {}
    for visual_type, style_map in visual_styles.items():
        if visual_type not in TARGET_VISUALS:
            continue
        if not isinstance(style_map, dict):
            continue
        for style_name, definition in style_map.items():
            style_key = (visual_type, normalise_style_name(style_name))
            flattened = flatten_theme_style(definition)
            styles[style_key]["sources"].add("theme")
            styles[style_key]["attributes"] = {
                key: str(value) if not isinstance(value, (dict, list)) else json.dumps(value)
                for key, value in flattened.items()
            }
            styles[style_key]["display_name"] = style_label(style_key)

    for row in catalog_rows:
        visual_type = row.get("visual_type", "")
        if visual_type not in TARGET_VISUALS:
            continue
        style_name = normalise_style_name(row.get("style_variant", ""))
        style_key = (visual_type, style_name)
        styles[style_key]["sources"].add("catalog")
        styles[style_key]["display_name"] = style_label(style_key)
        key = row.get("attribute_key", "")
        if key:
            catalog_attributes[style_label(style_key)][key].update([row.get("attribute_value", "")])

    return styles, catalog_attributes


def style_label(style_key: Tuple[str, str]) -> str:
    visual_type, style_name = style_key
    pretty_visual = TARGET_VISUALS.get(visual_type, visual_type)
    return f"{pretty_visual} - {style_name}"


def write_styles_json(styles: Dict[Tuple[str, str], Dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = []
    for style_key, info in sorted(styles.items(), key=lambda item: style_label(item[0])):
        data.append(
            {
                "visual_type": style_key[0],
                "style_variant": style_key[1],
                "display_name": info.get("display_name") or style_label(style_key),
                "sources": sorted(info.get("sources", [])),
                "theme_attribute_count": len(info.get("attributes", {})),
            }
        )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def write_attributes_csv(
    styles: Dict[Tuple[str, str], Dict[str, object]],
    catalog_attributes: Dict[str, Dict[str, Counter]],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "visual_type",
        "style_variant",
        "display_name",
        "attribute_key",
        "attribute_family",
        "source",
        "count",
        "example_value",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for style_key, info in sorted(styles.items(), key=lambda item: style_label(item[0])):
            display = info.get("display_name") or style_label(style_key)
            # Theme attributes
            for key, value in sorted(info.get("attributes", {}).items()):
                writer.writerow(
                    {
                        "visual_type": style_key[0],
                        "style_variant": style_key[1],
                        "display_name": display,
                        "attribute_key": key,
                        "attribute_family": family_from_key(key),
                        "source": "theme",
                        "count": 1,
                        "example_value": value,
                    }
                )
            # Catalog attributes
            catalog_map = catalog_attributes.get(display, {})
            for key, counter in sorted(catalog_map.items()):
                most_common = counter.most_common(1)
                sample_value = most_common[0][0] if most_common else ""
                writer.writerow(
                    {
                        "visual_type": style_key[0],
                        "style_variant": style_key[1],
                        "display_name": display,
                        "attribute_key": key,
                        "attribute_family": family_from_key(key),
                        "source": "catalog",
                        "count": sum(counter.values()),
                        "example_value": sample_value,
                    }
                )


def build_markdown_report(
    styles: Dict[Tuple[str, str], Dict[str, object]],
    catalog_attributes: Dict[str, Dict[str, Counter]],
    output_path: Path,
    theme_present: bool,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [info.get("display_name") or style_label(key) for key, info in sorted(styles.items(), key=lambda item: style_label(item[0]))]
    attribute_keys = set()
    for info in styles.values():
        attribute_keys.update(info.get("attributes", {}).keys())
    for style_name, attr_map in catalog_attributes.items():
        attribute_keys.update(attr_map.keys())
    attribute_rows = sorted(attribute_keys)

    lines: List[str] = []
    lines.append("# Table & Matrix Style Attribute Reference")
    lines.append("")
    lines.append("This report summarises configurable attributes for table and matrix visual styles, drawing from the Rainwater theme and scanned catalog artifacts.")
    lines.append("")
    lines.append("## Styles Covered")
    lines.append("")
    for key, info in sorted(styles.items(), key=lambda item: style_label(item[0])):
        display = info.get("display_name") or style_label(key)
        sources = ", ".join(sorted(info.get("sources", []))) or "n/a"
        lines.append(f"- `{display}` (sources: {sources})")
    lines.append("")
    lines.append("Legend: `Theme:` value found in the Rainwater theme; `Scan:` count of occurrences in the catalog with the dominant example value.")
    lines.append("")

    header = ["Attribute", "Family"] + columns
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")

    style_lookup = {info.get("display_name") or style_label(key): info for key, info in sorted(styles.items(), key=lambda item: style_label(item[0]))}

    for attribute in attribute_rows:
        family = family_from_key(attribute)
        row_cells = [attribute, family]
        for column in columns:
            info = style_lookup.get(column, {})
            parts: List[str] = []
            theme_attrs = info.get("attributes", {})
            if attribute in theme_attrs:
                parts.append(f"Theme: `{theme_attrs[attribute]}`")
            catalog_map = catalog_attributes.get(column, {})
            if attribute in catalog_map:
                counter = catalog_map[attribute]
                total = sum(counter.values())
                sample_value = counter.most_common(1)[0][0] if counter else ""
                if sample_value:
                    parts.append(f"Scan {total}: `{sample_value}`")
                else:
                    parts.append(f"Scan {total}")
            cell = "<br>".join(parts) if parts else "-"
            row_cells.append(cell)
        lines.append("| " + " | ".join(row_cells) + " |")

    if not theme_present:
        lines.append("")
        lines.append("> Note: The current Rainwater theme does not define explicit table or matrix style blocks; all attributes above originate from catalog observations.")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate table/matrix style attribute report.")
    parser.add_argument("--prompt", type=Path, default=Path("5.Prompts/TableMatrixStyleReport.xml"))
    args = parser.parse_args(argv)

    config = load_prompt(args.prompt.resolve())
    theme_data = json.loads(config.theme_path.read_text(encoding="utf-8"))
    catalog_rows = load_catalog_rows(config.catalog_json_path)

    styles, catalog_attributes = gather_styles(theme_data, catalog_rows)

    styles_json = config.outputs.get("table_matrix_style_styles.json")
    attributes_csv = config.outputs.get("table_matrix_style_attributes.csv")
    markdown_path = config.outputs.get("table_matrix_style_report.md")

    if not styles_json or not attributes_csv or not markdown_path:
        raise ValueError("Output paths missing in prompt outputs block.")

    write_styles_json(styles, styles_json)
    write_attributes_csv(styles, catalog_attributes, attributes_csv)
    theme_present = any("theme" in info.get("sources", set()) for info in styles.values())
    build_markdown_report(styles, catalog_attributes, markdown_path, theme_present)


if __name__ == "__main__":
    main()
