# 2-MINUTE DEMO VIDEO RECORDING GUIDE

**Hackathon Requirement**: 2-Minute Screen Recording of Your Work with Avaloka  
**Target Duration**: Strictly $\le 120$ Seconds (Target: 110–115 seconds)  
**Host Platform**: Avaloka AI (https://avaloka.ai)

---

## 1. Pre-Recording Setup & Environment Preparation

### Recommended Software:
- **Option A (Desktop)**: **OBS Studio** (Free, open source) or **Windows Clipchamp / Screen Recorder** (`Win + Alt + R`).
- **Option B (Cloud/Browser)**: **Loom** (Chrome extension or desktop app).

### Display & Audio Settings:
1. **Screen Resolution**: Set display to **1920x1080 (1080p)**.
2. **Browser Zoom**: Set Chrome/browser zoom to **110%** for maximum legibility of charts, code, and chat text.
3. **Microphone**: Use a headset or external microphone; ensure zero ambient room echo or fan noise.
4. **Browser Tabs Prepared**:
   - Tab 1: Avaloka Project Dashboard with `nyc_311_analytical_full.csv` registered.
   - Tab 2: The active Avaloka chat thread containing the executed prompts, code inspection drawer, and Auto Insights charts.
   - Tab 3: The Model Training Agent (MTA) model card showing ROC-AUC and the Inference Panel.

---

## 2. Second-by-Second Execution Walkthrough (Follow `DEMO_SCRIPT.md`)

```
0:00 - 0:15  | Scene 1: Problem Hook & Research Question
0:15 - 0:35  | Scene 2: Dataset Catalog & Auto Insights Profiling
0:35 - 0:55  | Scene 3: Agency Bottlenecks & Code Drawer Inspection
0:55 - 1:15  | Scene 4: Adversarial Audit: Challenging Simpson's Paradox
1:15 - 1:40  | Scene 5: Predictive Modeling with MTA & Leakage Screen
1:40 - 2:00  | Scene 6: Independent Verification & Operational Summary
```

### Scene-by-Scene Checklist:
- [ ] **Scene 1 (0:00–0:15)**: Start on the project title card or NYC Open Data portal, smoothly transitioning into Avaloka. State the core question: *"Can we predict 7-day municipal resolution delays at intake?"*
- [ ] **Scene 2 (0:15–0:35)**: Click into `nyc_311_analytical_full.csv`. Show Avaloka's automatic column profiling and hover smoothly over the **Auto Insights** charts. Mention the right-skewed median (2.8 days) vs. 19% exceeding 7 days.
- [ ] **Scene 3 (0:35–0:55)**: Scroll to the Agency prompt. Highlight the volume vs. delay scatter plot. **Click to open the Coder Agent's Python script drawer**; show the clean `pd.to_datetime` and non-parametric median calculations.
- [ ] **Scene 4 (0:55–1:15)**: Show the adversarial challenge in chat: *"Does the borough disparity persist when controlling for heating complaints?"* Highlight the controlled chart where borough gaps narrow, demonstrating **Simpson's Paradox**.
- [ ] **Scene 5 (1:15–1:40)**: Show the **Model Training Agent (MTA)** conversation. Highlight the green **Data Leakage Screening** pass. Show the trained model metrics (ROC-AUC ~0.83, confusion matrix, high recall on delayed cases).
- [ ] **Scene 6 (1:40–2:00)**: Show the public report view and mention independent verification scripts. Close with strong impact statement on civic triage.

---

## 3. Post-Recording Quality & Export Checklist

1. **Verify Runtime**: Open video properties. Ensure total duration is **under 120 seconds** (e.g., 01:54). Submissions exceeding 2:00 can be disqualified.
2. **Video Export**: MP4 format, 1080p, AAC stereo audio, file size < 80 MB.
3. **Cloud Hosting**:
   - **YouTube**: Upload as **Unlisted** (anyone with the link can view; not public to search).
   - **Loom**: Ensure sharing is set to **"Anyone with the link can view"**.
   - **Google Drive**: Ensure access is set to **"Anyone with the link can view"** (NOT restricted).
4. **Incognito Test**: Copy the video link and open it in a private/incognito browser window without signing in. Confirm that the video plays instantly without password or permission requests.

