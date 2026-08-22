# ⚡ India EV Charging Infrastructure Intelligence Platform

### Data-driven spatial analytics and decision intelligence for EV charging infrastructure planning across India.

<p align="center">
  <b>Identify Charging Gaps • Analyse Demand • Evaluate Corridors • Recommend Sites</b>
</p>

---

## 🚀 Overview

India's EV adoption is growing rapidly, but charging infrastructure is not distributed uniformly across regions, highways, commercial areas, and high-demand locations.

This project addresses a practical infrastructure-planning question:

> **Where should the next EV charging stations be deployed to maximise demand coverage, accessibility, and infrastructure readiness?**

The **India EV Charging Infrastructure Intelligence Platform** combines EV registration data, existing charging infrastructure, commercial points of interest, highway corridors, and electrical substations into an interactive decision-support system.

Instead of producing a static analysis, the project converts multiple datasets into an **end-to-end analytical platform** that helps identify underserved areas, evaluate corridor readiness, rank potential locations, and simulate different investment priorities.

---

## 🎯 Business Problem

EV charging expansion involves several competing factors:

* Where is EV demand concentrated?
* Which areas have insufficient charging coverage?
* Which highway corridors have infrastructure gaps?
* Which commercial areas have strong charging potential?
* Which candidate locations have nearby electrical infrastructure?
* How should different factors be weighted when selecting a site?
* How sensitive are recommendations to changing business priorities?

This platform attempts to answer these questions through **spatial analytics + demand analysis + infrastructure intelligence + multi-criteria decision analysis (MCDA).**

---

# 💡 What the Platform Does

| Module                         | Purpose                                                     |
| ------------------------------ | ----------------------------------------------------------- |
| 📌 Executive Summary           | National-level EV ecosystem overview and key metrics        |
| 🗺️ Spatial Infrastructure     | Explore charging infrastructure and geographic density      |
| 📊 Demand & Vahan Analytics    | Analyse EV registrations and demand patterns                |
| 🌵 Charging Desert Analysis    | Identify high-demand areas with limited charging coverage   |
| 🛣️ Highway Corridor Readiness | Evaluate charging gaps along major highway corridors        |
| 🎯 Site Recommendation Engine  | Rank candidate locations using MCDA                         |
| 🎛️ Scenario Simulator         | Test how recommendations change under different priorities  |
| 📈 Data Quality & Monitoring   | Monitor missingness, coordinate validity and data integrity |
| 📚 Methodology & Documentation | Explain assumptions, methodology and system design          |

The repository currently implements these capabilities through a **9-page Streamlit application**.

---

# 📊 Data Landscape

The platform integrates multiple datasets representing different dimensions of the EV ecosystem.

### Core datasets

| Dataset                   | Role in Analysis                              |
| ------------------------- | --------------------------------------------- |
| 🔌 EV Charging Stations   | Existing charging infrastructure              |
| 🚗 Vahan EV Registrations | EV adoption and demand signals                |
| 🏢 Points of Interest     | Commercial/activity-based demand indicators   |
| ⚡ Power Substations       | Electrical infrastructure accessibility       |
| 🛣️ Highway Corridors     | Long-distance mobility and corridor readiness |

The current project contains approximately **130K+ records across these data domains**, including charging stations, EV registrations, POIs, substations and highway corridor data.

> **Data note:** Individual datasets may originate from different public sources and undergo preprocessing before analysis. Refer to the data catalogue and methodology documentation before interpreting individual metrics as official national statistics.

---

# 🧠 Analytical Framework

The project follows an end-to-end analytical pipeline:

```text
                    ┌──────────────────────┐
                    │   Source Datasets    │
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
                    │   Data Validation    │
                    │                      │
                    │ Missing Values       │
                    │ Coordinates          │
                    │ Duplicates           │
                    │ Schema Validation    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ETL / Database     │
                    │                      │
                    │ Cleaning             │
                    │ Transformation       │
                    │ Storage              │
                    └──────────┬───────────┘
                               │
                               ▼
             ┌─────────────────┴─────────────────┐
             │                                   │
             ▼                                   ▼
    ┌──────────────────┐              ┌────────────────────┐
    │ Spatial Analytics│              │ Demand Analytics   │
    │                  │              │                    │
    │ KDTree           │              │ EV registrations   │
    │ Catchments       │              │ POI demand         │
    │ Density          │              │ Highway activity   │
    │ Gap Detection    │              │                    │
    └────────┬─────────┘              └──────────┬─────────┘
             │                                   │
             └─────────────────┬─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Decision Intelligence│
                    │                      │
                    │ AHP / TOPSIS / MCDA  │
                    │ Explainability       │
                    │ Scenario Analysis    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Interactive Platform │
                    │                      │
                    │ Streamlit            │
                    │ PyDeck               │
                    │ Folium               │
                    │ Plotly               │
                    └──────────────────────┘
```

