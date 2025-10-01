## Overview
- Spend Cube PBIP under /3.Sample Files/Spend Cube.Report exposes 8 pages with 191 visual containers (including 36 visual group containers used for layered layouts).
- Visual mix leans on 39 standard slicers, 13 Advanced Slicer custom visuals, 12 bookmark-driven action buttons, 7 Smart Narratives, and 3 Power KPI Matrix custom visuals.
- Report-level filters keep Direct vs Indirect purchases, operating units, and null suppression locked; bookmarks (25 JSON files) drive the action buttons for narrative open/close states.
- The file imports the corporate Rainwater theme (base CY24SU10 plus custom RainwaterTheme11234990230315.json) and embeds four image assets for branding.
- Generated inventory snapshot: /2.Custom Themes/Spend Cube/01_overview/spend-cube-inventory.json summarises counts, pages, and bookmark metadata for downstream automation.

## Folder map inside the report
- /3.Sample Files/Spend Cube.Report/definition/report.json - report-wide theme bindings, global filters, custom visual registrations, and performance settings.
- /3.Sample Files/Spend Cube.Report/definition/pages/<pageId>/page.json - per page canvas settings, drillthrough filters, and navigation metadata.
- /3.Sample Files/Spend Cube.Report/definition/pages/<pageId>/visuals/*/visual.json - individual visuals (standard, custom, and visualGroup containers) with data bindings and formatting.
- /3.Sample Files/Spend Cube.Report/definition/bookmarks/*.json - 25 scenario bookmarks referenced by action buttons and narratives for open/close states.
- /3.Sample Files/Spend Cube.Report/definition/version.json - schema version (2.0.0) for compatibility tracking.
- /2.Custom Themes/Spend Cube/01_overview/spend-cube-inventory.json - generated counts to keep reporting idempotent.

## Pages summary
- **Receipt Line Item Detail** (29 visuals): dense drillthrough detail combining 12 slicers, large transaction table, and action buttons for returning to summaries.
- **AP Summary** (42 visuals): landing dashboard packed with KPI cards, bookmarked narratives, and grouped layout frames; shapes/textboxes structure the header grid.
- **AP Indirect - Level Analysis** (27 visuals): advanced slicers by fiscal filters, pivot tables for level rollups, and a single line chart for trend context.
- **AP Checks** (17 visuals): slice-heavy layout (7 slicers) with AI narrative and bookmarked toggle buttons to flip narrative states.
- **AP Details** (18 visuals): transactional table focus with slicers per branch/vendor and action buttons tied to detail bookmarks.
- **Page 1** (2 visuals): prototype page with a single clustered column chart plus table, likely retained for design references.
- **AP Direct Overview** (29 visuals): mirrored structure to the summary page with direct spend KPIs, synced slicers, and grouped card clusters.
- **Open PO's (Qty Due > 0)** (27 visuals): operational focus featuring 10 slicers, PO tables, and action buttons that trigger open/close bookmark pairs.

## Visuals inventory
| Visual type | Count | Notes |
| --- | ---: | --- |
| Standard slicer | 39 | Dropdown and list slicers across pages; many synced via slicer groups. |
| Advanced Slicer (custom) | 13 | Custom visual for multi-select chips; bookmark-aware and synced. |
| Action button | 12 | Bookmark navigation for narrative open/close and back actions. |
| Visual group container | 36 | Canvas grouping to coordinate backgrounds, cards, and slicers. |
| Text box | 21 | Descriptive headers, captions, and KPI labels. |
| Shape | 18 | Layout scaffolding (background blocks, separators). |
| Image | 15 | Logos, legend callouts, and decorative assets. |
| Smart narrative | 7 | AI-generated narratives toggled via bookmarks. |
| Card | 7 | High-level KPI callouts (amounts, counts). |
| Table | 8 | TableEx visuals for detailed transaction lists. |
| Pivot table | 6 | PivotTable visuals for hierarchy exploration. |
| Power KPI Matrix (custom) | 3 | Certified custom visual for KPI grids. |
| Clustered column chart | 4 | Metric by category; one in the prototype page. |
| Line chart | 1 | Trend on indirect spend levels. |
| Waterfall chart | 1 | Spend contribution breakdown. |

Additional assets: 25 bookmarks, 1 report-level drillthrough configuration, and a single public custom visual dependency (Power KPI Matrix).

## Next actions
- Derive per-visual property fingerprints for each visual type (especially advanced slicers, Smart Narratives, Power KPI Matrix) to support style varianting.
- Produce human+CSV property inventories, ensuring visualGroup containers are tracked separately from renderable visuals.
- Validate bookmark/action button wiring while mapping properties to canonical templates in the next milestone.
