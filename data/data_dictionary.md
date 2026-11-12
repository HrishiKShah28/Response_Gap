# NYC 311 TELEMETRY DATA DICTIONARY & HYGIENE AUDIT

**Observation Period**: Calendar Year 2024 (Stratified Sample: 12 months)
**Total Raw Telemetry Ingested**: 119,967 records
**Censored / Unclosed Cases Isolated**: 2,131 records (1.78%)
**Completed Cases with closed_date**: 117,869 records (98.22%)
**Negative Duration Anomalies Dropped**: 33 records (0.028%)
**Valid Completed Cases Analyzed**: 117,836 records (98.19%)

### Dataset Accounting Waterfall:
```
Total Telemetry Ingested: 119,967 records
   │
   ├── Unresolved / Open Cases (1.78%): 2,131 records
   │   └── Isolated to `open_cases_censored.csv` (100.0% open > 7d; mean age: 142.6d)
   │
   └── Completed Cases (98.22%): 117,869 records
           │
           ├── Negative Duration Errors (0.028%): 33 records (Dropped)
           │
           └── Valid Analytical Completed Cohort: 117,836 records
                   ├── Chronological Train Split (Jan–Sep 2024): 88,462 records
                   └── Chronological Out-of-Time Test Split (Oct–Dec 2024): 29,374 records
```

---

## 1. Headline Empirical Summary Statistics

- **Median Resolution Time**: 0.20 decimal days (4.9 hours)
- **Interquartile Range (IQR)**: 0.03 days (25th percentile) to 2.94 days (75th percentile)
- **7-Day Delay Rate ($R_{7d}$)**: 17.56% of completed complaints exceed 7 days
- **30-Day Extreme Delay Rate ($R_{30d}$)**: 8.25% of completed complaints exceed 30 days
- **Unclosed Ticket Delay Rate**: 100.0% of open cases have been unresolved for > 7 days

---

## 2. Dataset Field Specification

| Column Name | Data Type | Null % | Description | Modeling Role & Leakage Status |
| :--- | :--- | :--- | :--- | :--- |
| `unique_key` | Integer | 0.0% | Unique service request identifier | Primary Key (Excluded from features) |
| `created_date` | Datetime | 0.0% | Citizen ticket creation timestamp | Intake temporal index |
| `closed_date` | Datetime | 0.0% | Agency ticket closure timestamp | 🔴 High Leakage (Used solely for duration calculation) |
| `agency` | String | 0.0% | Responding city agency acronym | 🟢 Safe Intake Feature (Key predictor) |
| `agency_name` | String | 0.0% | Full name of responding agency | 🟢 Safe (Redundant with agency) |
| `complaint_type` | String | 0.0% | Broad problem category | 🟢 Safe Intake Feature (Key predictor) |
| `descriptor` | String | 0.00% | Granular sub-complaint detail | 🟢 Safe Intake Feature |
| `location_type` | String | 0.00% | Physical site category | 🟢 Safe Intake Feature |
| `incident_zip` | String | 0.63% | 5-digit USPS postal code | 🟢 Safe Intake Feature |
| `borough` | String | 0.08% | NYC borough name | 🟢 Safe Intake Feature |
| `open_data_channel_type` | String | 0.0% | Intake mechanism (PHONE, ONLINE, etc.) | 🟢 Safe Intake Feature |
| `status` | String | 0.0% | Ticket lifecycle state | 🔴 High Leakage (Excluded) |
| `resolution_description` | String | 1.21% | Agency closure narrative | 🔴 High Leakage (Excluded) |
| `resolution_time_days` | Float | 0.0% | Exact resolution duration in decimal days | 🔴 Continuous Target (Excluded from features) |
| `delayed_over_7d` | Integer | 0.0% | Binary classification target (1 if >7d, else 0) | 🎯 Primary Prediction Target |
| `delayed_over_30d` | Integer | 0.0% | Secondary extreme-delay flag | 🔴 Target (Excluded from features) |
| `created_month` | Integer | 0.0% | Month of submission (1-12) | 🟢 Safe Intake Feature (Seasonality) |
| `created_dow` | Integer | 0.0% | Day of week of submission (0=Mon, 6=Sun) | 🟢 Safe Intake Feature (Weekly cadence) |
| `created_hour` | Integer | 0.0% | Hour of submission (0-23) | 🟢 Safe Intake Feature (Diurnal cycle) |
| `is_weekend` | Integer | 0.0% | Flag for Saturday/Sunday submission | 🟢 Safe Intake Feature |
| `is_business_hours` | Integer | 0.0% | Flag for Mon-Fri 08:00-18:00 submission | 🟢 Safe Intake Feature |

