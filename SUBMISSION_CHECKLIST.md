# HACKATHON SUBMISSION CHECKLIST & FORM GUIDE

**Event**: Avaloka AI Engineering Internship Hackathon  
**Organizer**: Guruvai Sciences (Indu Ganti)  
**Submission Form**: [Google Form Link](https://docs.google.com/forms/d/e/1FAIpQLSd4A0I7uC5qK2qUp17uBLefKRBkhR2oIHBQ4p7wV9fbdr8Law/viewform)  
**Submission Cutoff**: Sunday, November 15, 2026, 11:59 PM IST  

---

## 1. Primary Submission Requirements Audit

| Requirement | Status | Verification Detail |
| :--- | :---: | :--- |
| **Star Avaloka Repo** | ✅ Done | Starred `https://github.com/guruvaidev/avaloka` on GitHub. |
| **Register via Form** | ✅ Ready | Registered at `https://docs.google.com/forms/d/e/1FAIpQLSfIf2pfCeHoKOcgmNhrWjE76XOeMXt3iTN0c6ghs_M7H9ewVQ/viewform`. |
| **Public Avaloka Project Link** | 🔗 Ready | Public shareable link from Avaloka workspace session. |
| **2-Minute Screen Recording** | 🎥 Ready | MP4 video ($\le 120$ seconds) uploaded to Unlisted YouTube / Loom. |
| **Code & Documentation Repo** | 💻 Live | GitHub repository: `https://github.com/HrishiKShah28/Response_Gap`. |
| **Final Analytical Report** | 📄 Complete | Full 12-section evidence report in `final_report/REPORT.md`. |

---

## 2. Copy-Paste Answers for Official Submission Google Form

### Field 1: Project Title
```text
The 311 Response Gap: Can We Predict Which Public Complaints Will Take Too Long to Resolve?
```

### Field 2: Research Question & Dataset
```text
Research Question: Which types of public service complaints, agencies, and boroughs experience the longest resolution delays in New York City, and can we predict whether a newly submitted complaint will take more than seven days to resolve using only information available when it is submitted?

Dataset: NYC 311 Service Requests from 2020 to Present (NYC Open Data / Socrata identifier erm2-nwe9). Evaluated across a representative 12-month stratified cohort of 115,000+ completed records from 2024.
```

### Field 3: Public Avaloka Report / Analysis URL
```text
[PASTE YOUR SHAREABLE AVALOKA PROJECT LINK HERE]
```

### Field 4: 2-Minute Screen Recording Link
```text
[PASTE YOUR UNLISTED YOUTUBE / LOOM / DRIVE VIDEO LINK HERE]
```
*(Ensure link permissions are set to "Anyone with the link can view" without requiring sign-in).*

### Field 5: GitHub Repository URL
```text
https://github.com/HrishiKShah28/Response_Gap
```

### Field 6: Summary of Findings & Key Innovations
```text
Using Avaloka's multi-agent data intelligence platform, we conducted an empirical investigation into NYC 311 operational telemetry (117,836 valid completed records + 2,131 open cases from 2024):

1. Operational Disparities: Resolution durations exhibit extreme positive skewness (median 0.20 days / 4.9 hours vs. arithmetic mean 13.10 days). Over 17.5% of complaints exceed 7 days, and 8.25% exceed 30 days.
2. Volume vs. Turnaround: Agency-level complaint volume was not significantly associated with median resolution time in this observational sample (Spearman r = -0.301, p = 0.342). NYPD processes 49.8% of volume at 0.04d median, while HPD, DOB, and DPR face structural inspection backlogs.
3. Case-Mix Confounding & Simpson's Paradox: In aggregate, Manhattan (20.8%) and the Bronx (18.7%) exhibit higher delay rates than Queens (14.5%). Across a multi-strata audit of 6 shared categories, we proved this is driven by case-mix variation (HPD housing complaints constitute 35.7% of Bronx inquiries vs. 10.7% in Queens). In Heat/Hot Water complaints alone, the Bronx is actually fastest (1.20d median vs. 1.58d Manhattan). For police enforcement, all boroughs achieve 0.00% 7-day delays.
4. Intake-Time Predictive Modeling: Partnering with Avaloka's Model Training Agent (MTA), we trained a binary classifier (delayed > 7 days) on strictly intake-time features using an out-of-time chronological split (Oct-Dec 2024). The champion Gradient Boosted Trees model achieves an ROC-AUC of 0.935, PR-AUC of 0.746, and captures 85.4% of delayed complaints (high sensitivity), providing actionable early warning flags for municipal triage.
5. Critical AI Verification: Every headline metric was cross-validated through independent sandboxed Python scripts (zero discrepancies across 27 metrics), and right-censoring bias from unresolved open cases was explicitly quantified (100% open > 7 days).
```

---

## 3. Final Submission Verification Protocol

1. **Incognito Test for Video**: Open video link in an incognito window. Verify playback starts immediately.
2. **Incognito Test for Avaloka**: Open Avaloka report link in incognito window. Verify visualizations and chat are visible.
3. **GitHub Verification**: Check `https://github.com/HrishiKShah28/Response_Gap` to verify all latest reports, scripts, and figures are pushed to `main`.
4. **Submit Form**: Submit at least 60–90 minutes before Sunday, Nov 15, 11:59 PM IST.

