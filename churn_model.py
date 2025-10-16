# ================================================
# churn_model.py - CORRECTED VERSION
# ================================================
import pandas as pd
import numpy as np
import joblib

# ====================================================
# 1️⃣  Loading trained churn model
# ====================================================
MODEL_PATH = r'C:\Users\sjn17\Downloads\mobile_app_analytics\data\Deliverable\churn_prediction_model.pkl'
model = joblib.load(MODEL_PATH)

# ====================================================
# 2️⃣  Preprocessing function — same logic as in training
# ====================================================
def preprocess_new_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Reproduce the same feature engineering as during training.
    Input: raw user-level data
    Returns: processed DataFrame ready for model.predict()
    """

    # --------------- Convert to datetime ----------------
    raw_df = raw_df.copy()  # Don't modify original
    raw_df["date"] = pd.to_datetime(raw_df["date"], errors="coerce")

    # --------------- Group & aggregate ------------------
    agg_df = (
        raw_df.groupby("user_id")
        .agg(
            {
                "session_duration": ["mean", "std", "min", "max", "sum"],
                "screens_viewed": ["mean", "std", "max", "sum"],
                "app_opens": ["mean", "std", "max", "sum"],
                "retention_rate": ["mean", "min", "max", "std"],
                "daily_active_users": ["mean", "std"],
                "date": "count",
                "device_type": "last",
                "user_acquisition_channel": "last",
                "user_segment": "last",
            }
        )
    )

    # flatten the multi-level column names
    agg_df.columns = [
        "_".join(col) if isinstance(col, tuple) else col for col in agg_df.columns
    ]
    agg_df = agg_df.rename(columns={"date_count": "total_active_days"}).reset_index()

    # --------------- One-hot encoding (same as training) ------------------
    cat_cols = ["device_type_last", "user_acquisition_channel_last", "user_segment_last"]
    agg_df = pd.get_dummies(agg_df, columns=cat_cols, drop_first=True)

    # --------------- Align with model's feature order ---------------------
    expected_features = model.feature_names_in_  # works for sklearn >=1.0
    for col in expected_features:
        if col not in agg_df.columns:
            agg_df[col] = 0  # add missing cols as 0
    
    # Keeping user_id before selecting features
    user_ids = agg_df['user_id'].copy()
    feature_df = agg_df[expected_features]
    
    return feature_df, user_ids

# ====================================================
# 3️⃣  Prediction helper
# ====================================================
def predict_churn(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Accept raw user-level data, preprocess, and return predictions + probabilities
    """
    processed, user_ids = preprocess_new_data(raw_df)
    predictions = model.predict(processed)
    probs = model.predict_proba(processed)[:, 1]

    # Combining with user_id
    result_df = pd.DataFrame({
        "user_id": user_ids,
        "churn_probability": probs,
        "churn_prediction": predictions
    })
    return result_df

# ====================================================
# 4️⃣  Running directly for quick test
# ====================================================
if __name__ == "__main__":
    print("🔍 Loading test data...")
    test_data = pd.read_csv("data/mobile_analytics.csv")

    print("⚙️  Running churn predictions...")
    results = predict_churn(test_data)

    print("✅ Predictions complete. Sample output:")
    print(results[["user_id", "churn_probability", "churn_prediction"]].head())
    print(f"\nTotal users analyzed: {len(results)}")
    print(f"Predicted churners: {results['churn_prediction'].sum()}")
    print(f"Average churn probability: {results['churn_probability'].mean():.2%}")