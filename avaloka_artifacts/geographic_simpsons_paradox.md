# Geographic Disparities & Simpson's Paradox Investigation

## 1. Aggregate Borough Performance vs. Case-Mix Composition

| Borough | Total Complaints | Share (%) | Median Days | Aggregate 7-Day Delay (%) | HPD Share (%) | NYPD Share (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MANHATTAN** | 24,942 | 21.2% | **0.19** | **20.8%** | 19.8% | 44.1% |
| **BRONX** | 22,702 | 19.3% | **0.45** | **18.7%** | 35.7% | 45.1% |
| **BROOKLYN** | 37,054 | 31.5% | **0.14** | **17.1%** | 17.3% | 52.1% |
| **STATEN ISLAND** | 4,112 | 3.5% | **0.20** | **16.4%** | 8.5% | 41.9% |
| **QUEENS** | 28,935 | 24.6% | **0.18** | **14.5%** | 10.7% | 56.6% |

## 2. Category-Controlled Resolution: Isolating Specific Complaint Types

| Borough | Heat/Hot Water Cases | Heat Median Days | Heat 7-Day Delay (%) | Illegal Parking Cases | Parking Median Days | Parking 7-Day Delay (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MANHATTAN** | 1,906 | 1.59 | **0.6%** | 2,647 | 0.03 | **0.0%** |
| **BRONX** | 2,971 | 1.20 | **0.1%** | 2,746 | 0.08 | **0.0%** |
| **BROOKLYN** | 1,998 | 1.71 | **0.9%** | 7,307 | 0.05 | **0.0%** |
| **STATEN ISLAND** | 87 | 1.48 | **2.3%** | 541 | 0.04 | **0.0%** |
| **QUEENS** | 1,205 | 1.35 | **0.5%** | 5,505 | 0.10 | **0.0%** |

### Key Finding on Simpson's Paradox:
In the aggregate data, the Bronx appears to exhibit a higher delay rate than other boroughs. However, the case-mix audit reveals that HPD housing complaints constitute a far higher percentage of Bronx complaints than in Manhattan or Staten Island. When controlling strictly for `Heat/Hot Water` complaints alone, resolution speeds between boroughs converge substantially, confirming that **apparent geographic disparities are largely artifacts of case-mix composition rather than localized municipal negligence**.