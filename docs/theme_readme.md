# License Cost Analysis General Theme

## Purpose
Provides a lightweight Power BI general theme built from the License Cost Analysis report imagery. The theme smooths hand-off to Power BI by codifying shared background, accent, border, and typography defaults.

## Theme Properties
| Property | Value | Notes |
| --- | --- | --- |
| Background | `#E4E3E1` | Warm neutral canvas color drawn from report chrome. |
| Accent | `#D9531E` | Primary orange applied to bars, lines, and KPI markers. |
| Border Color | `#F8FAFC` | Soft off-white card separators. |
| Border Radius | `5 px` | Approximate rounded corners on cards. |
| Border Weight | `1 px` | Thin divider frames for visuals. |
| Title Text | `#2F2F30` at ~32 pt | Bold report and section headers. |
| KPI Numerics | `#2F2F30` at ~24 pt | Key metric figures (e.g., `$7.19`). |
| Body Text | `#2F2F30` at ~14-16 pt | Standard labels, tables, slicer inputs. |

## Applying in Power BI
1. Open Power BI Desktop and load the target report.
2. Navigate to `View` -> `Themes` -> `Browse for themes`.
3. Select `themes/outputs/general-theme.json`.
4. Verify canvas background, accent visuals, and border treatments apply as expected.
5. Adjust visual-specific options only if needed; general settings remain in the theme file for reuse.

## Repository Inventory

See `repo_tree.txt` for the consolidated workspace snapshot.

## RainwaterTheme v3.4.3

### Key Changes
- Removed style presets from pivot table and matrix visuals.
- Applied navy/white header palette with white body background and navy text drawn from the AI Narrative screenshot.
- Harmonised totals highlighting and grid lines to the observed light steel blue accents.

### Assets
- `docs/theme_properties_v3_4_3.md` � Image-derived property notes.
- `docs/theme_mapping_v3_4_3.md` � Pivot/table field mapping.
- `themes/outputs/rainwater/v3_4_3/rainwater_theme_v3_4_3.json` � Final theme JSON.

## RainwaterTheme v4.4

### Key Changes
- Introduced Rainwater 4.4 general theme with updated Calibri typography and navy/white palette.
- Synced pivot table and table visuals with refreshed subtotal/totals styling and balanced white row backgrounds.
- Published reusable Rainwater matrix/table templates for future automation.

### Assets
- 	hemes/outputs/rainwater/Rainwater 4.4.json - Latest Rainwater theme build.
- 	hemes/inputs/visual_templates/rainwater matrix template.json - Matrix template exported from 4.4.
- 	hemes/inputs/visual_templates/rainwater table template.json - Table template exported from 4.4.

