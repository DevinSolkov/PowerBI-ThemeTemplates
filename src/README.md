# Source Scripts
The `src/scripts/` folder hosts automation entry points:
- `build_table_matrix_templates.py` – generate table/matrix presets and manifests using catalog data.
- `integrate_table_matrix_templates.py` – merge generated presets into the Rainwater theme.
- `table_matrix_style_report.py` – summarise style attributes across themes and catalog scans.
- `theme_summary_comparison.py` – compare Rainwater theme coverage, emit diffs, and normalise fonts.

Each script loads configuration from XML prompts in `docs/prompts/`. Run them with Python 3.11+:
```
python src/scripts/<script>.py --prompt docs/prompts/<prompt>.xml
```
Outputs land in `themes/` or `reports/` as declared in each prompt.
