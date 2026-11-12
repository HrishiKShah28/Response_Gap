# AVALOKA CODER AGENT GENERATED CODE ARCHIVE

**Platform**: Avaloka AI Platform (https://avaloka.ai)  
**Session ID**: `avaloka-session-311-response-gap-2024`  
**Purpose**: Full archive of Python scripts extracted from Avaloka's code drawer for independent audit and verification.

---

## Code Block 1: Ingestion & Datetime Profiling
*Extracted from Prompt 1 Code Drawer:*
```python
import pandas as pd
import numpy as np

# Ingest analytical dataset
df = pd.read_csv('nyc_311_analytical_full.csv', low_memory=False)

# Convert floating timestamps to datetime with error coercion
df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

# Audit missingness and duplicates
null_summary = df.isna().mean() * 100
dup_keys = df['unique_key'].duplicated().sum()

print(f"Total Rows: {len(df):,d}")
print(f"Duplicate Keys: {dup_keys}")
print("Null Percentages:\n", null_summary[null_summary > 0])
```

---

## Code Block 2: Resolution Duration & Quantiles
*Extracted from Prompt 2 Code Drawer:*
```python
import pandas as pd
import numpy as np

# Calculate resolution duration in decimal days
df['resolution_time_days'] = (df['closed_date'] - df['created_date']).dt.total_seconds() / 86400.0

# Exclude anomalous negative durations
valid_df = df[df['resolution_time_days'] >= 0].copy()

# Compute non-parametric quantiles
stats_dict = {
    'sample_size': len(valid_df),
    'mean_days': valid_df['resolution_time_days'].mean(),
    'std_days': valid_df['resolution_time_days'].std(),
    'p25_days': valid_df['resolution_time_days'].quantile(0.25),
    'median_days': valid_df['resolution_time_days'].median(),
    'p75_days': valid_df['resolution_time_days'].quantile(0.75),
    'p90_days': valid_df['resolution_time_days'].quantile(0.90),
    'p99_days': valid_df['resolution_time_days'].quantile(0.99),
    'delay_7d_pct': (valid_df['resolution_time_days'] > 7.0).mean() * 100,
    'delay_30d_pct': (valid_df['resolution_time_days'] > 30.0).mean() * 100
}
```

---

## Code Block 3: Agency Operational Benchmarks
*Extracted from Prompt 3 Code Drawer:*
```python
import pandas as pd
import numpy as np
from scipy import stats

# Group by agency and compute robust summary metrics
agency_benchmarks = valid_df.groupby(['agency', 'agency_name']).agg(
    total_complaints=('unique_key', 'count'),
    median_resolution_days=('resolution_time_days', 'median'),
    p25_days=('resolution_time_days', lambda x: np.percentile(x, 25)),
    p75_days=('resolution_time_days', lambda x: np.percentile(x, 75)),
    pct_delayed_over_7d=('resolution_time_days', lambda x: (x > 7.0).mean() * 100)
).reset_index()

# Filter for agencies with at least 100 cases
major_agencies = agency_benchmarks[agency_benchmarks['total_complaints'] >= 100]

# Correlation between volume and median turnaround
spearman_r, spearman_p = stats.spearmanr(major_agencies['total_complaints'], major_agencies['median_resolution_days'])
```

---

## Code Block 4: Controlled Category Stratification (Simpson's Paradox)
*Extracted from Prompt 5 Follow-Up Code Drawer:*
```python
import pandas as pd
import numpy as np

# Controlled Category 1: HEAT/HOT WATER (HPD)
heat_cases = valid_df[(valid_df['complaint_type'] == 'HEAT/HOT WATER') & (valid_df['borough'] != 'UNSPECIFIED')]
heat_by_borough = heat_cases.groupby('borough').agg(
    cases=('unique_key', 'count'),
    median_days=('resolution_time_days', 'median'),
    pct_over_7d=('resolution_time_days', lambda x: (x > 7.0).mean() * 100)
).reset_index()

# Controlled Category 2: Illegal Parking (NYPD)
parking_cases = valid_df[(valid_df['complaint_type'] == 'Illegal Parking') & (valid_df['borough'] != 'UNSPECIFIED')]
parking_by_borough = parking_cases.groupby('borough').agg(
    cases=('unique_key', 'count'),
    median_days=('resolution_time_days', 'median'),
    pct_over_7d=('resolution_time_days', lambda x: (x > 7.0).mean() * 100)
).reset_index()
```

---

## Code Block 5: Model Training Pipeline (Model Training Agent)
*Extracted from Model Training Agent Execution Log:*
```python
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import roc_auc_score, average_precision_score, recall_score, precision_score, confusion_matrix

# Strict chronological split
train_data = df[df['created_month'] <= 9]
test_data = df[df['created_month'] >= 10]

features_cat = ['agency', 'complaint_type', 'descriptor_clean', 'borough', 'location_type', 'open_data_channel_type']
features_num = ['created_dow', 'created_hour', 'is_weekend', 'is_business_hours']

X_train = train_data[features_cat + features_num]
y_train = train_data['delayed_over_7d'].values

X_test = test_data[features_cat + features_num]
y_test = test_data['delayed_over_7d'].values

# Preprocessor & Model
prep = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), features_cat),
        ('num', 'passthrough', features_num)
    ]
)
X_train_trans = prep.fit_transform(X_train)
X_test_trans = prep.transform(X_test)

# Class weight balancing
sample_weight = np.where(y_train == 1, (len(y_train) - y_train.sum()) / y_train.sum(), 1.0)

mta_model = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
mta_model.fit(X_train_trans, y_train, sample_weight=sample_weight)

# Evaluation
y_prob = mta_model.predict_proba(X_test_trans)[:, 1]
y_pred = (y_prob >= 0.5).astype(int)

roc_auc = roc_auc_score(y_test, y_prob)
pr_auc = average_precision_score(y_test, y_prob)
recall = recall_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
```
