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

The platform addresses these questions through:

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
                    │ Explainability      │
                    │ Scenario Analysis    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  LIVE STREAMLIT APP  │
                    │                      │
                    │ Interactive Maps     │
                    │ Dashboards           │
                    │ Recommendations      │
                    │ Scenario Simulation  │
                    └──────────────────────┘
```

---

## 🗺️ Spatial Analytics

Spatial analysis is a core component of the platform.

The system uses spatial relationships to evaluate:

- Distance between demand and charging infrastructure
- Charging coverage within defined catchments
- Infrastructure density
- Highway corridor gaps
- Proximity to electrical substations
- Commercial demand clusters
- Potential charging deserts

### Spatial Indexing

The project uses **SciPy KDTree** to support nearest-neighbour and radius-based spatial searches across geospatial datasets.

This enables efficient spatial querying when analysing relationships between demand locations and existing or potential charging infrastructure.

---

## 🌵 Charging Desert Detection

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

### Conceptual Logic

```text
High EV Demand
      │
      ├───────────────┐
      │               │
      ▼               ▼
Commercial        Existing
Activity          Chargers
      │               │
      └───────┬───────┘
              ▼
       Spatial Analysis
              │
              ▼
     Coverage / Demand Gap
              │
              ▼
      Charging Desert
```

> **Important:** Charging-desert classification is an analytical model created for this project and is not an official government designation.

---

## 🛣️ Highway Corridor Readiness

Long-distance EV adoption depends heavily on charging availability along major travel corridors.

The platform evaluates selected highway corridors to identify areas where charging infrastructure may be insufficient.

The corridor analysis considers factors such as:

- Existing charging infrastructure
- Geographic coverage
- Corridor accessibility
- Charging gaps
- Nearby demand signals

This helps identify highway sections that may require further infrastructure assessment.

---

## 🎯 EV Charging Site Recommendation Engine

The platform goes beyond identifying infrastructure gaps.

It attempts to answer:

> **Which candidate locations should be prioritised for further investigation?**

The recommendation engine combines multiple decision criteria to produce a comparative ranking of candidate locations.

Potential decision factors include:

- Demand intensity
- Charging gap
- Commercial activity
- Grid / substation proximity
- Highway accessibility
- Existing infrastructure coverage

### Decision Framework

```text
                 Candidate Locations
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Demand Score    Charging Gap     Infrastructure
                                      Readiness
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                 Weighted Evaluation
                         │
                         ▼
                    MCDA Scoring
                         │
                         ▼
                  Ranked Candidates
```

The resulting ranking is intended to support **screening and prioritisation**, rather than replace detailed engineering, financial, regulatory or site-level feasibility studies.

---

## 🔍 Recommendation Explainability

A recommendation is more useful when users can understand **why** a location received a particular score.

The platform presents the contribution of individual decision criteria where applicable.

This helps users understand:

- Which factors are driving a candidate's ranking
- Where a candidate performs strongly
- Where a candidate has weaknesses
- How changing priorities can affect the ranking

This makes the recommendation process more transparent than a simple unexplained score.

---

## 🎛️ Scenario Simulator

Infrastructure planning rarely has one universally optimal solution.

Different stakeholders may prioritise different objectives.

| Planning Priority | Possible Focus |
| ----------------- | -------------------------------------------------- |
| Demand-led        | Maximise EV demand coverage |
| Gap-led           | Prioritise underserved locations |
| Grid-led          | Prioritise electrical infrastructure accessibility |
| Corridor-led      | Improve highway charging coverage |
| Commercial-led    | Prioritise high-activity locations |

The scenario simulator allows users to adjust decision priorities and observe how candidate rankings respond.

This enables **what-if analysis** and helps users understand the sensitivity of recommendations to different planning assumptions.

---

## 📈 Data Quality & Monitoring

Data quality is treated as an important part of the analytical workflow.

The platform includes monitoring and validation for issues such as:

- Missing values
- Invalid coordinates
- Geographic bounds
- Duplicate records
- Incomplete records
- Dataset integrity

The purpose of this module is to make analytical outputs more transparent and help users understand potential limitations in the underlying datasets.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │     DATA SOURCES    │
                         │                     │
                         │ EV Registrations    │
                         │ Charging Stations   │
                         │ Points of Interest  │
                         │ Power Substations   │
                         │ Highway Corridors   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   DATA VALIDATION   │
                         │                     │
                         │ Missing Values      │
                         │ Coordinates         │
                         │ Duplicates          │
                         │ Schema Checks       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    ETL / DATA       │
                         │   TRANSFORMATION    │
                         │                     │
                         │ Cleaning            │
                         │ Transformation      │
                         │ Feature Preparation │
                         └──────────┬──────────┘
                                    │
                                    ▼
              ┌─────────────────────┴─────────────────────┐
              │                                           │
              ▼                                           ▼
     ┌─────────────────────┐                  ┌─────────────────────┐
     │  SPATIAL ANALYTICS  │                  │   DEMAND ANALYTICS  │
     │                     │                  │                     │
     │ KDTree              │                  │ EV Registrations    │
     │ Distance Analysis   │                  │ POI Activity        │
     │ Density             │                  │ Demand Signals      │
     │ Catchments          │                  │ Corridor Activity   │
     │ Gap Detection       │                  │                     │
     └──────────┬──────────┘                  └──────────┬──────────┘
                │                                        │
                └──────────────────┬─────────────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │ DECISION INTELLIGENCE│
                         │                     │
                         │ MCDA                │
                         │ AHP / TOPSIS        │
                         │ Explainability      │
                         │ Scenario Analysis   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   STREAMLIT APP     │
                         │                     │
                         │ Dashboards          │
                         │ Interactive Maps    │
                         │ Recommendations     │
                         │ Scenario Simulation │
                         │ Data Monitoring     │
                         └─────────────────────┘
```

