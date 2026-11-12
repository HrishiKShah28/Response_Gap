# 2-MINUTE DEMO VIDEO SCRIPT & STORYBOARD

**Project**: The 311 Response Gap: Can We Predict Which Public Complaints Will Take Too Long to Resolve?  
**Target Duration**: Exactly 120 Seconds (2:00 Minutes)  
**Submission Requirement**: Avaloka AI Engineering Internship Hackathon (Guruvai Sciences)

---

## 1. Technical Recording Specifications

- **Target Resolution**: 1920x1080 (1080p, 16:9), 60 FPS.
- **Audio Capture**: Clean directional microphone, zero background noise, normalized to -14 LUFS.
- **Pacing**: Steady delivery at ~135 words per minute (Total spoken word count: ~260 words).
- **Cursor Discipline**: Smooth, deliberate cursor movements; no rapid erratic scrolling; highlight key charts with brief smooth hovering.
- **Visual Focus**: The Avaloka Web UI (`avaloka.ai`), showing dataset catalog, chat conversation, code inspection drawer, Auto Insights panel, and Model Training Agent cards.

---

## 2. Second-by-Second Storyboard & Spoken Narration

```
0:00 - 0:15  | Scene 1: The Research Question & Civic Problem
0:15 - 0:35  | Scene 2: Dataset Ingestion & Auto-Insights Profiling
0:35 - 0:55  | Scene 3: Investigating Bottlenecks & Code Inspection
0:55 - 1:15  | Scene 4: Challenging an AI Claim (Simpson's Paradox)
1:15 - 1:40  | Scene 5: Predictive Modeling with MTA & Leakage Screen
1:40 - 2:00  | Scene 6: Independent Verification & Operational Impact
```

---

### Scene 1: The Research Question & Real-World Motivation (0:00 – 0:15)
- **On Screen**: Quick title card showing *"The 311 Response Gap"* transitioning immediately to the NYC Open Data 311 portal and then the clean Avaloka workspace.
- **Visual Action**: Cursor highlights the research question pinned in the project header.
- **Spoken Narration (Voiceover)**:
  > *"Every year, New Yorkers file millions of 311 complaints. But while some are closed in hours, others languish for weeks. Our project investigated the 'Response Gap': which complaints suffer systemic delays, and can Avaloka predict if a newly submitted ticket will take over seven days using only information available at intake?"*
- **Duration**: 15 seconds (Cumulative: 0:15)

---

### Scene 2: Dataset Registration & Auto-Profiling (0:15 – 0:35)
- **On Screen**: Avaloka Dataset Catalog showing `nyc_311_analytical_full.csv` (115,000 records, 2024–2025).
- **Visual Action**: Click on the dataset. The screen reveals Avaloka's automatic data dictionary, missing value summary, and the **Auto Insights** panel with interactive charts.
- **Spoken Narration (Voiceover)**:
  > *"We ingested 115,000 sanitized records from NYC Open Data into Avaloka. Avaloka's agents instantly profiled the schema, verified temporal consistency, and rendered Auto Insights—revealing an extreme right-skewed resolution distribution where the median is 2.8 days, yet over 19% of complaints exceed seven calendar days."*
- **Duration**: 20 seconds (Cumulative: 0:35)

---

### Scene 3: Investigating Agency Bottlenecks & Code Inspection (0:35 – 0:55)
- **On Screen**: Avaloka Chat Interface. Prompt asking for agency benchmarks and the volume vs. delay scatter plot.
- **Visual Action**: Avaloka responds with the scatter plot. User clicks to expand the **Coder Agent's Python script**, highlighting `pd.to_datetime` and non-parametric median aggregations.
- **Spoken Narration (Voiceover)**:
  > *"Prompting Avaloka to benchmark responding agencies produced a surprising finding: complaint volume does not drive delays. NYPD handles the highest volume but resolves cases rapidly, while HPD and DOB face the largest backlogs. Inspecting Avaloka's generated Python code confirmed robust median and quantile logic with zero negative timestamps."*
- **Duration**: 20 seconds (Cumulative: 0:55)

---

### Scene 4: Adversarial Audit: Challenging an AI Claim (0:55 – 1:15)
- **On Screen**: Chat prompt comparing borough delays, followed by a follow-up challenging Simpson's Paradox.
- **Visual Action**: Show user submitting the follow-up prompt: *"Does the borough disparity persist when controlling for Heat/Hot Water complaints?"* Avaloka runs the controlled cross-tabulation and updates the chart.
- **Spoken Narration (Voiceover)**:
  > *"When Avaloka initially reported that the Bronx had higher delay rates than Manhattan, we challenged the finding to test for Simpson’s Paradox. Prompting Avaloka to control for complaint category proved that when isolating heating complaints alone, borough differences largely vanish—the disparity was driven by complaint mix, not agency bias."*
- **Duration**: 20 seconds (Cumulative: 1:15)

---

### Scene 5: Predictive Modeling with the Model Training Agent (1:15 – 1:40)
- **On Screen**: Interaction with Avaloka's **Model Training Agent (MTA)**.
- **Visual Action**: Show the MTA proposing the training plan for `delayed_over_7d`. Show the **Data Leakage Screening** status passing (`closed_date` and `status` excluded). User clicks *"Looks good — train it"*. The model card updates with ROC-AUC (0.83), PR-AUC, and the confusion matrix.
- **Spoken Narration (Voiceover)**:
  > *"Next, we tasked Avaloka's Model Training Agent with predicting 7-day delays. The agent screened and blocked post-intake fields to guarantee zero data leakage. Training with an out-of-time chronological split achieved an ROC-AUC of 0.83, vastly outperforming the majority baseline and delivering high recall on prolonged complaints."*
- **Duration**: 25 seconds (Cumulative: 1:40)

---

### Scene 6: Independent Verification & Operational Impact (1:40 – 2:00)
- **On Screen**: Side-by-side view showing Avaloka's report view and our local verification script confirming identical metrics, ending on the final report summary card.
- **Visual Action**: Hover over the shareable Avaloka project URL, showing the published report.
- **Spoken Narration (Voiceover)**:
  > *"Every headline metric was independently verified against raw data. By combining Avaloka's autonomous multi-agent workflow with rigorous human verification, we proved that cities can reliably triage high-risk complaints at the moment of intake. Explore our public report and code at the links below. Thank you!"*
- **Duration**: 20 seconds (Cumulative: 2:00 / 120s total)

---

## 3. Rehearsal & Editing Checklist

- [ ] Word count verified at ~265 words (132 words/min).
- [ ] No pauses longer than 1.5 seconds.
- [ ] UI text zoomed to 110% in Chrome for razor-sharp legibility on mobile and desktop.
- [ ] Audio noise gate and compressor applied in post-processing.
- [ ] Export format: MP4, H.264, 1080p, AAC Audio, File size < 50 MB.

