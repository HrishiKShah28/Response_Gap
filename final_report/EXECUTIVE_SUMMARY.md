# EXECUTIVE SUMMARY: THE 311 RESPONSE GAP

**Project**: The 311 Response Gap: Can We Predict Which Public Complaints Will Take Too Long to Resolve?  
**Event**: Avaloka AI Engineering Internship Hackathon (Nov 13–15, 2026)  
**Organizers**: Guruvai Sciences (Indu Ganti)  
**Platform Evaluated**: Avaloka AI (https://avaloka.ai)

---

## 1. The Municipal Challenge: The "Response Gap"

Every day, thousands of New Yorkers report civic issues to the city's 311 hotline, ranging from blocked driveways and loud street parties to freezing apartments without heat and hazardous structural building cracks. While municipal dashboards frequently boast rapid citywide average response times, citizen lived experience often diverges sharply: while an illegal parking violation is routinely addressed by the NYPD in under three hours, a residential heating outage or lead paint inspection managed by HPD or DOB often takes weeks or months to resolve.

This operational divergence constitutes the **"Response Gap"**—a systemic variance in turnaround velocity driven by agency mandates, case complexity, and administrative latency. This hackathon project partnered with **Avaloka** to answer a vital public policy question:

> *"Which types of public service complaints, agencies, and boroughs experience the longest resolution delays in New York City, and can we predict whether a newly submitted complaint will take more than seven days to resolve using only information available when it is submitted?"*

---

## 2. Core Empirical Findings

Across a representative, 12-month stratified cohort of **115,000+ completed service requests** from Calendar Year 2024 (with an auxiliary audit of **8,000+ unresolved open cases**), our investigation yielded five fundamental insights:

### 1. Extreme Skewness Dominates Municipal Turnaround
- Citywide resolution time exhibits an extreme right-skewed distribution where the arithmetic mean (**8.6 days**) is heavily distorted by extreme outliers.
- The **median resolution time is 2.8 days** ($IQR = 0.3 \text{ to } 6.4 \text{ days}$), yet **19.4% of all complaints exceed 7 calendar days**, and **4.2% exceed 30 calendar days**.
- Reporting arithmetic means in civic dashboards creates a misleading impression of agency performance.

### 2. Agency Volume vs. Turnaround Velocity
- Agency-level complaint volume was **not significantly associated with median resolution time** in this observational sample (**Spearman $r = -0.301$, $p = 0.342$**; Pearson on log volume $r = -0.376$, $p = 0.228$).
- **NYPD** receives the single largest share of complaints (49.8%) yet achieves the fastest median resolution time (**0.04 days / under 1 hour**), driven by localized mobile dispatch and rapid enforcement protocols.
- Conversely, lower-volume agencies like **HPD** (Housing, median 3.47d, 36.7% delayed), **DOB** (Buildings, median 19.70d, 60.1% delayed), and **DPR** (Parks, median 25.35d, 64.0% delayed) exhibit prolonged durations governed by statutory inspection notice and cure requirements.

### 3. Case-Mix Confounding & Simpson's Paradox in Borough Equity
- In raw aggregate comparisons, **Manhattan (20.84%)** and the **Bronx (18.74%)** exhibit higher 7-day delay rates than Queens (14.50%) and Staten Island (16.42%).
- However, our multi-strata audit across 6 core municipal categories proved this is driven by **Case-Mix Confounding**: HPD housing maintenance complaints make up **35.7% of all Bronx inquiries**, compared to only **10.7% in Queens**.
- When evaluating *Heat/Hot Water* complaints ($N = 8,141$), a classic rank reversal occurs: the **Bronx achieves the fastest median turnaround (1.20 days)** compared to 1.58 days in Manhattan and 1.70 days in Brooklyn. For routine police enforcement (parking, noise, driveways), turnaround times uniformly converge to under 2 hours (0.00% 7-day delays) across all five boroughs.

### 4. The Weekend Intake Phenomenon
- Counter-intuitively, complaints filed on weekends exhibit a *lower* 7-day delay rate (12.55%) than weekdays (19.29%, $OR = 0.600$, $p = 7.02 \times 10^{-165}$).
- This compositional shift occurs because weekend volume is heavily dominated by rapid NYPD quality-of-life enforcement (parties, street noise, blocked driveways) that swarms the queue and dilutes slower administrative cases.

### 5. Intake-Time Predictive Early Warning
- Collaborating with Avaloka's **Model Training Agent (MTA)**, we trained a binary classifier to predict 7-day delays using zero post-intake leakage.
- Evaluated on a strict **out-of-time chronological test set** (Oct–Dec 2024, $N = 29,374$), the champion Gradient Boosted Trees model achieves:
  - **ROC-AUC**: **0.935**
  - **PR-AUC**: **0.746** (vs. 0.174 prevalence baseline)
  - **Recall on Delayed Cases**: **85.4%** (capturing 4,361 out of 5,104 delayed cases)
  - **Overall Accuracy**: **86.4%** (vs. 82.6% naive majority baseline)
- Naive majority-class baselines achieve 82.6% accuracy by ignoring all delayed cases (0% recall). Our model provides actionable early warning, capturing >85% of delayed complaints at intake.

### 6. Survivor / Right-Censoring Bias Audit
- From 119,967 initially ingested records, exactly **2,131 records (1.78%)** were unresolved.
- An auxiliary audit revealed that **100.0% of these open cases have been unresolved for $> 7$ days** (mean age: 142.6 days). Because this cohort was drawn from Calendar Year 2024 evaluated in early 2025 (minimum 60 days elapsed), surviving open tickets have necessarily languished, illustrating classical right-censoring in municipal completed-case metrics.

---

## 3. Avaloka Platform Evaluation & Multi-Agent Collaboration

This project adhered strictly to an **Avaloka-First Methodology**:
- **Planner Agent**: Effectively decomposed broad civic inquiries into logical execution graphs, distinguishing between categorical groupings, temporal distributions, and modeling requests.
- **Coder & Validator Agents**: Generated robust, vectorized Python code utilizing non-parametric medians and percentiles, properly handling datetime parsing with `errors='coerce'` and zero data mutation.
- **Visualization Agent**: Automatically rendered informative, publication-grade interactive charts in the *Auto Insights* pane, facilitating rapid hypothesis generation.
- **Model Training Agent (MTA)**: Enforced strict pre-training **Data Leakage Screening**, proactively screening and rejecting post-intake fields (`closed_date`, `status`, `resolution_description`), preventing artificial 99% accuracy traps.
- **Human-in-the-Loop Peer Auditing**: We demonstrated critical data science by challenging Avaloka on aggregate borough disparities, prompting the category-controlled cross-tabulation that uncovered Simpson's Paradox.

---

## 4. Municipal Policy & Operational Recommendations

1. **Intake-Time Triage Flags**: Integrate the Avaloka-trained prediction model into the NYC 311 intake CRM. High-risk complaints ($p > 0.35$) should be immediately routed with an *"Early Delay Warning"* badge to agency dispatchers.
2. **Dynamic Citizen SLA Expectations**: Replace static SLA estimates with dynamic, intake-modeled resolution ranges (e.g., *"Based on historical data for heating complaints in this building class, typical resolution is 5–9 days"*), managing expectations and reducing repeat calls.
3. **Survivor Bias Transparency**: Municipal open data portals must publish elapsed duration metrics for open/pending tickets alongside completed-case statistics to prevent misleadingly optimistic performance claims.

