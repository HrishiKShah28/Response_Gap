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
Using Avaloka's multi-agent intelligence platform, we conducted an empirical investigation into NYC 311 operational telemetry:

1. Operational Disparities: Resolution durations exhibit extreme positive skewness (median 2.8 days, mean 8.6 days). Over 19% of complaints exceed 7 days, and 4.2% exceed 30 days.
2. Volume Does Not Drive Delay: NYPD processes the largest intake volume yet achieves the fastest median resolution, whereas HPD (Housing) and DOB (Buildings) face severe statutory backlogs. Complaint volume alone does not cause slow resolution (Spearman r = -0.18).
3. Simpson's Paradox Confirmed: In aggregate, the Bronx exhibits higher delay rates than other boroughs. However, when controlling for complaint categories (isolating Heat/Hot Water complaints), borough disparities diminish substantially, proving that geographic gaps are driven by case-mix variation (higher concentration of complex housing disputes) rather than municipal dispatch bias.
4. Intake-Time Predictive Modeling: Partnering with Avaloka's Model Training Agent (MTA), we trained a binary classifier (delayed > 7 days) on strictly intake-time features (agency, complaint type, descriptor, borough, timing) using an out-of-time chronological train/test split. The model achieves an ROC-AUC of 0.83 and captures >75% of delayed complaints (high recall), providing actionable early warning flags for municipal triage.
5. Critical AI Verification: Every headline metric was cross-validated through independent sandboxed Python scripts, and right-censoring bias from unresolved open cases was explicitly quantified.
```

---

## 3. Final Submission Verification Protocol

1. **Incognito Test for Video**: Open video link in an incognito window. Verify playback starts immediately.
2. **Incognito Test for Avaloka**: Open Avaloka report link in incognito window. Verify visualizations and chat are visible.
3. **GitHub Verification**: Check `https://github.com/HrishiKShah28/Response_Gap` to verify all latest reports, scripts, and figures are pushed to `main`.
4. **Submit Form**: Submit at least 60–90 minutes before Sunday, Nov 15, 11:59 PM IST.
