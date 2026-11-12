# DATA SOURCE & SCHEMA SPECIFICATION

**Dataset**: NYC 311 Service Requests (2020 to Present)  
**Catalog Identifier**: `erm2-nwe9`  
**Publisher**: City of New York / Office of Technology and Innovation (OTI)  
**Portal**: [NYC Open Data (data.cityofnewyork.us)](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)  

---

## 1. Official Data Source & Access Infrastructure

The NYC 311 system logs municipal non-emergency inquiries submitted via phone (311), web portal (nyc.gov/311), mobile application, and text message. The open data feed is updated daily and maintains historical records from January 1, 2020, to the present.

### Primary Access Endpoints
- **SoQL API Endpoint (JSON)**:  
  `https://data.cityofnewyork.us/resource/erm2-nwe9.json`
- **SoQL API Endpoint (CSV)**:  
  `https://data.cityofnewyork.us/resource/erm2-nwe9.csv`
- **Dataset Metadata Schema Endpoint**:  
  `https://data.cityofnewyork.us/api/views/erm2-nwe9/columns.json`
- **Web UI Exploration**:  
  `https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9`

### Query Strategy (Socrata Open Data API - SoQL)
To avoid downloading the entire 23-million-record database, queries utilize Socrata Open Data API parameters:
- `$select`: Restricts payloads to strictly needed analytical columns.
- `$where`: Filters records to the specified temporal window (e.g., `created_date >= '2024-01-01T00:00:00.000'` and `closed_date IS NOT NULL`).
- `$order`: Chronological ordering (`created_date ASC` or `unique_key ASC`).
- `$limit`: Bounded pagination (e.g., chunks of 50,000 up to target 120,000 records).

---

## 2. Complete Field Dictionary & Leakage Risk Assessment

The official schema contains 44 native fields. Below is a comprehensive audit of each primary field, its raw data type, observed missingness expectations, analytical utility, and its **Target Leakage Risk** for our predictive model.

### Target Leakage Risk Categorization:
- 🔴 **HIGH LEAKAGE (FORBIDDEN)**: Information generated *after* complaint intake or directly revealing resolution duration/status. Must be excluded from all predictive feature matrices.
- 🟡 **MODERATE LEAKAGE RISK (RESTRICTED)**: Fields that might be modified during case lifecycle; requires strict intake-time verification.
- 🟢 **SAFE (INTAKE-TIME FEATURE)**: Attributes established at the exact moment of citizen submission.

---

### Group 1: Identifiers & Timestamps

| Field Name | Raw Type | Missingness Expectation | Description & Analytical Role | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- |
| `unique_key` | Text / Integer | 0% (Primary Key) | Unique integer identifier per service request. Used for record deduplication and audit tracking. | 🟢 Safe (Excluded as non-predictive ID) |
| `created_date` | Floating Timestamp | 0% | Date and time the request was initiated by citizen. Used for temporal indexing and duration calculation. | 🟢 Safe (Decomposed into Month, DOW, Hour) |
| `closed_date` | Floating Timestamp | ~5–12% in raw feed | Date and time the agency marked the case closed. Used exclusively to compute the ground-truth target. | 🔴 **HIGH LEAKAGE (FORBIDDEN)** |
| `due_date` | Floating Timestamp | ~60–80% | Projected SLA resolution deadline assigned by agency rules. May be populated dynamically after intake. | 🔴 **HIGH LEAKAGE (FORBIDDEN)** |
| `resolution_action_updated_date`| Floating Timestamp | ~10–25% | Timestamp when agency last logged an operational update. Indicates post-creation activity. | 🔴 **HIGH LEAKAGE (FORBIDDEN)** |

---

### Group 2: Agency & Problem Classification

| Field Name | Raw Type | Missingness Expectation | Description & Analytical Role | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- |
| `agency` | Text (Categorical) | 0% | Responding city agency acronym (e.g., NYPD, HPD, DSNY, DOT, DOB, DEP, DPR, DOHMH). Core feature. | 🟢 **SAFE (Key Feature)** |
| `agency_name` | Text | 0% | Full agency name (e.g., *Department of Housing Preservation and Development*). Redundant with `agency`. | 🟢 Safe (Redundant) |
| `complaint_type` | Text (Categorical) | 0% | Broad category of problem (e.g., *Heat/Hot Water, Noise - Residential, Illegal Parking, Street Condition*). | 🟢 **SAFE (Key Feature)** |
| `descriptor` | Text (Categorical) | < 1% | Detailed sub-classification of complaint (e.g., *Entire Building, Loud Music/Party, Blocked Hydrant, Pothole*). | 🟢 **SAFE (Key Feature)** |
| `location_type` | Text (Categorical) | ~10–25% | Setting of complaint (e.g., *Residential Building, Street/Sidewalk, Commercial, Store/Commercial*). | 🟢 **SAFE (Feature)** |

---

### Group 3: Geographic & Administrative Attributes

