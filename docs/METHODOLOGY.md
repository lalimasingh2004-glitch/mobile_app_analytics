# Mobile App Analytics Dashboard - Methodology

**Author:** Lalima Singh
**Last Updated:** May 2026

---

## Table of Contents

1. Research Objectives
2. Data Collection Strategy
3. Data Cleaning Pipeline
4. Exploratory Data Analysis
5. Feature Engineering Process
6. Machine Learning Model Development
7. Dashboard Architecture
8. Statistical Methods
9. Validation & Testing
10. Assumptions & Limitations
11. Future Improvements
12. References & Technologies Used

---

## 1. Research Objectives

### Primary Goals

**Business Intelligence:**
- Understand user engagement patterns and behavior
- Identify factors influencing retention and churn
- Quantify revenue opportunities from user optimization
- Provide actionable recommendations for growth

**Technical Innovation:**
- Build scalable analytics infrastructure
- Implement predictive modeling for proactive intervention
- Create story-driven business intelligence dashboard
- Deliver production-ready deployment on Render

### Success Criteria

| Criterion | Target | Achieved |
|-----------|--------|----------|
| User Coverage | 9,000+ users |  9,340 users |
| F1 Score | >0.80 |  0.851 |
| AUC-ROC | >0.90 |  0.994 |
| Dashboard Load Time | <3 seconds |  <2 seconds |
| Business Insights | Quantifiable ROI |  $121,887 identified |

---

## 2. Data Collection Strategy

**Data Sources & Architecture:**
Raw Data Generation
↓
PostgreSQL Database (pgAdmin 4)
↓
SQL-based Extraction & Cleaning
↓
Sub-datasets (9 files)
↓
Pandas Aggregation
↓
Final Analytical Datasets

**Data Generation Process:**
- Synthetic data created using `dataset.py`
- 9,340 users simulated with 146,194 session records
- Seasonality and lifecycle patterns incorporated

**Database Management:**
- Raw data imported into PostgreSQL
- Normalized tables with indexing on `user_id` and `date`
- Explored and validated using pgAdmin 4

---

## 3. Data Cleaning Pipeline

### SQL-Based Cleaning

**Phase 1: Data Validation**
```sql
-- Remove duplicates
DELETE FROM sessions
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM sessions
    GROUP BY user_id, date, session_id
);

-- Handle NULL values
UPDATE sessions
SET session_duration = 0
WHERE session_duration IS NULL;

-- Fix data types
ALTER TABLE sessions
ALTER COLUMN date TYPE DATE USING date::DATE;
```

**Phase 2: Data Segmentation**
- 9 specialized sub-datasets (demographics, session metrics, retention, engagement patterns, churn indicators, channel performance, device analytics, temporal trends, user segments)

### Pandas-Based Cleaning

**Missing Data Handling:**
```python
# Session duration
mobile_df['session_duration'].fillna(
    mobile_df.groupby('user_segment')['session_duration'].transform('median'),
    inplace=True
)

# Categorical
mobile_df['user_acquisition_channel'].fillna('unknown', inplace=True)
```

**Outlier Treatment (IQR Method):**
```python
Q1 = mobile_df['session_duration'].quantile(0.25)
Q3 = mobile_df['session_duration'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR

mobile_df['session_duration'] = mobile_df['session_duration'].clip(
    lower=max(0, lower_bound),
    upper=upper_bound
)
```

---

## 4. Exploratory Data Analysis

### Univariate Analysis
- **Session Duration:** Mean: 72.5 min, Median: 45.2 min, Std Dev: 58.3 min
- **User Segmentation:** Casual 37.9%, Regular 37.1%, Power 16.3%, Churned 8.7%

### Bivariate Analysis
- **Retention vs Session Duration:** Pearson r = 0.72 → longer sessions → higher retention
- **Device Type Impact:** iOS users slightly higher retention (63.8%) vs Android (58.5%)

### Multivariate Analysis
- **Cohort Retention:** Drops sharply after Day 7 (Day 1: 96.1%, Day 90: 45.2%)
- **Channel Performance:** Top channels → App Store, Paid Social, Organic

---

## 5. Feature Engineering Process

**User-Level Aggregation (25 features per user):**
- Session metrics: mean, std, min, max, sum of session duration
- Retention metrics: mean, min, max retention rate
- Engagement metrics: total app opens, average screens viewed
- Temporal features: total active days, activity frequency
- Categorical encodings: device type, acquisition channel, user segment (one-hot encoded)

**Churn Definition:**
A user is labeled churned if their last recorded session was more than 30 days before the most recent date in the dataset — a standard industry definition.

```python
max_date = mobile_df['date'].max()
cutoff_date = max_date - pd.Timedelta(days=30)
last_seen['churned'] = (last_seen['last_seen_date'] < cutoff_date).astype(int)
```