---

## 3. Top Responding Agencies by Volume

| Agency | Full Name | Count | Share (%) | Median Duration (Days) | 7-Day Delay Rate (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NYPD** | New York City Police Department | 58,662 | 49.8% | 0.04 | 0.0% |
| **HPD** | Department of Housing Preservation and Development | 22,929 | 19.5% | 3.47 | 36.7% |
| **DSNY** | Department of Sanitation | 9,758 | 8.3% | 1.28 | 14.2% |
| **DOT** | Department of Transportation | 6,261 | 5.3% | 2.39 | 27.4% |
| **DEP** | Department of Environmental Protection | 6,255 | 5.3% | 1.06 | 19.6% |
| **DPR** | Department of Parks and Recreation | 4,123 | 3.5% | 25.35 | 64.0% |
| **DOB** | Department of Buildings | 3,115 | 2.6% | 19.70 | 60.1% |
| **DOHMH** | Department of Health and Mental Hygiene | 2,971 | 2.5% | 0.87 | 36.1% |
| **TLC** | Taxi and Limousine Commission | 1,131 | 1.0% | 69.24 | 80.4% |
| **EDC** | Economic Development Corporation | 1,085 | 0.9% | 18.75 | 94.8% |

---

## 4. Top Complaint Types by Volume

| Complaint Type | Primary Agency | Count | Share (%) | Median Duration (Days) | 7-Day Delay Rate (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Illegal Parking** | NYPD | 18,748 | 15.9% | 0.06 | 0.0% |
| **Noise - Residential** | NYPD | 13,820 | 11.7% | 0.03 | 0.0% |
| **HEAT/HOT WATER** | HPD | 8,141 | 6.9% | 1.41 | 0.2% |
| **Noise - Street/Sidewalk** | NYPD | 7,083 | 6.0% | 0.03 | 0.0% |
| **Blocked Driveway** | NYPD | 6,183 | 5.2% | 0.07 | 0.0% |
| **UNSANITARY CONDITION** | HPD | 3,918 | 3.3% | 8.26 | 58.3% |
| **Noise - Commercial** | NYPD | 3,135 | 2.7% | 0.03 | 0.0% |
| **Abandoned Vehicle** | NYPD | 2,548 | 2.2% | 0.08 | 0.0% |
| **PLUMBING** | HPD | 2,021 | 1.7% | 7.26 | 51.8% |
| **Water System** | DEP | 2,013 | 1.7% | 0.11 | 11.4% |

---

## 5. Borough Breakdown & Disparity Preview

| Borough | Count | Share (%) | Median Duration (Days) | 7-Day Delay Rate (%) |
| :--- | :--- | :--- | :--- | :--- |
| **BROOKLYN** | 37,054 | 31.4% | 0.14 | 17.1% |
| **QUEENS** | 28,935 | 24.6% | 0.18 | 14.5% |
| **MANHATTAN** | 24,942 | 21.2% | 0.19 | 20.8% |
| **BRONX** | 22,702 | 19.3% | 0.45 | 18.7% |
| **STATEN ISLAND** | 4,112 | 3.5% | 0.20 | 16.4% |
| **UNSPECIFIED** | 91 | 0.1% | 3.27 | 33.0% |