---

## 🧪 Testing & Validation

The analytical workflow is designed to include validation of data-processing and analytical components.

Testing may cover areas such as:

- Data loading
- Data cleaning
- Coordinate validation
- Spatial calculations
- Feature generation
- Recommendation scoring
- Data-quality checks

If a test runner is included in the repository, tests can be executed using:

```bash
python tests/run_tests.py
```

---

## 💻 Technology Stack

### 🐍 Programming & Data Analysis

- Python
- Pandas
- NumPy
- SciPy
- Scikit-learn

### 🗺️ Geospatial Analytics

- Spatial indexing
- Coordinate-based analysis
- Distance calculations
- Geographic visualisation
- Interactive mapping

### 📊 Visualisation

- Plotly
- PyDeck
- Folium

### 🖥️ Application

- Streamlit

### 🗄️ Data & Storage

- CSV
- Excel
- Parquet
- SQLite

### 🎯 Decision Intelligence

- Multi-Criteria Decision Analysis (MCDA)
- Weighted scoring
- Scenario analysis
- Recommendation explainability

---

## 📂 Project Structure

```text
EV/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── data/
│   ├── analytics/
│   ├── gis/
│   └── recommendations/
│
├── tests/
│
├── docs/
│
└── assets/
```

> **Note:** The structure above represents the logical organisation of the project. Keep the file/folder names aligned with the actual repository if they differ.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/koushikgarg11/EV.git
cd EV
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser through the local Streamlit server.

### 5. Run tests

If the repository contains the test runner:

```bash
python tests/run_tests.py
```

---

## 📚 Documentation

The project follows a structured documentation approach covering business requirements, product requirements, data and technical architecture.

Recommended supporting documentation includes:

| Document            | Purpose |
| ------------------- | --------------------------------------------- |
| `BRD.md`            | Business Requirements Document |
| `PRD.md`            | Product Requirements Document |
| `DATA_CATALOGUE.md` | Dataset and field-level documentation |
| `ARCHITECTURE.md`   | Technical and analytical architecture |
| Methodology         | Analytical assumptions and decision framework |

---

## 📌 Key Analytical Outputs

### Infrastructure Intelligence

- Charging station distribution
- Charging infrastructure density
- Geographic charging gaps
- Potential charging-desert locations

### Demand Intelligence

- EV registration patterns
- Geographic demand concentration
- Commercial activity signals
- Demand hotspots

### Corridor Intelligence

- Highway charging coverage
- Corridor infrastructure gaps
- Potential areas requiring further investigation

### Site Selection

- Candidate location scoring
- Candidate ranking
- Decision-factor comparison
- Recommendation explainability

### Scenario Planning

- Priority-based analysis
- What-if scenarios
- Sensitivity of rankings to different planning priorities

---

## 📊 Business Value

The platform is designed to demonstrate how data can support infrastructure planning decisions.

### For EV Infrastructure Operators

Identify areas that may have:

- High demand
- Low charging coverage
- Strong commercial potential
- Better infrastructure accessibility

### For Mobility & Energy Analysts

Understand relationships between:

- EV adoption
- Charging infrastructure
- Geographic accessibility
- Highway mobility
- Electrical infrastructure

### For Decision Makers

Explore:

- Where infrastructure gaps exist
- Which candidate locations deserve attention
- Why a location ranks highly
- How recommendations change under different priorities

---

## 🔍 From Dashboard to Decision Intelligence

Traditional dashboards primarily answer:

> **What happened?**

This platform attempts to extend the analytical workflow toward:

```text
WHAT?
  ↓
EV adoption & infrastructure patterns
  ↓
WHERE?
  ↓
Geographic gaps & underserved areas
  ↓
WHY?
  ↓
Demand + infrastructure relationships
  ↓
WHERE SHOULD WE ACT?
  ↓
Candidate site prioritisation
  ↓
WHAT IF?
  ↓
Scenario simulation
```

