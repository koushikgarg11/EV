# ⚡ India EV Charging Infrastructure Intelligence Platform

### Data-driven spatial analytics and decision intelligence for EV charging infrastructure planning across India.

<p align="center">
  <b>Identify Charging Gaps • Analyse Demand • Evaluate Corridors • Recommend Sites</b>
</p>

<p align="center">
  <a href="https://chargedesert.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20LIVE%20DASHBOARD-Launch%20App-brightgreen?style=for-the-badge" alt="Live Dashboard">
  </a>
</p>

<p align="center">
  <a href="https://github.com/koushikgarg11/EV">
    <img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github" alt="GitHub Repository">
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Application-red?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/GIS-Spatial%20Analytics-orange?style=for-the-badge" alt="GIS">
</p>

---

## 🚀 Explore the Live Platform

> **The project is deployed as an interactive Streamlit application.**

### 👉 [Launch the Live EV Charging Intelligence Dashboard](https://chargedesert.streamlit.app/)

The deployed platform allows users to interact with the analytical modules directly in the browser, including:

- 📌 Executive EV infrastructure overview
- 🗺️ Spatial infrastructure analysis
- 📊 EV demand and registration analytics
- 🌵 Charging desert identification
- 🛣️ Highway corridor readiness
- 🎯 EV charging site recommendations
- 🎛️ Scenario simulation
- 📈 Data quality monitoring
- 📚 Methodology and documentation

---

## 🎯 Project Overview

India's EV adoption is growing rapidly, but charging infrastructure is not distributed uniformly across regions, highways, commercial areas, and high-demand locations.

This project addresses a practical infrastructure-planning question:

> **Where should the next EV charging stations be deployed to maximise demand coverage, accessibility, and infrastructure readiness?**

The **India EV Charging Infrastructure Intelligence Platform** combines EV registration data, existing charging infrastructure, commercial points of interest, highway corridors, and electrical substations into an interactive decision-support system.

Rather than producing only a static analysis or dashboard, the project brings together:

**Data Engineering → Spatial Analytics → Demand Analysis → Decision Modelling → Explainability → Interactive Business Intelligence**

---

## 💼 Business Problem

EV charging expansion involves several competing considerations:

- Where is EV demand concentrated?
- Which areas have insufficient charging coverage?
- Where are potential charging deserts?
- Which highway corridors have infrastructure gaps?
- Which commercial areas have strong charging potential?
- Which candidate locations have nearby electrical infrastructure?
- How should different factors be weighted when selecting a site?
- How sensitive are recommendations when business priorities change?

The platform attempts to address these questions through:

> **Spatial Analytics + Demand Analysis + Infrastructure Intelligence + Multi-Criteria Decision Analysis (MCDA)**

---

## 💡 What the Platform Does

| Module | Purpose |
|---|---|
| 📌 Executive Summary | National-level EV ecosystem overview and key metrics |
| 🗺️ Spatial Infrastructure | Explore charging infrastructure and geographic density |
| 📊 Demand & Vahan Analytics | Analyse EV registrations and demand patterns |
| 🌵 Charging Desert Analysis | Identify high-demand areas with limited charging coverage |
| 🛣️ Highway Corridor Readiness | Evaluate charging gaps along major highway corridors |
| 🎯 Site Recommendation Engine | Rank candidate locations using MCDA |
| 🎛️ Scenario Simulator | Test how recommendations change under different priorities |
| 📈 Data Quality & Monitoring | Monitor missingness, coordinate validity and data integrity |
| 📚 Methodology & Documentation | Explain assumptions, methodology and system design |

The project is implemented as a **9-page Streamlit application**.

---

## 📊 Data Landscape

The platform integrates multiple datasets representing different dimensions of the EV ecosystem.

### Core Data Domains

| Dataset | Role in Analysis |
|---|---|
| 🔌 EV Charging Stations | Existing charging infrastructure |
| 🚗 Vahan EV Registrations | EV adoption and demand signals |
| 🏢 Points of Interest | Commercial/activity-based demand indicators |
| ⚡ Power Substations | Electrical infrastructure accessibility |
| 🛣️ Highway Corridors | Long-distance mobility and corridor readiness |

The current project contains approximately **130K+ records across these data domains**, including charging stations, EV registrations, POIs, substations and highway corridor data.

> **Data Note:** Individual datasets may originate from different public sources and undergo preprocessing before analysis. Refer to the data catalogue and methodology documentation before interpreting individual metrics as official national statistics.

---

## 🧠 Analytical Framework

The project follows an end-to-end analytical pipeline:

```text
                    ┌──────────────────────┐
                    │   SOURCE DATASETS    │
                    │                      │
                    │ EV Registrations     │
                    │ Charging Stations    │
                    │ POIs                 │
                    │ Power Substations    │
                    │ Highway Corridors    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   DATA VALIDATION    │
                    │                      │
                    │ Missing Values       │
                    │ Coordinates          │
                    │ Duplicates           │
                    │ Schema Validation    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    ETL / STORAGE     │
                    │                      │
                    │ Cleaning             │
                    │ Transformation       │
                    │ Database / Files     │
                    └──────────┬───────────┘
                               │
                               ▼
             ┌─────────────────┴─────────────────┐
             │                                   │
             ▼                                   ▼
    ┌──────────────────┐              ┌────────────────────┐
    │ SPATIAL ANALYTICS│              │  DEMAND ANALYTICS  │
    │                  │              │                    │
    │ KDTree           │              │ EV Registrations   │
    │ Catchments       │              │ POI Demand         │
    │ Density          │              │ Highway Activity   │
    │ Gap Detection    │              │                    │
    └────────┬─────────┘              └──────────┬─────────┘
             │                                   │
             └─────────────────┬─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ DECISION INTELLIGENCE│
                    │                      │
                    │ AHP / TOPSIS / MCDA  │
                    │ Explainability       │
                    │ Scenario Analysis    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  LIVE STREAMLIT APP   │
                    │                      │
                    │ Interactive Maps     │
                    │ Dashboards           │
                    │ Recommendations      │
                    │ Scenario Simulation  │
                    └──────────────────────┘
```
