# TTC Streetcar Delay Analysis
## Overview
This project analyzes historical Toronto Transit Commission (TTC) streetcar delay records from 2014 to 2026 to examine service reliability, identify delay patterns, and investigate potential operational bottlenecks.

Using Python for data processing and Microsoft Excel for interactive data visualization, the project transforms raw historical records into structured datasets and an analytical dashboard.

The project focuses on understanding how streetcar delays vary across routes, time periods, and incident categories to support data-driven operational insights.

## Objectives
- Analyze historical TTC streetcar delay patterns from 2014 to 2026.
- Identify routes with the highest frequency and severity of reported delays.
- Examine temporal patterns across days, hours, months, and years.
- Investigate incident categories contributing to reported delay minutes.
- Develop an interactive Excel dashboard to communicate key findings.
- Automate data cleaning, standardization, and aggregation using Python.

## Data Source
The dataset was obtained from the [City of Toronto Open Data Portal](https://open.toronto.ca/dataset/ttc-streetcar-delay-data/)

## Tools & Technologies
- **Python:** Data processing and automation.
- **Pandas:** Data cleaning, transformation, standardization, and aggregration.
- **Microsoft Excel:** Interactive dashboards, PivotTables, PivotCharts, and slicers

## Dashboard Overview
The workbook contains four interactive analytical dashboards:
### 1. Overview
Provides a summary of TTC streetcar delay performance, including total delay records, accumulated delay minutes, average delay duration, and historical trends.
### 2. Route Performance
Compares streetcar routes based on reported delay frequency, total delay in minutes, and average delay duration to identify routes with potentially greater operational challenges.
### 3. Temporal Analysis
Examines delay patterns across different days of the week, hours of the day, months, and years to identify periods associated with higher delay activity.
### 4. Incident Analysis
Examines incident categories based on reported frequency, total delay minutes, and average delay duration to identify categories contributing significantly to historical streetcar delays.

## Key Findings
- Route 501 recorded the highest accumulated delay minutes among the 13 regular streetcar routes.
- Route 508 recorded the highest average delay per incident, at approximately 29.48 minutes.
- February 2025 recorded the highest monthly total delay minutes.
- The analysis identified temporal and incident-related patterns that may warrant further operational investigation.

## Limitations
- 2026 data is partial, covering January through September.
- A good chunk of the records (2014–2024) primarily use free-text incident descriptions, while recent records (2025–2026) use a separate incident-code classification system. These classifications are analyzed separately where appropriate.
- Some recent incident codes could not be matched to descriptions in the available TTC reference data.
- Reported delay records reflect recorded incidents and may not capture every aspect of actual service disruption.
- Identified patterns indicate potential operational bottlenecks but do not independently establish the underlying causes of delays.
