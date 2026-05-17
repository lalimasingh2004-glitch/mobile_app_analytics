# Mobile App Analytics Dashboard

> **[View Live Dashboard](https://mobile-app-analytics.onrender.com)** | [GitHub](https://github.com/lalimasingh2004-glitch/mobile_app_analytics)

<img width="1395" height="833" alt="Screenshot 2026-05-17 174648" src="https://github.com/user-attachments/assets/e00fa2fe-a160-4d04-828c-050fbe87bcef" />

<img width="1389" height="932" alt="Screenshot 2026-05-17 175158" src="https://github.com/user-attachments/assets/031ae9cd-ca9e-4289-9321-7aff5cb09c3d" />

<img width="1377" height="922" alt="Screenshot 2026-05-17 175246" src="https://github.com/user-attachments/assets/a83cf709-d68f-490f-9cce-1c139c557891" />

*A production-ready analytics and ML-powered churn prediction system for mobile applications.*
Built with **Dash, Plotly, and Scikit-learn**, this project provides real-time business insights, predictive modeling, and user behavior analytics in one place.

---

## Overview

This project delivers a complete **data-to-decision pipeline** for mobile app analytics — combining **data engineering, visualization, and machine learning** into one powerful system.

### Key Highlights

- 20+ interactive dashboards and KPIs
- Random Forest–based churn prediction with **F1-score of 0.851** and **AUC-ROC of 0.994**
- Class imbalance handled using `class_weight='balanced'` (5.4% churn rate)
- Real-time user engagement and retention insights
- Automated data refresh and churn risk scoring
- Business intelligence summaries and actionable recommendations

### Key Metrics

| Metric | Value |
|--------|--------|
| Users Tracked | 9,340 |
| App Sessions | 146,194 |
| Avg Retention Rate | 60% |
| Revenue Opportunity Identified | $121,887 |

---

## Features

### Dashboard Capabilities

- **5 KPI Cards** – quick performance overview
- **Executive Summary** – key insights & strategic recommendations
- **Growth & Engagement Analytics** – daily active users, session patterns, and screen interactions
- **Retention Analysis** – cohort-based visualization
- **User Behavior Analysis** – funnel and segmentation charts
- **ML-powered Churn Prediction** – churn probabilities & classifications

### Note on Load Time

> This dashboard is hosted on [Render](https://render.com) using a free tier. Free-tier apps spin down when inactive, so the **first request** may take up to a minute to load. Subsequent visits will load instantly.

### Technical Highlights

- Lazy Loading for faster performance
- Auto-refresh enabled
- Built with **Plotly Dash**
- Responsive design (desktop/tablet friendly)
- Error handling & logging integrated

---

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/lalimasingh2004-glitch/mobile_app_analytics.git
cd mobile_app_analytics
```

### Step 2 — Create Virtual Environment

```bash
# Windows
python -m venv analytics_env
analytics_env\Scripts\activate

# macOS/Linux
python3 -m venv analytics_env
source analytics_env/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install pandas numpy plotly dash scikit-learn joblib matplotlib seaborn
```

### Step 4 — Verify Installation

```bash
python -c "import dash, pandas, plotly, sklearn, matplotlib, seaborn; print('All dependencies installed successfully!')"
```

---

## Usage

### Run the Dashboard

```bash
python app.py
```

Then open your browser → [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

### Run Churn Predictions

```bash
python churn_model.py
```

Outputs:
- Predicted churn probabilities
- User-level churn risk classifications

### Run Full Model Evaluation

```bash
python evaluate_churn.py
```

Outputs:
- F1-score, Precision, Recall, AUC-ROC
- Confusion Matrix, ROC Curve, Feature Importance charts
- Saved as `churn_evaluation_charts.png`

### Data Refresh

In the dashboard → click **Refresh Data**, or programmatically:

```python
from app import refresh_data
refresh_data()
```

---

## Project Structure
```
mobile_app_analytics/
│
├── app.py                        # Main dashboard
├── business_impact.py            # Business insights & summaries
├── churn_model.py                # ML churn prediction script
├── evaluate_churn.py             # Model evaluation — F1, AUC-ROC, charts
├── metrics_extractor.py          # KPI & metric extraction module
├── churn_evaluation_charts.png   # Confusion matrix, ROC curve, feature importance
├── requirements.txt
├── Procfile
├── render.yaml
├── runtime.txt
│
├── data/
│   ├── Deliverable/              # ML model artifacts
│   │   ├── churn_prediction_model.pkl
│   │   └── churn_prediction_model_v2.pkl   # Improved model with balanced classes
│   ├── sub_data/                 # 9 cleaned datasets (via SQL)
│   ├── advanced_dua.csv
│   ├── advanced_retention.csv
│   ├── churn_predictions.csv
│   ├── cohort_results.csv
│   ├── final_clean_dataset.csv
│   └── mobile_analytics.csv
│
├── docs/
│   ├── METHODOLOGY.md
│   ├── README.md
│   ├── DEPLOYMENT.md
│   └── PROJECT_SUMMARY.md
│
├── notebooks/
│   ├── advanced_analytics.ipynb
│   ├── core_metrics1.ipynb
│   ├── core_metrics2.ipynb
│   ├── dashboard.ipynb
│   ├── pandas_analysis.ipynb
│   └── visualization.ipynb
│
├── sql/                          # SQL queries for cleaning & aggregation
├── test_files/                   # Unit tests and sample runs
└── src/
└── dataset.py                # Data generation script

---
```
## Data Pipeline

Raw Data → Cleaning (SQL) → Sub Data → Analysis (Pandas) → Aggregation → Final Dataset → ML & Dashboard

### Key Data Sources

| File | Purpose |
|------|---------|
| `mobile_analytics.csv` | Raw session-level data |
| `sub_data/*.csv` | Cleaned subsets from SQL |
| `advanced_dua.csv` | Daily user activity |
| `advanced_retention.csv` | Retention cohorts |
| `final_clean_dataset.csv` | Combined dataset for modeling |
| `churn_predictions.csv` | Model predictions |

---

## ML Model

| Property | Detail |
|----------|--------|
| **Algorithm** | Random Forest Classifier |
| **Accuracy** | 98.5% |
| **F1-Score** | 0.851 |
| **AUC-ROC** | 0.994 |
| **Precision** | 0.92 |
| **Recall** | 0.79 |
| **Framework** | Scikit-learn |
| **Features** | 25 engineered features per user |
| **Class Imbalance** | Handled via `class_weight='balanced'` (5.4% churn rate) |
| **Train/Test Split** | 70/30 with stratification |

### How Churn is Defined

A user is labeled **churned** if their last recorded session was more than **30 days before** the most recent date in the dataset. This is a standard industry definition used by companies like Netflix, Spotify, and others.
Max date in dataset  =  September 1, 2025
Churn cutoff         =  August 2, 2025
Last seen BEFORE Aug 2  →  churned = 1
Last seen AFTER  Aug 2  →  churned = 0

### Class Imbalance Handling

With only 5.4% of users churning, a naive model would simply predict "not churned" for everyone and achieve high accuracy while being completely useless. We solve this using `class_weight='balanced'`, which automatically penalizes misclassification of the minority (churned) class proportionally — making the model actually learn to detect churners.

### Feature Engineering

Features are aggregated **per user** from raw session-level data:

- **Session metrics** — total sessions, mean, std, min, max duration
- **Engagement metrics** — total app opens, average screens viewed
- **Retention metrics** — mean, min, max retention rate
- **Activity metrics** — total active days
- **Categorical encodings** — device type, acquisition channel, user segment

### Model Evaluation Charts

Running `evaluate_churn.py` generates `churn_evaluation_charts.png` containing:

- **Confusion Matrix** — true vs predicted classifications
- **ROC Curve** — model discrimination ability (AUC = 0.994)
- **Top 10 Feature Importances** — key churn drivers

---

## Dashboard Components

| Section | Description |
|---------|-------------|
| **KPI Cards** | DAU, Avg Session, Retention, App Opens, Screens |
| **Executive Summary** | Business findings & strategic insights |
| **Growth & Engagement** | 7 charts — DAU, Sessions, Screens, Growth Rate, etc. |
| **Retention Analysis** | Cohort & churn visualization |
| **User Behavior** | Device, Channel, Segment breakdowns |
| **Churn Prediction** | Probability charts & summary cards |

---

## Performance

| Operation | Time |
|-----------|------|
| Dashboard Load (cold start) | ~1 min (free tier) |
| Section Expand | < 15s |
| Data Refresh | < 5s |
| Churn Prediction (9K users) | < 10s |
| Model Evaluation Script | ~30s |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install pandas numpy plotly dash scikit-learn joblib matplotlib seaborn` |
| `FileNotFoundError` (data) | Ensure files are inside `/data/` |
| Model load error | Check model path in `churn_model.py` |
| Port already in use | Run `app.run(port=8051)` |
| Version warning on model load | Use `churn_prediction_model_v2.pkl` — retrained on current sklearn |

---

## Future Enhancements

- Real-time data streaming
- Advanced user segmentation (RFM analysis)
- Predictive LTV modeling
- A/B test analytics
- Automated alerts for churn risk
- PDF report export
- Authenticated dashboard access
- API endpoints for integrations

---

## Contributing

Contributions are welcome!

1. Fork this repo
2. Create a feature branch — `git checkout -b feature/NewFeature`
3. Commit your changes — `git commit -m 'Add NewFeature'`
4. Push to the branch — `git push origin feature/NewFeature`
5. Open a pull request

---

## Author

**Lalima Singh**

- Email: [lalimasingh2004@gmail.com](mailto:lalimasingh2004@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/lalima-singh-031431288)
- [GitHub](https://github.com/lalimasingh2004-glitch)

---

## Acknowledgments

- [Plotly Dash](https://plotly.com/dash) for visualization
- [Scikit-learn](https://scikit-learn.org) for machine learning
- [Pandas](https://pandas.pydata.org) for data manipulation
- [pgAdmin 4](https://www.pgadmin.org) for database cleaning and extraction
- The open-source developer community

---

## Support

For issues or feature requests:

- Open a [GitHub Issue](https://github.com/lalimasingh2004-glitch/mobile_app_analytics/issues)
- Email: [lalimasingh2004@gmail.com](mailto:lalimasingh2004@gmail.com)
- See documentation in `/docs/`

---

*Last Updated: May 2026*
*Version: 2.0.0*
