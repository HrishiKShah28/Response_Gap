# HACKATHON OPERATIONAL TIMELINE & PHASE GATES

**Event**: Avaloka AI Engineering Internship Hackathon  
**Organizer**: Guruvai Sciences (Indu Ganti)  
**Submission Cutoff**: Sunday, November 15, 2026, 11:59 PM IST  

---

## 1. Hackathon Deadlines & Submission Checkpoints

```
[Fri 13 Nov, 11:59 PM IST]  ──► Registration Deadline & Repository Star Verification
[Sat 14 Nov, 09:00 AM IST]  ──► Official Hackathon Kickoff: Data Prep & Avaloka Ingestion
[Sat 14 Nov, 08:00 PM IST]  ──► Milestone 1: Exploratory Analysis, Code Audits & Challenge Complete
[Sun 15 Nov, 01:00 PM IST]  ──► Milestone 2: Predictive Modeling (MTA) & Independent Validation Complete
[Sun 15 Nov, 06:00 PM IST]  ──► Milestone 3: Final Written Report Compiled & Cross-Checked
[Sun 15 Nov, 09:00 PM IST]  ──► Milestone 4: 2-Minute Screen Recording Recorded & Edited
[Sun 15 Nov, 10:30 PM IST]  ──► Final QA & Form Submission (90-Minute Contingency Buffer)
[Sun 15 Nov, 11:59 PM IST]  ──► HARD DEADLINE
```

---

## 2. Phase-by-Phase Execution Schedule

### Phase 0: Pre-Hackathon Setup & Planning (Friday, Nov 13)
- [x] Star the official Avaloka repository: `https://github.com/guruvaidev/avaloka`.
- [x] Complete registration form: `https://docs.google.com/forms/d/e/1FAIpQLSfIf2pfCeHoKOcgmNhrWjE76XOeMXt3iTN0c6ghs_M7H9ewVQ/viewform`.
- [x] Author the 11 core planning specifications in the project workspace.
- [ ] Review and obtain formal human signoff on architecture and prompts.

---

### Phase 1: Data Acquisition, Sanitization & Payload Packaging (Sat Nov 14, 09:00 – 12:30 IST)
- **Goal**: Download, filter, and package the representative NYC 311 dataset from Socrata API (`erm2-nwe9`).
- **Tasks**:
  1. Execute sandboxed acquisition script pulling 120,000 records across 2024–2025.
  2. Perform data hygiene checks (drop negative resolution timestamps, cap extreme multi-year outliers).
  3. Extract auxiliary open/censored ticket subset ($N \approx 8,000$) for survivor bias reporting.
  4. Generate `nyc_311_analytical_full.csv` (~35 MB) and `nyc_311_model_intake.csv` (~28 MB).
  5. Verify payload is safely below Avaloka's 100 MB single-file threshold.
- **Phase Gate**: Verified clean CSV ready on disk with documented row counts.

---

### Phase 2: Avaloka Ingestion, Profiling & Overall Performance (Sat Nov 14, 13:30 – 16:30 IST)
- **Goal**: Register dataset on Avaloka platform, trigger Auto Insights, and execute Theme A & B analyses.
- **Tasks**:
  1. Upload `nyc_311_analytical_full.csv` to Avaloka.
  2. Execute **Prompt 1**: Ingestion, schema profiling, missing values, and review of the 5 Auto Insights charts.
  3. Execute **Prompt 2**: Duration distribution, median/IQR, 7-day and 30-day delay rate quantiles.
  4. Inspect generated Python code from Coder Agent; verify `pd.to_datetime` and quantile logic.
  5. Execute **Prompt 3**: Agency benchmarks, volume vs. median duration scatter plot.
- **Phase Gate**: Auto Insights captured, quantile tables logged, agency rankings documented.

---

### Phase 3: Deep Dives, Equity Checks & Adversarial Verification (Sat Nov 14, 17:00 – 21:00 IST)
- **Goal**: Execute Theme C, D, and E inquiries, perform Simpson's Paradox check, and challenge an AI claim.
- **Tasks**:
  1. Execute **Prompt 4**: Complaint category and descriptor bottlenecks (top 15 slowest types).
  2. Execute **Prompt 5**: Borough resolution comparison and Simpson's Paradox category-controlled test.
  3. Execute **Prompt 6**: Temporal submission cadence (hour of day, day of week, weekend latency).
  4. **Adversarial Human-in-the-Loop Audit**: Challenge Avaloka on a counter-intuitive finding (e.g., why aggregate borough rankings disappear when controlling for housing complaints).
  5. Save all code snippets, charts, and intermediate query outputs into `avaloka_artifacts/`.
