# RESEARCH QUESTIONS & INVESTIGATIVE FRAMEWORK

**Project**: The 311 Response Gap: Can We Predict Which Public Complaints Will Take Too Long to Resolve?  
**Platform**: Avaloka AI Data Intelligence Engine

---

## Overview

This investigation is organized into five core descriptive/inferential analytical themes (Themes A through E) and one primary predictive machine learning inquiry. Each theme defines the exact operational question, underlying hypotheses, mathematical metric definitions, confounding variables, and the corresponding natural language prompt designed for Avaloka.

---

## Theme A: Overall Municipal Service Performance

### Core Questions
1. What is the overall distribution of resolution duration across New York City? What are the median, interquartile range (IQR), and 90th/99th percentiles?
2. What percentage of 311 complaints exceed a 7-day resolution window?
3. What percentage of complaints represent extreme delays exceeding 30 days?
4. How do resolution metrics fluctuate month-over-month across 2024 and 2025?

### Hypotheses
- $H_{A1}$: NYC 311 resolution duration exhibits an extreme right-skewed log-normal or Pareto-like distribution, where the arithmetic mean is heavily distorted by extreme outliers, necessitating median and non-parametric metric reporting.
- $H_{A2}$: Between 15% and 25% of all complaints exceed 7 calendar days, with a small tail (< 5%) exceeding 30 days.

### Metric Definitions
- **Resolution Duration ($\Delta t$)**:
  $$\Delta t = \text{closed\_date} - \text{created\_date} \quad (\text{expressed in decimal days})$$
- **7-Day Delay Rate ($R_{7d}$)**:
  $$R_{7d} = \frac{\sum_{i=1}^N \mathbb{I}(\Delta t_i > 7.0)}{N} \times 100\%$$
- **30-Day Delay Rate ($R_{30d}$)**:
  $$R_{30d} = \frac{\sum_{i=1}^N \mathbb{I}(\Delta t_i > 30.0)}{N} \times 100\%$$

### Confounding Factors to Control
- **Same-Day Rapid Closures**: Automated or immediate administrative closures (e.g., NYPD closing a parking complaint within 15 minutes as "unfounded") can suppress median resolution figures.
- **Weekend / Holiday Distortions**: Non-emergency agencies (e.g., DOB, DEP) operating on business hours accumulate artificial delay over weekends.

### Avaloka Prompt Formulation
> *"Calculate the overall distribution of resolution duration in days for our dataset. Provide the median, 25th, 75th, 90th, and 99th percentiles, as well as the exact percentage of cases taking > 7 days and > 30 days. Break this down by calendar month to show the temporal trend."*

---

## Theme B: Agency-Level Operational Bottlenecks

### Core Questions
1. Which municipal agencies receive the highest volume of public complaints?
2. Which agencies exhibit the longest median resolution durations?
3. Is intake volume negatively correlated with resolution efficiency (i.e., are high-volume agencies structurally slower, or do they possess superior triaging automation)?
4. Which agencies have the highest proportion of requests breaching the 7-day threshold?

### Hypotheses
- $H_{B1}$: Enforcement-heavy agencies (NYPD, DSNY) resolve complaints rapidly (median < 24–48 hours) due to localized mobile dispatch, despite handling the highest aggregate volumes.
- $H_{B2}$: Inspection- and adjudication-intensive agencies (HPD, DOB, DEP, DOT) exhibit significantly higher median durations (> 5–10 days) and higher 7-day delay rates due to legal notice requirements, physical inspection protocols, and property owner cure periods.
- $H_{B3}$: Complaint volume alone does *not* explain resolution delay; agency operational workflows and statutory mandates dominate resolution velocity.

### Confounding Factors to Control
- **Statutory Workflow Differences**: Comparing NYPD noise complaints to HPD lead paint inspections without noting statutory differences creates a false equivalence.
- **Batch Closures**: Periodic administrative cleanups where hundreds of aging tickets are bulk-closed on a single day.

### Avaloka Prompt Formulation
> *"Group the complaints by Agency. For each agency, compute total complaint volume, median resolution time in days, interquartile range, and the percentage of complaints taking > 7 days. Plot a scatter plot of complaint volume versus median resolution time to evaluate whether high-volume agencies are slower."*

---

## Theme C: Complaint-Level Performance & Problem Typology

### Core Questions
1. Which specific complaint types (`complaint_type`) and sub-descriptors (`descriptor`) experience the highest median resolution times?
2. Are certain complaint types consistently delayed across all seasons and geographies?
3. Within a single agency, how does complaint complexity influence turnaround time?

