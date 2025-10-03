#!/usr/bin/env python3
"""Utilities for the Theme Summary Comparison prompt pipeline."""
from __future__ import annotations

import argparse
import copy
import csv
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

VISUAL_TYPE_SYNONYMS = {
    'advancedslivervisual': 'slicer',
    'advanced slicer visual': 'slicer',
    'advanced slicer': 'slicer',
}


def canonical_visual_type(name: str) -> str:
    if not name:
        return ''
    key = name.lower()
    mapped = VISUAL_TYPE_SYNONYMS.get(key)
    if mapped:
        return mapped
    return name


def normalized_visual_type_key(name: str) -> str:
    canonical = canonical_visual_type(name)
    if canonical == '*':
        return '__global__'
    return canonical.lower()


def display_visual_type_label(name: str) -> str:
    canonical = canonical_visual_type(name)
    if canonical == '*':
        return '*'
    return canonical


def normalize_attribute_key(key: str) -> str:
    return (key or '').lower()


def stringify_value(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    return str(value)


@dataclass
class PipelineConfig:
    repo_root: Path
    theme_file: Path
    human_summary: Path
    catalog_csv_input: Path
    inventory_path: Path
    schema_file: Path
    outputs: Dict[str, Path]


@dataclass
class ThemeAttribute:
    visual_type: str
    style_variant: str
    attribute_key: str
    pointer: str
    value: object

    def normalized_key(self) -> Tuple[str, str]:
        return normalized_visual_type_key(self.visual_type), normalize_attribute_key(self.attribute_key)

    def display_visual_type(self) -> str:
        return display_visual_type_label(self.visual_type)

    def serialized_value(self) -> str:
        return stringify_value(self.value)


@dataclass
class CatalogAttribute:
    report_path: str
    page_id: str
    visual_id: str
    visual_type: str
    style_variant: str
    attribute_key: str
    attribute_value: str
    value_type: str
    source_path: str

    def normalized_key(self) -> Tuple[str, str]:
        return normalized_visual_type_key(self.visual_type), normalize_attribute_key(self.attribute_key)

    def display_visual_type(self) -> str:
        return display_visual_type_label(self.visual_type)

    def serialized_value(self) -> str:
        return self.attribute_value or ''


def load_config(prompt_path: Path) -> PipelineConfig:
    tree = ET.parse(prompt_path)
    root = tree.getroot()

    def require_text(xpath: str) -> str:
        node = root.find(xpath)
        if node is None or node.text is None:
            raise ValueError(f"Missing required node: {xpath}")
        return node.text.strip()

    repo_root = prompt_path.resolve().parents[1]

    theme_file = repo_root / require_text('./context/themeFile')
    human_summary = repo_root / require_text('./context/scanArtifacts/humanSummary')
    catalog_csv_input = repo_root / require_text('./context/scanArtifacts/catalogCsv')
    inventory_path = repo_root / require_text('./context/scanArtifacts/inventory')
    schema_file = repo_root / require_text('./context/schemaFile')

    outputs: Dict[str, Path] = {}
    for node in root.findall('./outputs/path'):
        if node.text:
            raw = node.text.strip()
            outputs[Path(raw).name] = repo_root / raw

    return PipelineConfig(
        repo_root=repo_root,
        theme_file=theme_file,
        human_summary=human_summary,
        catalog_csv_input=catalog_csv_input,
        inventory_path=inventory_path,
        schema_file=schema_file,
        outputs=outputs,
    )


def load_visual_properties(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def derive_attribute_family(property_path: str) -> str:
    if not property_path:
        return ''
    if '.' in property_path:
        return property_path.split('.', 1)[0]
    return property_path


def build_catalog(rows: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    catalog: List[Dict[str, str]] = []
    for row in rows:
        family = derive_attribute_family(row.get('property_path', ''))
        catalog.append(
            {
                'report_path': row.get('report_path', ''),
                'page_id': row.get('page_id', ''),
                'visual_id': row.get('visual_id', ''),
                'visual_type': row.get('visual_type', ''),
                'style_variant': row.get('style_variant', ''),
                'attribute_family': family,
                'attribute_key': row.get('property_path', ''),
                'attribute_name': row.get('property_name', ''),
                'attribute_value': row.get('property_value', ''),
                'value_type': row.get('value_type', ''),
                'source_path': row.get('source_file', ''),
            }
        )
    catalog.sort(
        key=lambda item: (
            item['report_path'],
            item['page_id'],
            item['visual_id'],
            item['attribute_key'],
        )
    )
    return catalog


def validate_catalog_sources(catalog: Sequence[Dict[str, str]], repo_root: Path) -> Dict[str, List[str]]:
    missing_sources: set[str] = set()
    missing_reports: set[str] = set()
    checked_reports: set[str] = set()
    for item in catalog:
        report = item['report_path'].lstrip('/')
        if report and report not in checked_reports:
            checked_reports.add(report)
            report_dir = repo_root / report
            if not report_dir.exists():
                missing_reports.add(report)
        source_rel = item['source_path']
        if source_rel:
            source_path = repo_root / source_rel
            if not source_path.exists():
                missing_sources.add(source_rel)
    return {
        'missing_reports': sorted(missing_reports),
        'missing_sources': sorted(missing_sources),
    }


def write_catalog(catalog: Sequence[Dict[str, str]], csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        'report_path',
        'page_id',
        'visual_id',
        'visual_type',
        'style_variant',
        'attribute_family',
        'attribute_key',
        'attribute_name',
        'attribute_value',
        'value_type',
        'source_path',
    ]
    with csv_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in catalog:
            writer.writerow({field: row.get(field, '') for field in fieldnames})
    with json_path.open('w', encoding='utf-8') as handle:
        json.dump(list(catalog), handle, indent=2)


def summarise_visual_attributes(catalog: Sequence[Dict[str, str]]) -> Dict[str, object]:
    visuals = {(item['report_path'], item['page_id'], item['visual_id']) for item in catalog}
    families = Counter(item['attribute_family'] or 'unknown' for item in catalog)
    by_visual_type: Dict[str, Counter[str]] = defaultdict(Counter)
    for item in catalog:
        visual_type = item['visual_type'] or 'unknown'
        family = item['attribute_family'] or 'unknown'
        by_visual_type[visual_type][family] += 1
    return {
        'total_rows': len(catalog),
        'unique_visuals': len(visuals),
        'families': families,
        'by_visual_type': by_visual_type,
    }


def truncate_label(value: str, limit: int = 48) -> str:
    value = value or 'unknown'
    if len(value) <= limit:
        return value
    return value[: limit - 3] + '...'


def render_summary_markdown(stats: Dict[str, object], check_results: Dict[str, List[str]], human_summary_path: Path) -> str:
    lines: List[str] = []
    lines.append('# Visual Attribute Summary')
    lines.append('')
    lines.append(f"Total cataloged attributes: {stats['total_rows']}")
    lines.append(f"Unique visuals covered: {stats['unique_visuals']}")
    missing_sources = check_results['missing_sources']
    missing_reports = check_results['missing_reports']
    if missing_sources:
        lines.append(f"Missing source files: {len(missing_sources)} (see appendix)")
    else:
        lines.append('Missing source files: 0')
    if missing_reports:
        lines.append(f"Missing report directories: {len(missing_reports)} (see appendix)")
    else:
        lines.append('Missing report directories: 0')
    lines.append('')
    lines.append('## Attribute Families (Top 10)')
    lines.append('')
    lines.append('| Attribute Family | Count |')
    lines.append('| --- | ---: |')
    for family, count in stats['families'].most_common(10):
        lines.append(f"| {truncate_label(family)} | {count} |")
    lines.append('')
    lines.append('## Visual Type x Attribute Family (Top 5 each)')
    lines.append('')
    lines.append('| Visual Type | Top Families |')
    lines.append('| --- | --- |')
    for visual_type, fam_counter in sorted(stats['by_visual_type'].items()):
        top_chunks = []
        for name, count in fam_counter.most_common(5):
            top_chunks.append(f"{truncate_label(name)}:{count}")
        top_families = ', '.join(top_chunks) or '—'
        lines.append(f"| {truncate_label(visual_type)} | {top_families} |")
    if missing_sources or missing_reports:
        lines.append('')
        lines.append('## Appendix: Missing References')
        if missing_reports:
            lines.append('')
            lines.append('### Report directories not found')
            for report in missing_reports:
                lines.append(f'- {report}')
        if missing_sources:
            lines.append('')
            lines.append('### Source files not found')
            for source in missing_sources:
                lines.append(f'- {source}')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append(f'Reference human summary: `{human_summary_path}`')
    lines.append('')
    return '\n'.join(lines)


def run_ingestion(config: PipelineConfig) -> None:
    rows = load_visual_properties(config.catalog_csv_input)
    catalog = build_catalog(rows)
    outputs = config.outputs
    csv_path = outputs.get('catalog.csv')
    json_path = outputs.get('catalog.json')
    if not csv_path or not json_path:
        raise ValueError('Output paths for catalog CSV/JSON not found in prompt outputs block')
    write_catalog(catalog, csv_path, json_path)
    checks = validate_catalog_sources(catalog, config.repo_root)
    stats = summarise_visual_attributes(catalog)
    summary_md = render_summary_markdown(stats, checks, config.human_summary)
    summary_path = outputs.get('summary_visual_attributes.md')
    if not summary_path:
        raise ValueError('Summary output path not defined in prompt outputs')
    summary_path.write_text(summary_md, encoding='utf-8')


def flatten_theme_visual_styles(theme_data: Dict[str, object]) -> List[ThemeAttribute]:
    visual_styles = theme_data.get('visualStyles', {})
    entries: List[ThemeAttribute] = []

    for visual_type, style_map in visual_styles.items():
        if not isinstance(style_map, dict):
            continue
        for style_variant, definition in style_map.items():
            pointer_root = ['visualStyles', visual_type, style_variant]

            def walk(node: object, pointer_parts: List[str], logical_parts: List[str]) -> None:
                if isinstance(node, dict):
                    for key, value in node.items():
                        walk(value, pointer_parts + [key], logical_parts + [key])
                elif isinstance(node, list):
                    for idx, item in enumerate(node):
                        walk(item, pointer_parts + [str(idx)], logical_parts)
                else:
                    if logical_parts:
                        entries.append(
                            ThemeAttribute(
                                visual_type=visual_type,
                                style_variant=style_variant,
                                attribute_key='.'.join(logical_parts),
                                pointer='/' + '/'.join(pointer_parts),
                                value=node,
                            )
                        )

            walk(definition, pointer_root, [])
    return entries


def load_catalog_attributes(config: PipelineConfig) -> List[CatalogAttribute]:
    output_csv = config.outputs.get('catalog.csv')
    rows: List[Dict[str, str]]
    if output_csv and output_csv.exists():
        with output_csv.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
    else:
        source_rows = load_visual_properties(config.catalog_csv_input)
        rows = build_catalog(source_rows)
    attributes: List[CatalogAttribute] = []
    for row in rows:
        attributes.append(
            CatalogAttribute(
                report_path=row.get('report_path', ''),
                page_id=row.get('page_id', ''),
                visual_id=row.get('visual_id', ''),
                visual_type=row.get('visual_type', ''),
                style_variant=row.get('style_variant', ''),
                attribute_key=row.get('attribute_key', ''),
                attribute_value=row.get('attribute_value', ''),
                value_type=row.get('value_type', ''),
                source_path=row.get('source_path', ''),
            )
        )
    return attributes


def build_diff_records(theme_attrs: List[ThemeAttribute], catalog_attrs: List[CatalogAttribute]) -> List[Dict[str, object]]:
    theme_map: Dict[Tuple[str, str], List[ThemeAttribute]] = defaultdict(list)
    for attr in theme_attrs:
        if attr.attribute_key:
            theme_map[attr.normalized_key()].append(attr)
    catalog_map: Dict[Tuple[str, str], List[CatalogAttribute]] = defaultdict(list)
    for attr in catalog_attrs:
        if attr.attribute_key:
            catalog_map[attr.normalized_key()].append(attr)

    diff_records: List[Dict[str, object]] = []
    for key in sorted(theme_map.keys() | catalog_map.keys()):
        theme_list = theme_map.get(key, [])
        catalog_list = catalog_map.get(key, [])
        classification = 'in_both'
        if theme_list and not catalog_list:
            classification = 'only_in_theme'
        elif catalog_list and not theme_list:
            classification = 'only_in_scans'

        attribute_key = theme_list[0].attribute_key if theme_list else (catalog_list[0].attribute_key if catalog_list else '')
        display_visual = theme_list[0].display_visual_type() if theme_list else (catalog_list[0].display_visual_type() if catalog_list else '')
        theme_values = [attr.serialized_value() for attr in theme_list]
        theme_pointers = [attr.pointer for attr in theme_list]
        theme_styles = sorted({attr.style_variant for attr in theme_list})

        catalog_values = [attr.serialized_value() for attr in catalog_list]
        catalog_styles = sorted({attr.style_variant for attr in catalog_list if attr.style_variant})
        value_counts = Counter(catalog_values)
        value_counts_list = [{'value': val, 'count': cnt} for val, cnt in value_counts.most_common()]
        dominant_value = value_counts_list[0]['value'] if value_counts_list else ''
        dominant_count = value_counts_list[0]['count'] if value_counts_list else 0

        if classification == 'in_both':
            match_status = 'aligned' if set(theme_values) & set(value_counts.keys()) else 'mismatch'
        else:
            match_status = 'n/a'

        catalog_samples = [
            {
                'report_path': attr.report_path,
                'page_id': attr.page_id,
                'visual_id': attr.visual_id,
                'style_variant': attr.style_variant,
                'attribute_value': attr.attribute_value,
                'source_path': attr.source_path,
            }
            for attr in catalog_list[:5]
        ]

        diff_records.append(
            {
                'classification': classification,
                'normalized_visual_type': key[0],
                'display_visual_type': display_visual,
                'attribute_key': attribute_key,
                'theme': {
                    'count': len(theme_list),
                    'style_variants': theme_styles,
                    'values': theme_values,
                    'pointers': theme_pointers,
                },
                'catalog': {
                    'count': len(catalog_list),
                    'style_variants': catalog_styles,
                    'value_counts': value_counts_list,
                    'samples': catalog_samples,
                },
                'match_status': match_status,
                'dominant_catalog_value': dominant_value,
                'dominant_catalog_count': dominant_count,
            }
        )
    return diff_records


def render_diff_summary(diff_records: List[Dict[str, object]]) -> str:
    counts = Counter(record['classification'] for record in diff_records)
    total = sum(counts.values())
    mismatches = [record for record in diff_records if record['match_status'] == 'mismatch']
    missing = sorted(
        (record for record in diff_records if record['classification'] == 'only_in_scans'),
        key=lambda rec: rec['catalog']['count'],
        reverse=True,
    )
    theme_only = sorted(
        (record for record in diff_records if record['classification'] == 'only_in_theme'),
        key=lambda rec: len(rec['theme']['values']),
        reverse=True,
    )

    recommendations: List[str] = []
    for record in missing[:3]:
        recommendations.append(
            f"Extend theme coverage for `{record['display_visual_type']}.{record['attribute_key']}` to align with {record['catalog']['count']} catalog instance(s)."
        )
    for record in mismatches[:3]:
        theme_val = record['theme']['values'][0] if record['theme']['values'] else '—'
        dom_val = record['dominant_catalog_value'] or '—'
        dom_count = record['dominant_catalog_count']
        recommendations.append(
            f"Align `{record['display_visual_type']}.{record['attribute_key']}` (theme uses `{theme_val}`) with dominant catalog value `{dom_val}` observed {dom_count} time(s)."
        )
    for record in theme_only[:3]:
        theme_val = record['theme']['values'][0] if record['theme']['values'] else '—'
        recommendations.append(
            f"Validate unique theme setting `{record['display_visual_type']}.{record['attribute_key']}` = `{theme_val}`; no scanned visuals reference this attribute."
        )

    baseline_recs = [
        'Review remaining `only_in_scans` entries to prioritize future theme coverage.',
        'Confirm global (`*`) defaults align with high-usage visuals before rollout.',
        'Schedule a follow-up scan after applying Calibri updates to confirm alignment.',
        'Document rationale for any theme-only settings to guide report builders.',
        'Consider augmenting scans for visuals absent in the theme to close gaps.',
    ]
    for item in baseline_recs:
        if len(recommendations) >= 5:
            break
        if item not in recommendations:
            recommendations.append(item)

    lines: List[str] = []
    lines.append('# Rainwater Theme v4.1 vs Catalog')
    lines.append('')
    lines.append('## Overview')
    lines.append('')
    lines.append(f'- Total attribute keys compared: {total}')
    lines.append(f"- In both: {counts.get('in_both', 0)}")
    lines.append(f"- Only in theme: {counts.get('only_in_theme', 0)}")
    lines.append(f"- Only in scans: {counts.get('only_in_scans', 0)}")
    lines.append(f'- Mismatched values: {len(mismatches)}')
    lines.append('')
    lines.append('## Recommendations')
    lines.append('')
    for rec in recommendations[:5]:
        lines.append(f'- {rec}')
    lines.append('')
    lines.append('## Top Missing Attributes (catalog only)')
    lines.append('')
    lines.append('| Visual Type | Attribute | Instances | Sample Source |')
    lines.append('| --- | --- | ---: | --- |')
    if missing:
        for record in missing[:5]:
            sample_source = record['catalog']['samples'][0]['source_path'] if record['catalog']['samples'] else '—'
            lines.append(
                f"| {record['display_visual_type']} | {record['attribute_key']} | {record['catalog']['count']} | {sample_source} |"
            )
    else:
        lines.append('| — | — | 0 | — |')
    lines.append('')
    lines.append('## Top Value Mismatches')
    lines.append('')
    lines.append('| Visual Type | Attribute | Theme Value | Dominant Catalog | Occurrences |')
    lines.append('| --- | --- | --- | --- | ---: |')
    if mismatches:
        for record in mismatches[:5]:
            theme_val = record['theme']['values'][0] if record['theme']['values'] else '—'
            dom_val = record['dominant_catalog_value'] or '—'
            lines.append(
                f"| {record['display_visual_type']} | {record['attribute_key']} | {theme_val} | {dom_val} | {record['dominant_catalog_count']} |"
            )
    else:
        lines.append('| — | — | — | — | 0 |')
    lines.append('')
    return '\n'.join(lines)


def write_diff_outputs(diff_records: List[Dict[str, object]], config: PipelineConfig) -> None:
    json_path = config.outputs.get('diff_rainwater_v4_1_vs_catalog.json')
    csv_path = config.outputs.get('diff_rainwater_v4_1_vs_catalog.csv')
    summary_path = config.outputs.get('exec_summary_diff.md')

    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open('w', encoding='utf-8') as handle:
            json.dump(diff_records, handle, indent=2)

    if csv_path:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            'classification',
            'visual_type',
            'attribute_key',
            'theme_style_variants',
            'theme_values',
            'theme_pointers',
            'catalog_count',
            'catalog_style_variants',
            'catalog_dominant_value',
            'catalog_sample_value',
            'catalog_sample_source',
            'match_status',
        ]
        with csv_path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for record in diff_records:
                samples = record['catalog']['samples']
                sample_value = samples[0]['attribute_value'] if samples else ''
                sample_source = samples[0]['source_path'] if samples else ''
                writer.writerow(
                    {
                        'classification': record['classification'],
                        'visual_type': record['display_visual_type'],
                        'attribute_key': record['attribute_key'],
                        'theme_style_variants': ';'.join(record['theme']['style_variants']),
                        'theme_values': ';'.join(record['theme']['values']),
                        'theme_pointers': ';'.join(record['theme']['pointers']),
                        'catalog_count': record['catalog']['count'],
                        'catalog_style_variants': ';'.join(record['catalog']['style_variants']),
                        'catalog_dominant_value': record['dominant_catalog_value'],
                        'catalog_sample_value': sample_value,
                        'catalog_sample_source': sample_source,
                        'match_status': record['match_status'],
                    }
                )

    if summary_path:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(render_diff_summary(diff_records), encoding='utf-8')


def run_comparison(config: PipelineConfig) -> None:
    theme_text = config.theme_file.read_text(encoding='utf-8-sig')
    theme_data = json.loads(theme_text)
    theme_attrs = flatten_theme_visual_styles(theme_data)
    catalog_attrs = load_catalog_attributes(config)
    diff_records = build_diff_records(theme_attrs, catalog_attrs)
    write_diff_outputs(diff_records, config)


def detect_newline_style(text: str) -> str:
    if '\r\n' in text:
        return '\r\n'
    return '\n'


def apply_calibri_fonts(data: object) -> List[Dict[str, str]]:
    changes: List[Dict[str, str]] = []

    def recurse(node: object, pointer_parts: List[str]) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                new_pointer = pointer_parts + [key]
                if isinstance(value, (dict, list)):
                    recurse(value, new_pointer)
                else:
                    if 'font' in key.lower() and isinstance(value, str) and value != 'Calibri':
                        node[key] = 'Calibri'
                        changes.append(
                            {
                                'json_pointer': '/' + '/'.join(new_pointer),
                                'key': key,
                                'old_value': value,
                                'new_value': 'Calibri',
                                'note': 'standardized font string to Calibri',
                            }
                        )
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                recurse(item, pointer_parts + [str(idx)])

    recurse(data, [])
    return changes


def flatten_for_verification(node: object) -> Dict[str, Tuple[object, bool]]:
    results: Dict[str, Tuple[object, bool]] = {}

    def recurse(current: object, pointer_parts: List[str]) -> None:
        if isinstance(current, dict):
            for key, value in current.items():
                recurse(value, pointer_parts + [key])
        elif isinstance(current, list):
            for idx, value in enumerate(current):
                recurse(value, pointer_parts + [str(idx)])
        else:
            pointer = '/' + '/'.join(pointer_parts)
            last_key = next((part for part in reversed(pointer_parts) if not part.isdigit()), '')
            has_font = 'font' in last_key.lower()
            results[pointer] = (current, has_font)

    recurse(node, [])
    return results


def run_calibri_standardization(config: PipelineConfig) -> None:
    original_text = config.theme_file.read_text(encoding='utf-8-sig')
    newline_style = detect_newline_style(original_text)
    original_data = json.loads(original_text)
    updated_data = copy.deepcopy(original_data)

    changes = apply_calibri_fonts(updated_data)

    output_path = config.outputs.get('Rainwater Theme v4.1.calibri.json')
    if not output_path:
        raise ValueError('Calibri theme output path missing in prompt outputs')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(updated_data, indent=4)
    if newline_style != '\n':
        json_text = json_text.replace('\n', newline_style)
    if not json_text.endswith(newline_style):
        json_text += newline_style
    output_path.write_text(json_text, encoding='utf-8')

    change_log_path = config.outputs.get('calibri_change_log.csv')
    if not change_log_path:
        raise ValueError('Change log output path missing in prompt outputs')
    change_log_path.parent.mkdir(parents=True, exist_ok=True)
    with change_log_path.open('w', encoding='utf-8', newline='') as handle:
        fieldnames = ['path', 'json_pointer', 'key', 'old_value', 'new_value', 'note']
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        relative_theme = config.theme_file.relative_to(config.repo_root)
        for change in changes:
            row = {'path': str(relative_theme)}
            row.update(change)
            writer.writerow(row)

    verification_path = config.outputs.get('verification_report.md')
    if not verification_path:
        raise ValueError('Verification report output path missing in prompt outputs')

    original_flat = flatten_for_verification(original_data)
    updated_flat = flatten_for_verification(updated_data)

    non_font_diffs = []
    font_violations = []
    for pointer, (new_value, has_font) in updated_flat.items():
        old_value, _ = original_flat.get(pointer, (None, has_font))
        if has_font:
            if isinstance(new_value, str):
                if new_value != 'Calibri':
                    font_violations.append(pointer)
            else:
                if old_value != new_value:
                    font_violations.append(pointer)
        else:
            if old_value != new_value:
                non_font_diffs.append(pointer)

    missing_pointers = sorted(set(original_flat) - set(updated_flat))
    font_total = sum(1 for _, has_font in original_flat.values() if has_font)

    lines: List[str] = []
    lines.append('# Calibri Standardization Verification')
    lines.append('')
    lines.append('## Results')
    lines.append('')
    lines.append(f'- Total font-related keys detected: {font_total}')
    lines.append(f'- Font string updates applied: {len(changes)}')
    lines.append(f'- Non-font keys altered: {len(non_font_diffs)}')
    lines.append(f'- Font verification issues: {len(font_violations)}')
    lines.append(f'- Missing pointers in updated theme: {len(missing_pointers)}')
    lines.append('')
    lines.append('## Checks Performed')
    lines.append('')
    lines.append('- Traversed theme JSON to enforce Calibri on string values where key names include `font`.')
    lines.append('- Compared original and updated trees to ensure non-font keys remain unchanged.')
    lines.append('- Validated every font-designated pointer resolves to the string `Calibri` or retains non-string values.')
    lines.append('')

    if non_font_diffs:
        lines.append('### Non-Font Differences Detected')
        lines.extend(f'- {pointer}' for pointer in non_font_diffs[:20])
        if len(non_font_diffs) > 20:
            lines.append(f'- ... {len(non_font_diffs) - 20} additional entries truncated ...')
        lines.append('')
    else:
        lines.append('No non-font differences detected.')
        lines.append('')

    if font_violations:
        lines.append('### Font Verification Issues')
        lines.extend(f'- {pointer}' for pointer in font_violations[:20])
        if len(font_violations) > 20:
            lines.append(f'- ... {len(font_violations) - 20} additional entries truncated ...')
        lines.append('')
    else:
        lines.append('All font pointers resolve to Calibri as required.')
        lines.append('')

    if missing_pointers:
        lines.append('### Missing Pointers')
        lines.extend(f'- {pointer}' for pointer in missing_pointers[:20])
        if len(missing_pointers) > 20:
            lines.append(f'- ... {len(missing_pointers) - 20} additional entries truncated ...')
        lines.append('')

    lines.append(f'Source theme: `{config.theme_file.relative_to(config.repo_root)}`')
    lines.append(f'Output theme: `{output_path.relative_to(config.repo_root)}`')
    lines.append(f'Change log: `{change_log_path.relative_to(config.repo_root)}`')
    lines.append('')

    verification_path.parent.mkdir(parents=True, exist_ok=True)
    verification_path.write_text('\n'.join(lines), encoding='utf-8')


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description='Theme Summary Comparison pipeline helper.')
    parser.add_argument('--prompt', default='5.Prompts/ThemeSummaryComparison.xml', type=Path)
    parser.add_argument('--task', choices=['ingest', 'diff', 'fonts', 'all'], default='all')
    args = parser.parse_args(argv)

    config = load_config(args.prompt.resolve())

    if args.task in {'ingest', 'all'}:
        run_ingestion(config)
    if args.task in {'diff', 'all'}:
        run_comparison(config)
    if args.task in {'fonts', 'all'}:
        run_calibri_standardization(config)


if __name__ == '__main__':
    main()
