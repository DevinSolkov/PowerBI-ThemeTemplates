AA# Rainwater Theme v4.1 vs Catalog

## Overview

- Total attribute keys compared: 625
- In both: 27
- Only in theme: 391
- Only in scans: 207
- Mismatched values: 8

## Recommendations

- Extend theme coverage for `advancedSlicerVisual.accentBar[id=default].position` to align with 13 catalog instance(s).
- Extend theme coverage for `advancedSlicerVisual.fillCustom[id=interaction:hover].fillColor.solid.color` to align with 13 catalog instance(s).V
- Extend theme coverage for `advancedSlicerVisual.fillCustom[id=interaction:hover].transparency` to align with 13 catalog instance(s).
- Align `clusteredColumnChart.categoryAxis.fontFamily` (theme uses `Segoe UI`) with dominant catalog value `Calibri` observed 4 time(s).
- Align `clusteredColumnChart.labels.fontFamily` (theme uses `Segoe UI Semibold`) with dominant catalog value `Calibri` observed 4 time(s).

## Top Missing Attributes (catalog only)

| Visual Type | Attribute | Instances | Sample Source |
| --- | --- | ---: | --- |
| advancedSlicerVisual | accentBar[id=default].position | 13 | 3.Sample Files/Spend Cube.Report/definition/pages/02604e232e37ce8027cd/visuals/59cc9da5c4d0f55695a5/visual.json |
| advancedSlicerVisual | fillCustom[id=interaction:hover].fillColor.solid.color | 13 | 3.Sample Files/Spend Cube.Report/definition/pages/02604e232e37ce8027cd/visuals/59cc9da5c4d0f55695a5/visual.json |
| advancedSlicerVisual | fillCustom[id=interaction:hover].transparency | 13 | 3.Sample Files/Spend Cube.Report/definition/pages/02604e232e37ce8027cd/visuals/59cc9da5c4d0f55695a5/visual.json |
| advancedSlicerVisual | layout.columnCount | 13 | 3.Sample Files/Spend Cube.Report/definition/pages/02604e232e37ce8027cd/visuals/59cc9da5c4d0f55695a5/visual.json |
| advancedSlicerVisual | layout.rowCount | 13 | 3.Sample Files/Spend Cube.Report/definition/pages/02604e232e37ce8027cd/visuals/59cc9da5c4d0f55695a5/visual.json |

## Top Value Mismatches

| Visual Type | Attribute | Theme Value | Dominant Catalog | Occurrences |
| --- | --- | --- | --- | ---: |
| clusteredColumnChart | categoryAxis.fontFamily | Segoe UI | Calibri | 4 |
| clusteredColumnChart | labels.fontFamily | Segoe UI Semibold | Calibri | 4 |
| clusteredColumnChart | labels.labelPrecision | 0 | 1 | 4 |
| clusteredColumnChart | legend.show | false | true | 2 |
| shape | fill.fillColor.solid.color | #FFFFFF | ThemeDataColor(ColorId=6,Percent=0) | 7 |
