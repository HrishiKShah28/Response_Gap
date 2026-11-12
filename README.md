# The 311 Response Gap: Can We Predict Which Public Complaints Will Take Too Long to Resolve?

[![Avaloka Hackathon](https://img.shields.io/badge/Avaloka-AI%20Engineering%20Internship%20Hackathon-blue.svg)](https://avaloka.ai)
[![Dataset](https://img.shields.io/badge/NYC%20OpenData-311%20Service%20Requests-green.svg)](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](LICENSE)

---

## Executive Overview

**"The 311 Response Gap"** is an empirical data science investigation designed for the **Avaloka AI Engineering Internship Hackathon** (November 13–15, 2026), hosted by **Guruvai Sciences**. 

The project investigates operational disparities across New York City municipal services using the official **NYC 311 Service Requests (2020 to Present)** dataset. Specifically, we explore which agency types, complaint categories, and geographic boroughs face systemic resolution bottlenecks, and evaluate whether an AI-assisted predictive model can reliably classify whether a newly submitted service request will experience extended delays (**> 7 days**) using *strictly* the attributes known at the instant of intake.

A central premise of this project is our **Avaloka-first methodology**: rather than treating Avaloka as a black-box or bypassing it with external scripts, Avaloka's multi-agent data intelligence platform ([avaloka.ai](https://avaloka.ai)) is the primary engine of discovery, code generation, profiling, and predictive modeling. We audit, critique, validate, and verify its generated code, intermediate calculations, auto-insights, and machine learning pipelines against rigorous statistical standards.

---

## Project Repository Structure

```
Response Gap/
├── README.md                     # Project overview, repository guide, and execution roadmap
├── PROJECT_BRIEF.md              # Background, motivation, problem statement, and hackathon objectives
├── RESEARCH_QUESTIONS.md         # Five empirical research themes and predictive hypotheses
├── DATA_SOURCE_AND_SCHEMA.md     # NYC OpenData 311 schema dictionary, field mapping, and SoQL endpoints
├── DATA_PREPARATION_PLAN.md      # Sampling, sanitization, feature engineering, and anti-leakage guards
├── ANALYSIS_PLAN.md              # Structured Avaloka prompt sequence, analytical steps, and audit checks
├── MODEL_EVALUATION_PLAN.md      # Binary classification formulation, MTA setup, baselines, and metrics
├── VALIDATION_AND_INTEGRITY.md   # Statistical integrity framework, censoring bias, and code auditing
├── HACKATHON_TIMELINE.md         # Phase-by-phase operational schedule (Nov 13 – Nov 15, 2026)
├── DEMO_SCRIPT.md                # 120-second storyboard and spoken narration for the video submission
├── AGENTS.md                     # Multi-agent architecture (Avaloka Agents vs. Research Team Roles)
│
├── data/                         # Data directory (managed during execution phase)
│   ├── raw/                      # Downloaded representative NYC 311 subset (CSV/Parquet)
│   ├── processed/                # Sanitized, leakage-free dataset for Avaloka ingestion
│   └── data_dictionary.md        # Snapshot data dictionary of final ingested dataset
│
├── prompts/                      # Complete sequence of structured prompts delivered to Avaloka
├── avaloka_artifacts/            # Exported code, execution logs, auto-insights charts, and model run IDs
├── validation_scripts/           # Independent sandboxed verification scripts (cross-checks)
└── final_report/                 # Comprehensive final deliverable report and figures
```

---

## Research Pillars

1. **Systemic Operational Disparities**: Which municipal agencies and complaint types drive extreme resolution delays, and does high intake volume inherently explain slow resolution?
2. **Geographic Equity**: Do resolution times differ significantly across the five boroughs (Bronx, Brooklyn, Manhattan, Queens, Staten Island) after controlling for agency jurisdiction and complaint mix?
3. **Temporal Dynamics**: How do seasonality, weather-related complaint surges, and submission timing influence municipal turnaround times?
4. **Intake-Time Predictive Modeling**: Can a machine learning model accurately flag high-risk delayed complaints (> 7 days) at the exact moment of ticket creation without target leakage?
5. **Human-in-the-Loop AI Auditing**: How robust are Avaloka's internal agents (Planner, Coder, Validator, Execution, Visualization, Model Training Agent) when subjected to adversarial follow-up queries and independent statistical verification?

---

## Technical & Platform Context: Avaloka 1.6+

Avaloka operates as a coordinated digital workforce of specialized data science agents:
- **Planner Agent**: Parses natural language research questions, formulates structured step-by-step analytical plans, and routes subtasks.
- **Coder Agent**: Writes Python scripts for data manipulation, statistical aggregation, and feature transformations.
- **Validator Agent**: Verifies generated code against actual schema, checks hygiene, and blocks syntax or structural flaws before execution.
- **Execution Agent**: Safely executes validated code within sandboxed runtime environments.
- **Visualization Agent**: Automatically renders interactive charts and summary cards in the *Auto Insights* interface.
- **Model Training Agent (MTA)**: Formulates predictive modeling workflows, enforces pre-training **Data Leakage Screening**, evaluates against trivial baselines, and generates Model Run IDs for inference testing.

### Operational Constraints & Ingestion Specs
- **Supported Formats**: CSV, Parquet, JSON, Excel (`.xlsx`, `.xls`).
- **File Limits**: Maximum **100 MB per file**; batch upload capped at **10 files / 200 MB total**.
- **Dataset Scope**: We extract a representative, high-integrity subset of **100,000–150,000 records** from 2024–2025 via NYC Open Data's Socrata Open Data API (SoQL), resulting in an uncompressed CSV of ~35–45 MB (well within Avaloka's 100 MB single-file ceiling).

---



## Key Empirical Findings Summary

| Operational Domain | Key Empirical Finding | Statistical Evidence |
| :--- | :--- | :--- |
| **Citywide Distribution** | Extreme right-skewness; arithmetic mean overstates typical delay by **65x**. | **Median: 0.20 days (4.9h)** vs. Mean: 13.10d. **17.56% > 7d**, **8.25% > 30d**. |
| **Volume vs. Delay** | Agency volume was **not significantly associated** with median resolution time. | **Spearman $r = -0.301$** ($p = 0.342$); Pearson on log volume $r = -0.376$. NYPD handles 49.8% volume at 0.04d median. |
| **Slowest Categories** | Forestry, health inspections, and tenant conditions dominate backlogs. | New Tree Requests: **344.2d median**; Mobile Food Vendors: **178.2d**; Unsanitary Housing: **58.3% > 7d**. |
| **Borough Equity** | **Simpson's Paradox & Case-Mix Confounding**: Disparities driven by complaint composition, not agency bias. | Multi-strata audit across 6 categories proves Bronx aggregate delay (18.7%) is driven by 35.7% HPD housing share. In Heat complaints alone, the Bronx is fastest (**1.20d** vs 1.58d Manhattan). In police enforcement, all boroughs achieve **0.00% delay**. |
| **Temporal Dynamics** | Counter-intuitive weekend effect: weekend submissions exhibit lower delay rates. | Weekend delay rate **12.55%** vs Weekday **19.29%** ($OR = 0.600, p = 7.02 \times 10^{-165}$), driven by rapid NYPD quality-of-life cases swamping the queue. |
| **Predictive Modeling** | Champion Gradient Boosted Trees captures >85% of delayed cases at intake with zero target leakage. | **ROC-AUC: 0.935**, **PR-AUC: 0.746**, **Recall: 85.4%**, **Accuracy: 86.4%** on out-of-time chronological test cohort ($N = 29,374$). |
| **Censoring Bias Audit** | Completed-case metrics represent an optimistic lower bound on real civic latency. | Auxiliary audit of 2,131 open cases shows **100.0% open > 7 days** (mean age: 142.6d), an expected artifact of the 2024 cohort observation horizon. |

---

## Avaloka Multi-Agent Collaboration Artifacts

To demonstrate full transparency and prove the platform's autonomous capabilities, the complete interaction lineage is version-controlled:
- 🤖 **[SESSION_TRANSCRIPT.md](file:///c:/Users/Hrishi/Desktop/projects/Response%20Gap/avaloka_session/SESSION_TRANSCRIPT.md)**: Full conversational trace covering Planner, Coder, Validator, Execution, Visualization, and Model Training agents.
- 💻 **[GENERATED_CODE_ARCHIVE.md](file:///c:/Users/Hrishi/Desktop/projects/Response%20Gap/avaloka_session/GENERATED_CODE_ARCHIVE.md)**: Raw Python scripts authored by Avaloka's Coder Agent extracted from the code drawer.
- 🔬 **[AVALOKA_VS_INDEPENDENT_AUDIT.md](file:///c:/Users/Hrishi/Desktop/projects/Response%20Gap/avaloka_session/AVALOKA_VS_INDEPENDENT_AUDIT.md)**: Double-blind verification audit table comparing Avaloka cloud executions against local sandboxed scripts across 27 metrics.

---

## Visualizations Generated

All figures are compiled in high-resolution in the [figures/](file:///c:/Users/Hrishi/Desktop/projects/Response%20Gap/figures/) directory:
- 📊 **Figure 1**: Resolution Duration Distribution (Log Scale, Median, P90, 7d/30d cutoffs)
- 📈 **Figure 2**: Monthly 7-Day Delay Trend & Median Turnaround across 2024
- 🔍 **Figure 3**: Agency Volume vs. Median Resolution Time Scatter Plot
- 📉 **Figure 4**: Top 15 Slowest NYC 311 Complaint Categories (Horizontal Bar Chart)
- 🗺️ **Figure 5**: Simpson's Paradox in Borough Response: Aggregate vs. Category-Controlled
- 🗓️ **Figure 6**: 168-Hour Heatmap of 7-Day Delay Risk by Day-of-Week & Intake Hour
- 🎯 **Figure 7**: Out-of-Time Receiver Operating Characteristic (ROC) & Precision-Recall (PR) Curves
- 🔲 **Figure 8**: Confusion Matrix Heatmap on Out-of-Time Test Set ($N = 29,374$)
- ⚖️ **Figure 9**: Logistic Regression Log-Odds Coefficients for Intake-Time Predictors

---


