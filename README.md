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

## Hackathon Deliverables

As stipulated by Guruvai Sciences, this project delivers:
1. **Public / Shareable Avaloka Report Link**: The live interactive analytical session and model artifact within the Avaloka cloud platform.
2. **2-Minute Screen Recording**: High-impact demonstration of the real-world inquiry, Avaloka dataset profiling, agent code generation, model training, critical verification of an AI finding, and final takeaways (following `DEMO_SCRIPT.md`).
3. **Evidence-Backed Final Analytical Report**: A publishable, peer-grade research document combining Avaloka's findings with rigorous independent validation.
4. **Complete Reproducibility Package**: All sanitized data scripts, exact prompt trajectories, exported Python code snippets, and audit logs.

---

## Project Status

- [x] Phase 0: Project Initiation, Documentation Review, and Architecture Planning
- [ ] Phase 1: Representative Data Acquisition & Schema Profiling
- [ ] Phase 2: Avaloka Ingestion, Auto-Profiling & Exploratory Analysis
- [ ] Phase 3: In-Depth Categorical, Agency & Geographic Investigations
- [ ] Phase 4: Predictive Modeling with Avaloka Model Training Agent (MTA)
- [ ] Phase 5: Independent Verification, Code Auditing & Integrity Checks
- [ ] Phase 6: Final Analytical Report Compilation & Executive Artifact Creation
- [ ] Phase 7: Demo Video Recording, Public Link Validation & Form Submission

> [!IMPORTANT]
> **No analysis has been performed yet.** This repository is currently in the foundational planning phase. Execution begins following formal review and approval of the planning suite.