---

## 6. Machine Learning Model Development

### Model Selection Process

**Models Tested:**
```python
# Cross-validation results (5-fold):
# Logistic Regression: 78.2% ± 2.1%
# Random Forest:       85.3% ± 1.8%  ← SELECTED
# Gradient Boosting:   83.7% ± 2.3%
# XGBoost:             84.9% ± 1.9%
```

**Selection Rationale:**
- Random Forest provided best F1 score
- Most stable across folds (low std dev)
- Naturally handles feature interactions
- Provides interpretable feature importance
- Less prone to overfitting than XGBoost

### Class Imbalance Handling

With only 5.4% of users churning, a naive model would predict "not churned" for everyone and still achieve high accuracy while being completely useless. We solved this using `class_weight='balanced'`:

```python
model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',  # Penalizes missing churners proportionally
    random_state=42
)
```

This automatically weights the minority class (churners) ~18x higher than the majority class, forcing the model to actually learn to detect churners.

### Training Process

**Data Split:**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y  # Maintain class distribution
)
# Training set: 6,538 users
# Test set:     2,802 users
```

### Model Evaluation

**Performance Metrics (Test Set):**

| Metric | Value |
|--------|-------|
| Accuracy | 98.5% |
| F1 Score | 0.851 |
| AUC-ROC | 0.994 |
| Precision | 0.92 |
| Recall | 0.79 |

**Full Classification Report:**
          precision    recall  f1-score   support
Not Churned       0.99      1.00      0.99      2651
Churned       0.92      0.79      0.85       151
accuracy                           0.99      2802
macro avg       0.95      0.90      0.92      2802
weighted avg       0.98      0.99      0.98      2802

**ROC-AUC Interpretation:**
An AUC-ROC of 0.994 means the model has near-perfect ability to separate churners from loyal users — far above the 0.5 baseline of random guessing.

**Top 5 Churn Drivers (Feature Importance):**
1. `avg_retention_rate` — strongest single predictor
2. `active_days` — habit formation is critical
3. `total_sessions` — low engagement signals early churn
4. `avg_session_duration` — short sessions = low value found
5. `total_app_opens` — early disengagement signal

---

## 7. Dashboard Architecture

**Design Philosophy:**
The dashboard tells a business story in 5 acts rather than just displaying charts:
ACT 1 → What is the problem?
ACT 2 → Who is churning?
ACT 3 → Why are they churning?
ACT 4 → How accurately can we predict churn?
ACT 5 → What should the business do?

**Technical Implementation:**
- Built with Plotly Dash
- Dark professional theme (#0f1923 background)
- Each section answers a business question
- 💡 Insight boxes provide plain-English interpretation
- Deployed on Render (auto-deploys from GitHub)

---

## 8. Statistical Methods

- **Retention Rate:** `(users_active_day_n / users_active_day_0) * 100`
- **Churn Rate:** `100 - retention_rate`
- **Growth Rate:** `dau_growth = dua_df['dau'].pct_change() * 100`
- **Statistical Significance:** t-test for iOS vs Android retention → p=0.03 (<0.05)

---

## 9. Validation & Testing

**Data Quality Checks:** No duplicates, valid dates, positive metrics, valid categories

**Model Validation:**
- 70/30 train/test split with stratification
- class_weight='balanced' for imbalance handling
- Evaluated on F1, AUC-ROC, Precision, Recall — not just accuracy
- Charts saved: confusion matrix, ROC curve, feature importance

**Dashboard Testing:** Tested locally before deploying to Render

---

## 10. Assumptions & Limitations

**Assumptions:**
- Synthetic data represents real user behaviour
- Churn defined as 30+ days inactive (industry standard)
- Features relatively independent
- class_weight='balanced' sufficient for imbalance handling

**Limitations:**
- Synthetic rather than real-world data
- Model predicts probability, not certainty
- External factors (marketing, product updates) not included
- Free tier hosting causes cold-start delay (~1 min)

---

## 11. Future Improvements

- Real-time data streaming
- Time-series forecasting and CLV prediction
- Advanced user segmentation (RFM analysis)
- Automated alerts for high-risk users
- A/B test analytics integration
- Authenticated dashboard access

---

## 12. References & Technologies Used

- **Database:** PostgreSQL + pgAdmin 4
- **Programming:** Python 3.8+
- **ML Framework:** Scikit-learn (Random Forest, class_weight='balanced')
- **Visualization:** Plotly Dash, Matplotlib, Seaborn
- **Data Processing:** Pandas, NumPy, Joblib
- **Deployment:** Render (auto-deploy from GitHub)
- **Version Control:** Git + GitHub
- **Methodology:** CRISP-DM framework