- **Phase Gate**: Complete set of EDA findings and verified charts ready for reporting.

---

### Phase 4: Predictive Modeling with Avaloka MTA (Sun Nov 15, 09:00 – 13:00 IST)
- **Goal**: Build and evaluate intake-time delay classifier using Avaloka's Model Training Agent.
- **Tasks**:
  1. Ingest `nyc_311_model_intake.csv` (strictly intake-time features, target = `delayed_over_7d`).
  2. Submit Model Request prompt to MTA.
  3. Verify MTA's **Data Leakage Screening** passes with zero flags.
  4. Review MTA proposed training plan; tune class weighting and request baseline comparison.
  5. Approve and trigger training (evaluating Logistic Regression and Tree Ensemble).
  6. Extract metrics: ROC-AUC, PR-AUC, Confusion Matrix, and Model Run ID.
  7. Conduct decision threshold analysis for municipal asymmetric loss.
- **Phase Gate**: Valid Model Run ID, confusion matrix, and feature importances extracted.

---

### Phase 5: Independent Cross-Check & Report Compilation (Sun Nov 15, 14:00 – 18:00 IST)
- **Goal**: Run independent Python verification scripts and author the final comprehensive report.
- **Tasks**:
  1. Run `validation_scripts/` against raw data to independently verify headline medians and delay rates.
  2. Author final analytical report in `final_report/REPORT.md` (complete 12-section standard).
  3. Embed high-resolution figures, comparison tables, and methodological disclaimers.
  4. Document survivor bias from open tickets and anti-leakage compliance.
- **Phase Gate**: Complete, publication-grade analytical report finalized and proofread.

---

### Phase 6: 2-Minute Screen Recording & Narration (Sun Nov 15, 18:30 – 21:00 IST)
- **Goal**: Record, edit, and export the required 2-minute (120-second) video submission.
- **Tasks**:
  1. Set up screen recording software (OBS Studio / Loom / Camtasia) at 1080p 60fps.
  2. Rehearse following the exact second-by-second timeline in `DEMO_SCRIPT.md`.
  3. Record video capturing Avaloka UI: prompt submission, Coder Agent code inspection, Auto Insights charts, MTA training dialogue, and challenging the AI finding.
  4. Record crisp voiceover audio synced to on-screen actions.
  5. Review final runtime: strictly $\le 120$ seconds.
- **Phase Gate**: Video exported (MP4) and uploaded to accessible cloud storage (YouTube Unlisted / Google Drive).

---

### Phase 7: Final Audit, Submission & Buffer (Sun Nov 15, 21:00 – 22:30 IST)
- **Goal**: Verify all links, confirm public access permissions, and submit form.
- **Tasks**:
  1. Test public shareable Avaloka project link in an incognito browser window.
  2. Test video link accessibility without requiring sign-in.
  3. Verify GitHub repo star on `guruvaidev/avaloka`.
  4. Fill out and submit the official submission Google Form:  
     `https://docs.google.com/forms/d/e/1FAIpQLSd4A0I7uC5qK2qUp17uBLefKRBkhR2oIHBQ4p7wV9fbdr8Law/viewform`.
  5. Archive all submission confirmations.
- **Buffer**: 90-minute safety cushion prior to the 11:59 PM IST cutoff.

---

## 3. Contingency & Fallback Matrix

| Potential Failure Mode | Likelihood | Impact | Pre-Planned Mitigation / Fallback |
| :--- | :--- | :--- | :--- |
| **Socrata API Rate Limiting** | Low | High | Use pagination (`$offset`, `$limit=50000`), fetch via HTTPS stream, cache raw JSON/CSV locally immediately. |
| **Avaloka File Upload Timeout** | Low | Medium | Pre-filter columns down to the essential 15 features; compress to Parquet (8 MB) or optimized CSV (28 MB). |
| **MTA Compute Latency** | Medium | Medium | Train on a stratified 50,000-record training split if full 100k times out on free-tier compute. |
| **Video Runtime Exceeds 120s** | Medium | High | Script is tightly timed to 110s, leaving a 10s natural pause buffer; edit with pacing cuts if necessary. |

