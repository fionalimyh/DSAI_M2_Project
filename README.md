# Brazil Delivery Time & Revenue Analysis Dashboard

![Dashboard](/Document/dashboard.png)

## Overview

An interactive dual-layer web dashboard for analysing delivery performance and revenue across Brazilian regions. Built on the Olist e-commerce dataset with a dbt + BigQuery data pipeline feeding a Leaflet/Plotly.js frontend.

## Quick Start

```bash
cd /Users/fengfeng/Dev/DSAI_M2_Project/olist/notebook
python3 run_delivery_revenue_dashboard.py
```

Opens at **http://localhost:8004/brazil_delivery_revenue_dashboard.html**. Press `Ctrl+C` to stop.

## Features

### Map

- **Three view modes** — Delivery Time, Revenue, and Dual Layer
- **Dual Layer view**: outer colored ring = delivery speed, inner solid circle = revenue
- **Zoom-based aggregation** — automatically switches between aggregation levels as you zoom:
  | Zoom | Level |
  |------|-------|
  | < 7  | State |
  | 7–10 | City  |
  | ≥ 11 | Zip code |
- **7 map tile styles** — selectable from a dropdown in the top-right corner of the map (CartoDB Voyager, Light, Dark, Esri Gray, Stadia Smooth, OpenStreetMap, and more)
- **Aggregation level badge** — bottom-left corner always shows the current zoom level

### Color Schemes

| Layer | Colors | Meaning |
|-------|--------|---------|
| Delivery Time | Green → Yellow → Orange → Red | ≤7 / 8–14 / 15–21 / >21 days |
| Revenue | Light blue → Dark navy | Low → High revenue |

### Filters (Left Panel)

- **State selector** — multi-select with Select All / Deselect All
- **City selector** — auto-updates based on selected states; includes a search bar
- **Delivery time range slider** — dual-handle slider on a single axis to filter by a min–max day range (e.g. 10–15 days); only shown in Delivery and Dual views

### Charts

#### Delivery vs Revenue Correlation
Scatter plot of delivery days vs revenue per zip code region. Includes a linear regression trend line showing:
- **Slope** — revenue change per extra delivery day
- **R²** — how much of revenue variance is explained by delivery time alone

#### Regional Performance Score
Horizontal bar chart of the top 10 and bottom 10 regions ranked by a composite score:

```
Score (0–100) = (Revenue Score × 0.6) + (Delivery Speed Score × 0.4)
```

Both sub-scores are normalised to the current filtered data, so scores shift when filters change.

### Explanatory Text

All metrics, charts, and controls include inline descriptions so viewers can understand what they are looking at without prior context.

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Data warehouse | BigQuery |
| Transformation | dbt (staging → intermediate → marts) |
| Map | Leaflet.js |
| Charts | Plotly.js |
| Frontend | Vanilla HTML/CSS/JavaScript |
| Data fallback | Sample data generated in-browser when BigQuery unavailable |

## Data Pipeline

```
Kaggle CSV files
  → Google Cloud Storage
    → BigQuery (raw tables)
      → dbt models
          staging/        (10 source models)
          intermediate/   (4 joined models)
          marts/core/     (fct_delivery_time_by_zip, fct_geo_revenue, fct_orders, 4 dim tables)
          marts/business_intelligence/  (customer, financial, operational, product analytics)
```

See `Document/project_steps.md` for setup instructions including GCP service account, dbt profile configuration, and data loading scripts.

## File Structure

```
olist/notebook/
├── brazil_delivery_revenue_dashboard.html   # Main dashboard
├── dashboard_data_generator_en.py           # Generates dashboard_data.json from BigQuery
├── dashboard_data.json                      # Pre-generated data file
└── run_delivery_revenue_dashboard.py        # HTTP server (port 8004)
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Blank map / no circles | Check browser console; verify `dashboard_data.json` exists |
| City filter empty | Select at least one state first |
| Circles not visible in dual view | Zoom in — at low zoom only the outer delivery ring may be visible |
| Slow rendering | Use state/city filters or the delivery time range slider to reduce data volume |

### Verify data file

```bash
python3 -c "
import json
with open('dashboard_data.json') as f:
    data = json.load(f)
print('Records:', len(data['data']))
print('Fields:', list(data['data'][0].keys()))
"
```

### Refresh data from BigQuery

```bash
cd olist/notebook
python3 dashboard_data_generator_en.py
```

---

**Version**: 3.0.0
**Last Updated**: May 2026
**Compatibility**: Modern browsers with JavaScript ES6+ support
