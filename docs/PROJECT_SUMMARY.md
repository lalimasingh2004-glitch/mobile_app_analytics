# Mobile App Analytics Dashboard - Project Summary

## Executive Summary

A production-ready business intelligence dashboard with ML-powered churn prediction, analyzing 9,340 users and 146,194 sessions to identify $121,887 in revenue at risk — with a story-driven 5-act dashboard that translates raw data into actionable business decisions.

- **Project Status:** COMPLETE - Production Ready
- **Last Updated:** May 2026
- **Live Dashboard:** https://mobile-app-analytics-3.onrender.com

---

## Project Outcomes

### Quantitative Achievements

| Metric | Achievement |
|--------|-------------|
| Users Analyzed | 9,340 |
| Sessions Tracked | 146,194 |
| F1 Score | 0.851 |
| AUC-ROC | 0.994 |
| Precision | 92% |
| Recall | 79% |
| Class Imbalance Handling | class_weight='balanced' (5.4% churn rate) |
| Engineered Features | 25 per user |
| Revenue at Risk Identified | $121,887 |
| High-Risk Users Identified | 504 churned users |

### Qualitative Achievements

**Business Value:**
- Story-driven dashboard answering 5 core business questions
- Plain-English insight boxes below every chart
- Strategic recommendations with quantified revenue impact
- Executive-ready presentation format

**Technical Excellence:**
- Proper churn definition (30-day inactivity rule)
- Class imbalance handled correctly (not just accuracy)
- Model evaluated on F1, AUC-ROC, Precision, Recall
- Auto-deploys to Render on every GitHub push

---

## The 5-Act Dashboard Story

**ACT 1 — What is the problem?**
504 users churned at 5.4% — leaving $121,887 in revenue at risk.

**ACT 2 — Who is churning?**
Breakdown by user segment, device type, and acquisition channel.

**ACT 3 — Why are they churning?**
Top 5 behavioural signals from Random Forest feature importance.

**ACT 4 — How accurately can we predict churn?**
F1=0.851, AUC-ROC=0.994, Precision=92%, Recall=79%.

**ACT 5 — What should the business do?**
3 strategic recommendations with revenue recovery scenarios.

---

## Machine Learning Model

**Algorithm:** Random Forest Classifier
**Framework:** Scikit-learn
**Features:** 25 engineered features per user

### Performance Metrics

| Metric | Value |
|--------|-------|
| Accuracy | 98.5% |
| F1 Score | 0.851 |
| AUC-ROC | 0.994 |
| Precision | 0.92 |
| Recall | 0.79 |

### Key Design Decisions

**Churn Definition:**
Users last seen more than 30 days before the most recent date = churned. Industry standard used by Netflix, Spotify, and others.

**Class Imbalance:**
Only 5.4% of users churned. Used `class_weight='balanced'` to prevent the model from simply predicting "not churned" for everyone.

**Evaluation Priority:**
F1-score and AUC-ROC prioritized over raw accuracy — the only correct approach for imbalanced classification problems.

### Top Churn Drivers
1. `avg_retention_rate` — strongest predictor
2. `active_days` — habit formation is critical
3. `total_sessions` — low engagement = early churn signal
4. `avg_session_duration` — short sessions = low value
5. `total_app_opens` — early disengagement indicator

---

## Strategic Recommendations

**01 — Target High-Risk Users Immediately**
Model flags users with >70% churn probability. Personalised re-engagement campaigns before they leave. A small retention offer is far cheaper than losing $241.84 per user.

**02 — Fix Early Engagement**
Active days and session count are the #2 and #3 churn drivers. Users who don't form a habit in the first 7 days are most at risk. Improve onboarding with push notifications and daily streaks.

**03 — Reassess Acquisition Channels**
The 'unknown' channel has a 50% churn rate — likely attracting low-intent users. Reallocate budget toward channels with better long-term retention.

### Revenue Recovery Scenarios

| Scenario | Users Saved | Revenue Saved |
|----------|-------------|---------------|
| Retain 25% of churners | 126 users | $30,472 |
| Retain 50% of churners | 252 users | $60,944 |
| Retain 75% of churners | 378 users | $91,415 |

---

## Technical Architecture

**Tech Stack:**
- Python 3.8+, Pandas, NumPy, Joblib
- Scikit-learn (Random Forest, class_weight='balanced')
- Plotly Dash (dark professional theme)
- PostgreSQL + pgAdmin 4
- Git + GitHub + Render (auto-deploy)

**Data Pipeline:**
Raw Data Generation (dataset.py)
↓
PostgreSQL Database
↓
SQL-based Extraction & Cleaning
↓
9 Specialized Sub-datasets
↓
Pandas Aggregation & Feature Engineering
↓
Random Forest Model (evaluate_churn.py)
↓
5-Act BI Dashboard (app.py)

**Key Files:**
app.py                  ← 5-Act story dashboard
evaluate_churn.py       ← Model evaluation script
churn_model.py          ← Prediction script
metrics_extractor.py    ← KPI extraction
business_impact.py      ← Revenue impact analysis

---

## Deliverables

**Code:** `app.py`, `evaluate_churn.py`, `churn_model.py`, `metrics_extractor.py`, `business_impact.py`

**Data:** `data/` folder with cleaned datasets and model artifacts

**Model:** `churn_prediction_model_v2.pkl` (trained with class_weight='balanced')

**Charts:** `churn_evaluation_charts.png` (confusion matrix, ROC curve, feature importance)

**Documentation:** `README.md`, `METHODOLOGY.md`, `PROJECT_SUMMARY.md`, `DEPLOYMENT.md`

---

## Author

**Lalima Singh**
- Email: lalimasingh2004@gmail.com
- [LinkedIn](https://www.linkedin.com/in/lalima-singh-031431288)
- [GitHub](https://github.com/lalimasingh2004-glitch)
- [Live Dashboard](https://mobile-app-analytics-3.onrender.com)
