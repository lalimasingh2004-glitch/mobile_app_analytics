#  Mobile App Analytics Dashboard

>  **[View Live Dashboard](https://mobile-app-analytics.onrender.com)** | [GitHub](https://github.com/lalimasingh2004-glitch/mobile_app_analytics)



<img width="1841" height="767" alt="dash1" src="https://github.com/user-attachments/assets/1d315bc7-9340-41a9-97bc-fbf330ae7e75" /> 
 
 <img width="1877" height="800" alt="dash2" src="https://github.com/user-attachments/assets/c4034d07-df37-49a5-bbdc-1086b67becfe" />
 
*A production-ready analytics and ML-powered churn prediction system for mobile applications.*  
Built with *Dash, Plotly, and Scikit-learn*, this project provides real-time business insights, predictive modeling, and user behavior analytics in one place.

---


##  Overview

This project delivers a complete *data-to-decision pipeline* for mobile app analytics — combining *data engineering, visualization, and machine learning* into one powerful system.

### Key Highlights:
- 20+ interactive dashboards and KPIs
- Random Forest–based churn prediction with >85% accuracy
- Real-time user engagement and retention insights
- Automated data refresh and churn risk scoring
- Business intelligence summaries and actionable recommendations

### Key Metrics:
| Metric | Value |
|--------|--------|
| Users Tracked | 9,340 |
| App Sessions | 146,194 |
| Avg Retention Rate | 60% |
| Revenue Opportunity Identified | $121,887 |

---

##  Features

###  Dashboard Capabilities
- *5 KPI Cards* – quick performance overview  
- *Executive Summary* – key insights & strategic recommendations  
- *Growth & Engagement Analytics* – daily active users, session patterns, and screen interactions  
- *Retention Analysis* – cohort-based visualization  
- *User Behavior Analysis* – funnel and segmentation charts  
- *ML-powered Churn Prediction* – churn probabilities & classifications

### Note on Load Time
- **First Load May Take Few Minutes**  
- This dashboard is hosted on [Render](https://render.com) using a free tier.  
- Free-tier apps spin down when inactive, so the **first request after some time** may take up to a minute to load.  
- Subsequent visits will load instantly.


###  Technical Highlights
-  Lazy Loading for faster performance  
-  Auto-refresh enabled  
-  Built with *Plotly Dash*  
-  Responsive design (desktop/tablet friendly)  
-  Error handling & logging integrated  

---

##  Installation

### *Prerequisites*
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Setup Instructions

### *Step 1:Clone the repository*

 bash
git clone https://github.com/lalimasingh2004-glitch/mobile_app_analytics.git
cd mobile_app_analytics

### *Step 2: Create Virtual Environment*

 ⁠bash
# Windows
python -m venv analytics_env
analytics_env\Scripts\activate

# macOS/Linux
python3 -m venv analytics_env
source analytics_env/bin/activate


⁠ ### *Step 3: Install Dependencies*

 ⁠bash
pip install -r requirements.txt


*requirements.txt*


pandas>=1.3.0
numpy>=1.21.0
plotly>=5.3.0
dash>=2.0.0
scikit-learn>=1.0.0
joblib>=1.1.0


⁠ ### *Step 4: Verify Installation*

 ⁠bash
python -c "import dash, pandas, plotly, sklearn; print(' All dependencies installed successfully!')"


⁠ ---

##  Usage

### *Run the Dashboard*

 ⁠bash
python app.py


⁠ Then open your browser to → *[http://127.0.0.1:8050/](http://127.0.0.1:8050/)*

### *Run Churn Predictions*

 ⁠bash
python churn_model.py


⁠ Outputs:

* Predicted churn probabilities
* User-level churn risk classifications

### *Data Refresh*

In the dashboard → click * Refresh Data*
Or programmatically:

 ⁠python
from app import refresh_data
refresh_data()


---

##  Project Structure
```
mobile_app_analytics/
│
├── .gitignore
├── app.py # Main dashboard
├── business_impact.py # Business insights & summaries
├── churn_model.py # ML churn prediction script
├── metrics_extractor.py # KPI & metric extraction module
├── requirements.txt
├── Procfile
├── render.yaml
├── runtime.txt
│
├── data/
│ ├── AI/ # AI-related experimental dashboard
│ ├── Deliverable/ # ML model artifacts (4 files)
│ ├── sub_data/ # 9 cleaned datasets (via SQL)
│ ├── advanced_dua.csv
│ ├── advanced_retention.csv
│ ├── churn_predictions.csv
│ ├── cohort_results.csv
│ ├── final_clean_dataset.csv
│ └── mobile_analytics.csv
│
├── docs/
│ ├── METHODOLOGY.md
│ ├── README.md
│ ├──DEPLOYMENT.md 
│ └── PROJECT_SUMMARY.md
│
├── notebooks/
│ ├── advanced_analytics.ipynb
│ ├── core_metrics1.ipynb
│ ├── core_metrics2.ipynb
│ ├── dashboard.ipynb
│ ├── pandas_analysis.ipynb
│ └── visualization.ipynb
│
├── sql/ # SQL queries used for cleaning & aggregation
│
├── test_files/ # Unit tests and sample runs
│
├── src/
│ └── dataset.py # Data generation script
│
├── analytics_env/ # Virtual environment
│
└── pycache/
```
---

##  Data Pipeline

*Data Flow*


Raw Data → Cleaning (SQL) → Sub Data → Basic analysis (Pandas) → Aggregation → Final Dataset → ML & Dashboard


⁠ *Key Data Sources*

| File                      | Purpose                       |
| ------------------------- | ----------------------------- |
| mobile_analytics.csv    | Raw session-level data        |
| sub_data/*.csv          | Cleaned subsets from SQL      |
| advanced_dua.csv        | Daily user activity           |
| advanced_retention.csv  | Retention cohorts             |
| final_clean_dataset.csv | Combined dataset for modeling |
| churn_predictions.csv   | Model predictions             |

---

##  ML Model

*Algorithm:* Random Forest Classifier
*Accuracy:* 85%+
*Framework:* Scikit-learn
*Feature Set:* 20+ engineered features

### *Feature Engineering*

* Session metrics: mean, std, min, max, sum
* Retention metrics: mean, min, max, std
* Engagement metrics: app opens, screen views
* User activity: total active days
* Categorical encodings: device type, channel, segment

### *Model Training Steps*

1. Data cleaning & feature engineering
2. Train/test split (70/30)
3. Hyperparameter tuning via grid search
4. Validation with confusion matrix & ROC curve
5. Exported model to data/Deliverable/churn_prediction_model.pkl

### *Prediction Example*

 ⁠python
from churn_model import predict_churn
import pandas as pd

new_users = pd.read_csv("data/final_clean_dataset.csv")
results = predict_churn(new_users)
print(results.head())


⁠ ---

##  Dashboard Components

| Section                 | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| *KPI Cards*           | DAU, Avg Session, Retention, App Opens, Screens      |
| *Executive Summary*   | Business findings & strategic insights               |
| *Growth & Engagement* | 7 charts (DAU, Sessions, Screens, Growth Rate, etc.) |
| *Retention Analysis*  | Cohort & churn visualization                         |
| *User Behavior*       | Device, Channel, Segment breakdowns                  |
| *Churn Prediction*    | Probability charts & summary cards                   |

---

##  Configuration

Modify constants in app.py:

 ⁠python
RETENTION_THRESHOLD_STRONG = 40
RETENTION_THRESHOLD_MODERATE = 25
SAMPLE_SIZE = 10000


⁠ Change color palette:

 ⁠python
KPI_COLORS = {
    'dau': '#3498db',
    'session': '#2ecc71',
    'retention': '#e74c3c',
    'opens': '#f39c12',
    'screens': '#9b59b6'
}


⁠ Model path in churn_model.py:

 ⁠python
MODEL_PATH = "data/Deliverable/churn_prediction_model.pkl"


---

##  Performance Optimization

 *Lazy loading* for charts
 *Data caching* for repeated metrics
 *Auto-sampling* for large datasets
 *Efficient Dash callbacks*
 *Optimized model inference*

*Benchmarks:*

| Operation                   | Time |
| --------------------------- | ---- |
| Dashboard Load              | few mins |
| Section Expand              | < 15s |
| Data Refresh                | < 5s |
| Churn Prediction (9K users) | < 10s |

---

##  Troubleshooting

| Issue                      | Solution                              |
| -------------------------- | ------------------------------------- |
| ModuleNotFoundError      | Run pip install -r requirements.txt |
| FileNotFoundError (data) | Ensure files are inside /data/      |
| Model load error         | Check model path in churn_model.py  |
| Port already in use      | Run app.run(port=8051)              |
| TypeError on merge       | Ensure consistent data types          |

---

##  Future Enhancements

* Real-time data streaming
* Advanced user segmentation (RFM analysis)
* Predictive LTV modeling
* A/B test analytics
* Automated alerts for churn risk
* PDF report export
* Authenticated dashboard access
* API endpoints for integrations

---

##  Contributing

Contributions are welcome!

1. Fork this repo
2. Create feature branch (git checkout -b feature/NewFeature)
3. Commit (git commit -m 'Add NewFeature')
4. Push (git push origin feature/NewFeature)
5. Open a pull request

---

##  Author

*Lalima Singh*
 - [[lalimasingh2004@gmail.com](mailto:lalimasingh2004@gmail.com)]
 - [LinkedIn](https://www.linkedin.com/in/lalima-singh-031431288)
 - [GitHub](https://github.com/lalimasingh2004-glitch)

---

##  Acknowledgments

* [Plotly Dash](https://plotly.com/dash) for visualization
* [Scikit-learn](https://scikit-learn.org) for machine learning
* [Pandas](https://pandas.pydata.org) for data manipulation
* [pgAdmin 4](https://www.pgadmin.org) for database cleaning and extraction  
* The open-source developer community

---

##  Support

For issues or feature requests:

* Open a GitHub issue
* Email: [[lalimasingh2004@gmail.com](mailto:lalimasingh2004@gmail.com)]
* See documentation in /docs/

---

 *Last Updated:* October 15, 2025
 *Version:* 1.0.0

---