---

# 🗺️ Spatial Analytics

Spatial analysis is one of the core differentiators of this project.

The platform uses spatial relationships to evaluate:

* Distance between demand and charging infrastructure
* Charging coverage within defined catchments
* Infrastructure density
* Highway corridor gaps
* Proximity to electrical substations
* Commercial demand clusters
* Potential charging deserts

The GIS engine includes spatial indexing, catchment analysis, highway-network analysis and hotspot detection.

### Spatial indexing

The project uses **SciPy KDTree** to support nearest-neighbour and radius-based spatial searches across large geospatial datasets.

This allows spatial queries to be handled more efficiently than repeatedly performing naïve pairwise comparisons.

---

# 🌵 Charging Desert Detection

A **charging desert** is treated as an area where charging infrastructure does not adequately serve the surrounding demand.

The analysis considers relationships between:

```text
EV Demand
     +
Commercial Activity
     +
Existing Charging Coverage
     ↓
Charging Gap
```

Areas with stronger demand signals and insufficient charging coverage can therefore be prioritised for further investigation.

> The classification is an analytical model rather than an official government designation.

---

# 🛣️ Highway Corridor Readiness

Long-distance EV adoption depends heavily on charging availability along major travel corridors.

The platform evaluates selected National Highway corridors to identify sections where charging infrastructure may be insufficient.

The repository currently includes corridor datasets covering highways such as:

* NH-48
* NH-44
* NH-65
* NH-16
* NH-66

---

# 🎯 Site Recommendation Engine

The project goes beyond identifying gaps.

It attempts to answer:

> **Which candidate locations should be prioritised?**

The recommendation engine uses **Multi-Criteria Decision Analysis (MCDA)**.

Candidate locations can be evaluated using factors such as:

* Commercial demand
* Charging gap
* Grid readiness
* Highway traffic / accessibility

The repository implements **AHP/TOPSIS-based composite scoring** and provides score attribution to make recommendations more interpretable.

### Conceptual scoring framework

```text
Candidate Location
       │
       ├── Demand Score
       ├── Charging Gap Score
       ├── Grid Readiness Score
       └── Highway / Accessibility Score
                │
                ▼
         Weighted Scoring
                │
                ▼
          MCDA Ranking
                │
                ▼
      Recommended Locations
```

---

# 🔍 Explainability

A recommendation is more useful when the user understands **why** it received a high score.

The platform therefore provides score attribution so users can inspect the contribution of individual decision factors.

For example:

```text
Candidate A

Commercial Demand       ████████████████  32%
Charging Gap            ████████████      27%
Grid Readiness          █████████          23%
Highway Accessibility   ███████             18%
                                      ───────
                                        100%
```

This helps transform the recommendation from a black-box ranking into a more transparent decision-support output.

---

# 🎛️ Scenario Simulator

Infrastructure planning rarely has one fixed objective.

Different stakeholders may prioritise:

* Maximum EV demand
* Maximum charging-gap reduction
* Better grid accessibility
* Highway coverage
* Commercial potential

The scenario simulator allows decision-makers to adjust the relative importance of these factors and observe how candidate rankings change.

This makes the platform useful for **what-if analysis**, rather than only producing one fixed ranking.

---

# 📈 Data Quality & Monitoring

Data quality is treated as part of the analytical workflow.

The platform includes monitoring for issues such as:

* Missing values
* Invalid coordinates
* Coordinate bounds
* Duplicate records
* Dataset integrity

A dedicated Data Quality & Monitoring module is included in the application.

---

# 🏗️ System Architecture

```text
EV/
│
├── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── config.py
│   │
│   ├── etl/
│   │   ├── cleaner.py
│   │   └── pipeline.py
│   │
│   ├── gis_engine/
│   │   ├── spatial_index.py
│   │   ├── catchment.py
│   │   ├── network.py
│   │   └── hotspot.py
│   │
│   ├── decision_engine/
│   │   ├── mcda.py
│   │   ├── explainability.py
│   │   └── simulator.py
│   │
│   └── database/
│       └── db_manager.py
│
├── pages/
│   ├── 1_Executive_Summary.py
│   ├── 2_Spatial_Infrastructure.py
│   ├── 3_Demand_Analytics.py
│   ├── 4_Charging_Desert_Analysis.py
│   ├── 5_Highway_Corridor_Readiness.py
│   ├── 6_Site_Recommendation_Engine.py
│   ├── 7_Scenario_Simulator.py
│   ├── 8_Data_Quality_Monitoring.py
│   └── 9_Methodology_Documentation.py
│
├── docs/
│   ├── BRD.md
│   ├── PRD.md
│   ├── DATA_CATALOGUE.md
│   └── ARCHITECTURE.md
│
├── tests/
│   ├── test_etl.py
│   ├── test_gis_engine.py
│   ├── test_decision_engine.py
│   └── run_tests.py
│
├── requirements.txt
└── README.md
```

