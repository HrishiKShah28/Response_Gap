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

### 2. The Volume Paradox: Volume Does Not Drive Delay
- High intake volume does *not* explain slow turnaround.
- **NYPD** receives the single largest share of complaints (~42%) yet maintains one of the fastest median resolution times (**< 4 hours**), driven by localized mobile patrol dispatch and standard operating procedures.
- Conversely, **HPD** (Housing Preservation & Development) and **DOB** (Buildings) handle lower volumes but face the largest median resolution times (**5.8 to 12.4 days**) and the highest 7-day delay rates (**38% to 62%**).
- Spearman rank correlation between agency complaint volume and median resolution duration is **$r = -0.18$ ($p = 0.54$)**, empirically rejecting the hypothesis that high-volume agencies are structurally slower.

### 3. Simpson's Paradox in Borough Equity
- In aggregate data, the **Bronx** appears to suffer the longest delays, with a raw 7-day delay rate of **24.2%**, compared to **16.8% in Manhattan** and **18.1% in Queens**.
- However, our adversarial follow-up revealed severe **Case-Mix Confounding**: HPD housing maintenance complaints make up over 48% of all Bronx complaints, compared to under 22% in Manhattan.
- When controlling for complaint category (e.g., evaluating *Heat/Hot Water* complaints alone across all five boroughs), the borough delay rates converge to within **$\pm 2.1\%$**, confirming **Simpson's Paradox**. Apparent geographic disparities reflect differences in neighborhood housing stock and socioeconomic complaint types, not geographic favoritism by city agencies.

### 4. The Weekend Latency Penalty
- Complaints submitted on Saturday or Sunday experience an immediate administrative delay ($OR = 1.34$, Fisher's exact $p < 10^{-10}$) compared to Tuesday/Wednesday submissions.
- Because non-emergency municipal depots (DEP, DOB, DOT) operate on standard business hours, complaints logged over weekends accumulate 48 hours of initial latency before case triage begins.

### 5. Intake-Time Predictive Early Warning
- Using Avaloka's **Model Training Agent (MTA)**, we trained a binary classifier to predict 7-day delays ($\text{delayed} > 7\text{d}$) using strictly intake-time features (agency, complaint type, descriptor, borough, ZIP code, channel, submission hour/day/month).
- Evaluated on a strict **out-of-time chronological test set** (Oct–Dec 2024), the champion Gradient Boosted model achieves:
  - **ROC-AUC**: **0.834**
  - **PR-AUC**: **0.582** (vs. 0.194 baseline prevalence)
  - **Recall on Delayed Cases**: **76.8%**
  - **Overall Accuracy**: **81.4%**
- Naive majority-class baselines achieve 80% accuracy by ignoring all delayed cases (0% recall). Our model provides actionable early warning, capturing over 3 out of every 4 delayed complaints at the exact moment of intake.

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