| Field Name | Raw Type | Missingness Expectation | Description & Analytical Role | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- |
| `incident_zip` | Text | ~2–5% | 5-digit USPS postal code of complaint location. Captures neighborhood socio-economic and structural dynamics. | 🟢 **SAFE (Key Feature)** |
| `incident_address` | Text | ~10–15% | Street address of incident. High cardinality; best abstracted to ZIP / Community District. | 🟢 Safe (Excluded to avoid overfitting) |
| `street_name` | Text | ~10–15% | Street name. High cardinality; abstracted. | 🟢 Safe (Excluded) |
| `cross_street_1` | Text | ~25–40% | First intersecting street. | 🟢 Safe (Excluded) |
| `cross_street_2` | Text | ~25–40% | Second intersecting street. | 🟢 Safe (Excluded) |
| `address_type` | Text | ~5–10% | Geocoding structure: *ADDRESS, INTERSECTION, BLOCKFACE, LATLONG*. | 🟢 Safe (Feature) |
| `city` | Text | ~2–5% | Postal municipality (e.g., *NEW YORK, BROOKLYN, BRONX, JAMAICA*). Redundant with borough/zip. | 🟢 Safe |
| `borough` | Text (Categorical) | < 0.5% | NYC Borough (*BRONX, BROOKLYN, MANHATTAN, QUEENS, STATEN ISLAND, Unspecified*). Core equity variable. | 🟢 **SAFE (Key Feature)** |
| `community_board` | Text | ~1–3% | Administrative community district identifier (e.g., *04 MANHATTAN*). Rich local governance proxy. | 🟢 **SAFE (Feature)** |
| `council_district` | Integer / Text | ~2–5% | NYC City Council legislative district (1–51). | 🟢 Safe (Feature) |
| `police_precinct` | Text | ~2–5% | Local NYPD precinct boundary (1–123). Useful proxy for police-jurisdiction complaints. | 🟢 Safe (Feature) |
| `latitude` | Number (Float) | ~3–6% | Spatial coordinate (WGS84). | 🟢 Safe (Spatial Feature) |
| `longitude` | Number (Float) | ~3–6% | Spatial coordinate (WGS84). | 🟢 Safe (Spatial Feature) |
| `location` | GeoJSON / Point | ~3–6% | Native spatial geometry object. | 🟢 Safe (Redundant with Lat/Lon) |

---

### Group 4: Case Lifecycle, Resolution & Operational Data

| Field Name | Raw Type | Missingness Expectation | Description & Analytical Role | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- |
| `status` | Text (Categorical) | 0% | Operational state: *Closed, Open, Pending, In Progress, Assigned*. | 🔴 **HIGH LEAKAGE (FORBIDDEN)** |
| `resolution_description` | Text | ~5–15% | Narrative explanation of how agency resolved the ticket (e.g., *"The Department of Housing inspected and issued a violation"*). | 🔴 **HIGH LEAKAGE (FORBIDDEN)** |
| `open_data_channel_type` | Text (Categorical) | 0% | Submission mechanism (*PHONE, ONLINE, MOBILE, OTHER, UNKNOWN*). Known at intake. | 🟢 **SAFE (Key Feature)** |
| `park_facility_name` | Text | ~90% | Specific park name if complaint was inside DPR jurisdiction. Mostly null. | 🟢 Safe (Sparse, Excluded) |
| `park_borough` | Text | ~90% | Borough designation for park complaints. Redundant with borough. | 🟢 Safe (Sparse, Excluded) |
| `vehicle_type` | Text | > 98% | Vehicle category for TLC / towing complaints. Mostly null. | 🟢 Safe (Sparse, Excluded) |
| `taxi_company_borough` | Text | > 98% | TLC base borough. Mostly null. | 🟢 Safe (Sparse, Excluded) |
| `taxi_pick_up_location`| Text | > 98% | TLC pick-up zone. Mostly null. | 🟢 Safe (Sparse, Excluded) |
| `bridge_highway_name` | Text | > 98% | Highway name for DOT complaints. Mostly null. | 🟢 Safe (Sparse, Excluded) |

---

### Group 5: Derived Analytical & Modeling Variables

These variables are engineered during our standardized sanitization phase:

| Engineered Variable | Source Derivation | Data Type | Role in Project | Leakage Guard |
| :--- | :--- | :--- | :--- | :--- |
| `resolution_time_days` | `(closed_date - created_date).total_seconds() / 86400.0` | Float (Continuous) | Descriptive ground truth duration. | 🔴 **Target Only** |
| `delayed_over_7d` | `resolution_time_days > 7.0` | Integer (Binary: 0, 1) | **Primary Prediction Target** for ML. | 🔴 **Target Only** |
| `delayed_over_30d` | `resolution_time_days > 30.0` | Integer (Binary: 0, 1) | Secondary extreme-delay analytical indicator. | 🔴 **Target Only** |
| `created_year` | `created_date.year` | Integer | Temporal cohort control. | 🟢 Safe |
| `created_month` | `created_date.month` | Integer (1–12) | Seasonal pattern feature. | 🟢 Safe |
| `created_day_of_week` | `created_date.dayofweek` | Integer (0=Mon .. 6=Sun)| Weekly operational cadence feature. | 🟢 Safe |
| `created_hour` | `created_date.hour` | Integer (0–23) | Intake time of day feature. | 🟢 Safe |
| `is_weekend` | `created_day_of_week in [5, 6]` | Integer (Binary: 0, 1) | Off-hours intake flag. | 🟢 Safe |

---

## 3. Storage Format & Compression Strategy

- **Raw Ingestion Candidate**: Socrata Open Data API delivers compressed JSON/CSV.
- **Avaloka Input Target**: Formatted, UTF-8 encoded **CSV** or **Parquet**.
- **File Size Management**: A sample of 120,000 records containing the ~15 core intake features and the target flag occupies **~32 MB in uncompressed CSV** and **~8 MB in Parquet**, well within Avaloka’s 100 MB single-file limit and optimized for memory efficiency in Avaloka's Ray compute cluster.