This progression is the central idea behind the project.

---

## ⚠️ Methodology & Data Disclaimer

This project is an **analytical decision-support platform** and should not be interpreted as an official government infrastructure-planning model.

The results depend on:

- Source-data coverage
- Data freshness
- Geographic accuracy
- Data preprocessing
- Feature engineering
- Spatial assumptions
- Catchment definitions
- Decision criteria
- Weight selection

Consequently, recommended locations should be treated as **analytical candidates for further investigation**, not definitive investment or infrastructure decisions.

Final site selection would require additional validation involving factors such as:

- Land availability
- Regulatory permissions
- Grid capacity
- Electricity connection feasibility
- Traffic volumes
- Capital expenditure
- Operating costs
- Land economics
- Charger utilisation
- Local demand validation

---

## 🔐 Data & Privacy Considerations

The platform is intended to work with aggregated, public or appropriately licensed datasets.

No personally identifiable information should be used as a required input to the analytical framework.

Users should independently verify the licensing and permitted usage of external datasets before redistributing or commercially using derived datasets.

---

## 🔮 Future Improvements

Potential future enhancements include:

- [ ] Real-time charging-station availability
- [ ] Charger utilisation data
- [ ] EV traffic-flow integration
- [ ] Road-network travel-time modelling
- [ ] Charger utilisation forecasting
- [ ] Cost and ROI modelling
- [ ] Electricity tariff integration
- [ ] Grid-capacity modelling
- [ ] More granular mobility data
- [ ] Automated data-refresh pipelines
- [ ] API layer for external applications
- [ ] Historical backtesting of recommendations
- [ ] Advanced optimisation-based site selection
- [ ] Weather and seasonal demand modelling
- [ ] Charging-station capacity optimisation

---

## 👨‍💻 Why I Built This

This project was built to explore how **data analytics can move beyond dashboards and descriptive reporting into decision intelligence.**

The objective was to combine:

**Data Engineering**

→ **Spatial Analytics**

→ **Demand Analysis**

→ **Decision Modelling**

→ **Explainability**

→ **Interactive Business Intelligence**

into one end-to-end platform.

The broader objective is to demonstrate how analytics can help answer not only:

> **What is happening?**

but also:

> **Where is the problem?**

> **Why is it happening?**

> **Where should we act?**

> **What happens if our priorities change?**

---

## ⭐ Project Highlights

| Area                  | Highlight |
| --------------------- | ------------------------------------------------------ |
| 📊 Data               | 130K+ multi-domain records |
| 🖥️ Application       | Interactive Streamlit platform |
| 📑 Modules            | 9 analytical modules |
| 🗺️ Spatial Analytics | Geographic infrastructure analysis |
| 🌵 Gap Detection      | Charging-desert analysis |
| 🛣️ Mobility          | Highway corridor analysis |
| 🎯 Decision Support   | MCDA-based candidate evaluation |
| 🔍 Explainability     | Factor-level recommendation insights |
| 🎛️ Simulation        | What-if scenario analysis |
| 🔄 Engineering        | Data validation + ETL workflow |
| 📚 Documentation      | Business, product, data and methodology documentation |

---

## 🏆 What Makes This Project Different

This project is not designed as a conventional data-visualisation dashboard.

It combines multiple layers of analytical work:

```text
                    ┌───────────────────┐
                    │     RAW DATA      │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │   DATA ENGINEERING│
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ SPATIAL ANALYTICS │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ DEMAND ANALYTICS  │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ GAP IDENTIFICATION│
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ DECISION MODELLING│
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ RECOMMENDATIONS   │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ SCENARIO ANALYSIS │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ INTERACTIVE APP   │
                    └───────────────────┘
```

The goal is therefore not simply to **visualise EV data**, but to demonstrate an end-to-end approach to **data-driven infrastructure decision support**.

---

## 🔗 Project Links

### 🚀 Live Dashboard

**[Launch the EV Charging Intelligence Platform](https://chargedesert.streamlit.app/)**

### 💻 GitHub Repository

**[View the Source Code](https://github.com/koushikgarg11/EV)**

---

## 📬 Feedback & Contributions

Suggestions, feedback and improvements are welcome.

If you identify an issue with:

- Data processing
- Spatial analysis
- Recommendation logic
- Application behaviour
- Documentation

please open an issue in the GitHub repository.

---

<p align="center">
  <b>⚡ Built with Python • Streamlit • GIS • Data Analytics • Decision Intelligence</b>
</p>

<p align="center">
  <a href="https://chargedesert.streamlit.app/">
    <b>🚀 Explore the Live Platform</b>
  </a>
</p>