### Hypotheses
- $H_{C1}$: Structural, tenant-landlord, and physical infrastructure complaints (e.g., *Heat/Hot Water*, *Lead Paint*, *Illegal Building Conversion*, *Street Condition/Pothole*) suffer higher delay rates than transitory public nuisances (e.g., *Blocked Driveway*, *Noise - Residential*).
- $H_{C2}$: High complaint frequency does not imply high delay: high-frequency complaints often benefit from streamlined municipal standard operating procedures.

### Confounding Factors to Control
- **Emergency Escalation Flags**: Emergency complaints (e.g., gas leaks, active heating outages in sub-zero weather) possess statutory fast-track SLAs that distort agency-wide averages.
- **Low-Sample Outliers**: Obscure complaint categories with fewer than 50 cases exhibiting anomalous multi-month resolution times.

### Avaloka Prompt Formulation
> *"Identify the top 15 most frequent complaint types, and separately the top 15 complaint types with the longest median resolution time (filtering for categories with at least 100 cases). Compare their 7-day delay rates and generate a comparative bar chart."*

---

## Theme D: Geographic Disparities & Borough Equity

### Core Questions
1. How do median resolution times and 7-day delay rates vary across the five boroughs (Bronx, Brooklyn, Manhattan, Queens, Staten Island)?
2. Do specific boroughs suffer disproportionate delays for identical complaint types (e.g., residential heat complaints taking longer in the Bronx vs. Manhattan)?
3. Are observed borough-level differences statistically significant, or are they an artifact of differing complaint category mixes?

### Hypotheses
- $H_{D1}$: Disparities exist across boroughs, with historically disadvantaged or higher-density boroughs (e.g., Bronx, parts of Brooklyn) exhibiting higher delay rates.
- $H_{D2}$: A substantial fraction of apparent borough disparity is driven by **Case Mix Variation** (e.g., the Bronx generating far higher proportions of complex HPD housing maintenance complaints than Staten Island).

### Confounding Factors to Control
- **Simpson’s Paradox / Case-Mix Bias**: An agency may resolve complaints at identical speeds across all boroughs, but a borough with 80% complex housing complaints will appear sluggish overall.
- **Unspecified / Cross-Borough Records**: Records labeled `"Unspecified"` borough must be isolated and evaluated for data quality anomalies.

### Avaloka Prompt Formulation
> *"Compare the resolution metrics across all five boroughs. For each borough, show total volume, median resolution days, and percentage of cases > 7 days. Then, select the top 3 shared complaint categories across the city and compare the median resolution time by borough for those specific categories to control for case mix."*

---

## Theme E: Temporal Trends & Seasonality Dynamics

### Core Questions
1. How does the volume and resolution speed of complaints fluctuate across calendar months and seasons?
2. Do municipal services experience winter or summer "service shocks" where delay rates surge citywide?
3. Does the day of week or hour of complaint submission correlate with prolonged resolution times?

### Hypotheses
- $H_{E1}$: Winter months (November–February) trigger massive surges in *Heat/Hot Water* complaints that saturate HPD inspection capacity, driving up citywide 7-day delay rates.
- $H_{E2}$: Complaints submitted on Friday afternoons or weekends experience an immediate 48-hour latency due to non-emergency agency scheduling.

### Confounding Factors to Control
- **Severe Weather Events**: Blizzards, heat waves, and torrential rainstorms cause acute localized spikes in tree damage, flooding, and power outages.

### Avaloka Prompt Formulation
> *"Analyze the monthly trend of 311 complaints across 2024 and 2025. Plot total volume and the 7-day delay rate over time. Investigate whether the hour of day or day of week at intake correlates with higher resolution delays."*

---

## Predictive Modeling Question: Early Delay Warning

### Core Question
> *"Can we predict whether a newly created 311 complaint will take more than seven days to resolve, using strictly the categorical and spatio-temporal features available at the exact moment of intake?"*

### Target Formulation
$$Y_i = \mathbb{I}(\Delta t_i > 7.0) \in \{0, 1\}$$

### Permissible Features (Intake-Time Only)
- Categorical: `agency`, `complaint_type`, `descriptor`, `borough`, `open_data_channel_type`, `location_type`.
- Spatio-temporal: `incident_zip`, `community_board`, `month_of_year`, `day_of_week`, `hour_of_day`, `is_weekend`.

### Strictly Forbidden Features (Post-Intake / Leakage)
- `closed_date`, `resolution_action_updated_date`, `resolution_description`, `status`, `due_date`, $\Delta t$.

### Avaloka Prompt Formulation (for Model Training Agent)
> *"We want to build a machine learning model to predict whether a complaint will take more than 7 days to close (delayed_over_7d). Use ONLY intake-time features: agency, complaint_type, descriptor, borough, incident_zip, submission_month, submission_day_of_week, and submission_hour. Do NOT use closed_date, status, or any resolution fields. Check for data leakage, set up a baseline model, and train a classifier."*