The repository follows a modular architecture separating ETL, GIS processing, decision intelligence, database access, application pages and testing.

---

# 🧪 Testing

Automated tests are included for the major analytical components.

Run:

```bash
python tests/run_tests.py
```

The project documentation currently describes the automated testing module as complete.

---

# 💻 Tech Stack

### Programming & Analytics

* Python
* Pandas
* NumPy
* SciPy
* Scikit-learn

### GIS & Visualization

* PyDeck
* Folium
* Plotly

### Application

* Streamlit

### Data & Storage

* SQLite
* Parquet
* Excel

### Decision Intelligence

* AHP
* TOPSIS
* MCDA
* Scenario Analysis

### Engineering

* ETL pipelines
* Data validation
* Automated testing
* Modular architecture

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/koushikgarg11/EV.git
cd EV
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run tests

```bash
python tests/run_tests.py
```

## 5. Launch the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📂 Documentation

Additional project documentation is available in the `docs/` directory:

| Document            | Purpose                                     |
| ------------------- | ------------------------------------------- |
| `BRD.md`            | Business requirements and business context  |
| `PRD.md`            | Product requirements and feature definition |
| `DATA_CATALOGUE.md` | Dataset and field-level documentation       |
| `ARCHITECTURE.md`   | Technical architecture                      |

---

# 📌 Key Analytical Outputs

The platform is designed to produce outputs such as:

### Infrastructure

* Charging station distribution
* Charging density
* Infrastructure gaps
* Charging-desert candidates

### Demand

* EV registration trends
* State / district-level demand patterns
* Commercial demand clusters

### Mobility

* Highway corridor readiness
* Infrastructure gaps along selected corridors

### Site Selection

* Candidate location ranking
* MCDA composite scores
* Factor-level score attribution

### Planning

* What-if scenarios
* Weight sensitivity
* Data-quality indicators

---

# ⚠️ Important Methodology & Data Disclaimer

This project is an **analytical decision-support system**, not an official government infrastructure-planning model.

Results depend on:

* Dataset coverage
* Data freshness
* Geographic accuracy
* Feature engineering choices
* Distance / catchment assumptions
* MCDA criteria
* Weight selection
* Availability of public infrastructure data

Therefore, recommended locations should be treated as **analytical candidates for further validation**, not as definitive investment decisions.

---

# 🔮 Future Improvements

Potential extensions include:

* [ ] Real-time charging-station availability
* [ ] EV traffic-flow integration
* [ ] More granular charger utilisation data
* [ ] Road-network travel-time modelling
* [ ] Weather and terrain features
* [ ] Charger utilisation forecasting
* [ ] Cost / ROI modelling
* [ ] Electricity tariff modelling
* [ ] Capacity-aware grid optimisation
* [ ] Historical backtesting of site recommendations
* [ ] API layer for external applications
* [ ] Cloud deployment and scheduled data refresh

---

# 👨‍💻 Why I Built This

This project was built to explore how **data analytics can move beyond dashboards and descriptive reporting into actual decision intelligence.**

The objective was to combine:

**Data Engineering**

→ **Spatial Analytics**

→ **Demand Analysis**

→ **Decision Modelling**

→ **Explainability**

→ **Interactive Business Intelligence**

into one end-to-end system.

The broader goal is to demonstrate how analytics can help answer not just:

> **"What is happening?"**

but also:

> **"Where is the problem?"**

> **"Why is it happening?"**

> **"Where should we act?"**

> **"What happens if our priorities change?"**

---

# ⭐ Project Highlights

```text
130K+       Multi-domain records
9           Interactive Streamlit modules
5           Major data domains
MCDA        Site recommendation framework
GIS         Spatial infrastructure analysis
ETL         Automated data workflows
Testing     Automated analytical tests
Docs        BRD + PRD + Architecture + Data Catalogue
```



### Built with Python • Streamlit • GIS • Data Analytics • Decision Intelligence
