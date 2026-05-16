import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve, f1_score,
    ConfusionMatrixDisplay
)

print("=" * 50)
print("STEP 1: Loading raw data...")
print("=" * 50)

df = pd.read_csv("data/mobile_analytics.csv")
df['date'] = pd.to_datetime(df['date'])
print(f" Loaded {len(df)} rows, {df['user_id'].nunique()} users")

# ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 2: Defining Churn...")
print("=" * 50)

max_date = df['date'].max()
cutoff_date = max_date - pd.Timedelta(days=30)
print(f"Max date: {max_date.date()}")
print(f"Churn cutoff: {cutoff_date.date()}")
print("(Users last seen before cutoff = churned)")

last_seen = df.groupby('user_id')['date'].max().reset_index()
last_seen.columns = ['user_id', 'last_seen_date']
last_seen['churned'] = (last_seen['last_seen_date'] < cutoff_date).astype(int)

print(f"\n Churn distribution:")
print(last_seen['churned'].value_counts())
print(f"Churn rate: {last_seen['churned'].mean()*100:.1f}%")

# ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 3: Engineering Features Per User...")
print("=" * 50)

features = df.groupby('user_id').agg(
    total_sessions        = ('session_duration', 'count'),
    avg_session_duration  = ('session_duration', 'mean'),
    std_session_duration  = ('session_duration', 'std'),
    total_screens_viewed  = ('screens_viewed', 'sum'),
    avg_screens_viewed    = ('screens_viewed', 'mean'),
    total_app_opens       = ('app_opens', 'sum'),
    avg_app_opens         = ('app_opens', 'mean'),
    avg_retention_rate    = ('retention_rate', 'mean'),
    min_retention_rate    = ('retention_rate', 'min'),
    max_retention_rate    = ('retention_rate', 'max'),
    active_days           = ('date', 'nunique'),
    device_type           = ('device_type', lambda x: x.mode()[0]),
    acquisition_channel   = ('user_acquisition_channel', lambda x: x.mode()[0]),
    user_segment          = ('user_segment', lambda x: x.mode()[0]),
).reset_index()

# Encode categorical columns
features = pd.get_dummies(features, columns=['device_type', 'acquisition_channel', 'user_segment'])

# Merge churn label
features = features.merge(last_seen[['user_id', 'churned']], on='user_id')
features = features.fillna(0)

print(f" Feature matrix shape: {features.shape}")
print(f" Features created: {features.shape[1] - 2} features per user")

# ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 4: Training Model...")
print("=" * 50)

X = features.drop(columns=['user_id', 'churned'])
y = features['churned']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# class_weight='balanced' handles class imbalance automatically
model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)
print(" Model trained with class_weight='balanced'")

# ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 5: Evaluating Model...")
print("=" * 50)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

accuracy  = (y_pred == y_test).mean()
f1        = f1_score(y_test, y_pred)
auc_roc   = roc_auc_score(y_test, y_prob)

print(f"\n RESULTS:")
print(f"  Accuracy  : {accuracy*100:.1f}%")
print(f"  F1 Score  : {f1:.3f}")
print(f"  AUC-ROC   : {auc_roc:.3f}")
print(f"\n Full Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Not Churned', 'Churned']))

# ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("STEP 6: Saving Charts...")
print("=" * 50)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Churn Model Evaluation', fontsize=16, fontweight='bold')

# Chart 1 - Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=['Not Churned', 'Churned'])
disp.plot(ax=axes[0], colorbar=False)
axes[0].set_title('Confusion Matrix')

# Chart 2 - ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
axes[1].plot(fpr, tpr, color='blue', label=f'AUC = {auc_roc:.3f}')
axes[1].plot([0,1], [0,1], 'k--')
axes[1].set_xlabel('False Positive Rate')
axes[1].set_ylabel('True Positive Rate')
axes[1].set_title('ROC Curve')
axes[1].legend()

# Chart 3 - Top 10 Feature Importances
importances = pd.Series(model.feature_importances_, index=X.columns)
top10 = importances.nlargest(10).sort_values()
top10.plot(kind='barh', ax=axes[2], color='steelblue')
axes[2].set_title('Top 10 Churn Drivers')
axes[2].set_xlabel('Importance Score')

plt.tight_layout()
plt.savefig('churn_evaluation_charts.png', dpi=150, bbox_inches='tight')
print(" Charts saved as churn_evaluation_charts.png")

# Save updated model
joblib.dump(model, 'data/Deliverable/churn_prediction_model_v2.pkl')
print(" New model saved as churn_prediction_model_v2.pkl")

print("\n ALL DONE! Check churn_evaluation_charts.png in your project folder")