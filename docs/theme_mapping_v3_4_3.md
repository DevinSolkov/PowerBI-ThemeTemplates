## Rainwater 3.4.3 – Table & Matrix Mapping

| Property | Target Visual | JSON Path | Value | Notes |
| --- | --- | --- | --- | --- |
| Header background navy | tableEx | `visualStyles.tableEx["*"].columnHeaders[0].backColor.solid.color` | `#0C2340` | Matches screenshot header bar. |
| Header font white | tableEx | `visualStyles.tableEx["*"].columnHeaders[0].fontColor.solid.color` | `#FFFFFF` | White uppercase text. |
| Header font size | tableEx | `visualStyles.tableEx["*"].columnHeaders[0].fontSize` | 12 | Approximate 12 pt. |
| Header alignment center | tableEx | `visualStyles.tableEx["*"].columnHeaders[0].alignment` | `Center` | Observed centering. |
| Value background white | tableEx | `visualStyles.tableEx["*"].values[0].backColor.solid.color` | `#FFFFFF` | No banding visible. |
| Value font navy | tableEx | `visualStyles.tableEx["*"].values[0].fontColor.solid.color` | `#0C2340` | Matches body text. |
| Value font size | tableEx | `visualStyles.tableEx["*"].values[0].fontSize` | 11 | Slightly smaller than headers. |
| Total top highlight background | tableEx | `visualStyles.tableEx["*"].total[0].backColor.solid.color` | `#0C2340` | Use navy block for totals card. |
| Total font color | tableEx | `visualStyles.tableEx["*"].total[0].fontColor.solid.color` | `#FFFFFF` | White totals text. |
| Grid horizontal color | tableEx | `visualStyles.tableEx["*"].grid[0].gridHorizontalColor.solid.color` | `#B0C4D4` | Soft blue separators. |
| Grid vertical off | tableEx | `visualStyles.tableEx["*"].grid[0].gridVertical` | false | None displayed. |
| Pivot header background navy | pivotTable | `visualStyles.pivotTable["*"].columnHeaders[0].backColor.solid.color` | `#0C2340` | Align pivot table with table. |
| Pivot header font white | pivotTable | `visualStyles.pivotTable["*"].columnHeaders[0].fontColor.solid.color` | `#FFFFFF` | White header text. |
| Pivot header size | pivotTable | `visualStyles.pivotTable["*"].columnHeaders[0].fontSize` | 12 | Matches table header sizing. |
| Pivot value font navy | pivotTable | `visualStyles.pivotTable["*"].values[0].fontColor.solid.color` | `#0C2340` | Align body text. |
| Pivot value font size | pivotTable | `visualStyles.pivotTable["*"].values[0].fontSize` | 11 | Consistent with table rows. |
| Pivot totals background | pivotTable | `visualStyles.pivotTable["*"].totals[0].backgroundColor.solid.color` | `#BDCBDC` | Light highlight strip. |
| Pivot totals font color | pivotTable | `visualStyles.pivotTable["*"].totals[0].fontColor.solid.color` | `#0C2340` | Bold navy totals. |
| Pivot grid horizontal color | pivotTable | `visualStyles.pivotTable["*"].grid[0].gridHorizontalColor.solid.color` | `#B0C4D4` | Matching separators. |
| Pivot grid vertical off | pivotTable | `visualStyles.pivotTable["*"].grid[0].gridVertical` | false | No vertical lines observed. |
