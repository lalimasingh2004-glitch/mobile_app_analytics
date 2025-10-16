# business_impact_calculator.py
import pandas as pd

print("💰 CALCULATING BUSINESS IMPACT PROJECTIONS\n")

# Load your data
mobile_df = pd.read_csv("data/mobile_analytics.csv")
ret_df = pd.read_csv("data/advanced_retention.csv")

# ========== ASSUMPTIONS (ADJUST THESE) ==========
AVERAGE_REVENUE_PER_USER_MONTHLY = 10  # $ per user per month
CUSTOMER_ACQUISITION_COST = 25  # $ per new user
HIGH_VALUE_USER_MONTHLY_REVENUE = 30  # $ per month

total_users = mobile_df['user_id'].nunique()
current_retention = ret_df['retention_rate'].mean()
current_churn = ret_df['churn_rate'].mean()

print("=" * 60)
print("CURRENT STATE")
print("=" * 60)
print(f"Total Users: {total_users:,}")
print(f"Current Retention Rate: {current_retention:.1f}%")
print(f"Current Churn Rate: {current_churn:.1f}%")
print(f"Monthly Churning Users: {int(total_users * current_churn / 100):,}")

print("\n" + "=" * 60)
print("SCENARIO 1: 5% RETENTION IMPROVEMENT")
print("=" * 60)
new_retention = current_retention + 5
users_saved = int(total_users * 0.05)
revenue_impact = users_saved * AVERAGE_REVENUE_PER_USER_MONTHLY * 12
cac_saved = users_saved * CUSTOMER_ACQUISITION_COST

print(f"New Retention Rate: {new_retention:.1f}%")
print(f"Additional Retained Users: {users_saved:,}")
print(f"Annual Revenue Impact: ${revenue_impact:,}")
print(f"CAC Saved: ${cac_saved:,}")
print(f"TOTAL BENEFIT: ${revenue_impact + cac_saved:,}")

print("\n" + "=" * 60)
print("SCENARIO 2: TARGET HIGH-RISK USERS")
print("=" * 60)
# Assume 10% of users are high-risk
high_risk_users = int(total_users * 0.10)
# If we save 50% of them
users_saved_from_churn = int(high_risk_users * 0.50)
revenue_at_risk = high_risk_users * AVERAGE_REVENUE_PER_USER_MONTHLY * 12
revenue_saved = users_saved_from_churn * AVERAGE_REVENUE_PER_USER_MONTHLY * 12
intervention_cost = high_risk_users * 2  # $2 per user for campaign

print(f"High-Risk Users Identified: {high_risk_users:,}")
print(f"Revenue at Risk (annual): ${revenue_at_risk:,}")
print(f"Users Saved (50% success): {users_saved_from_churn:,}")
print(f"Revenue Saved: ${revenue_saved:,}")
print(f"Intervention Cost: ${intervention_cost:,}")
print(f"NET BENEFIT: ${revenue_saved - intervention_cost:,}")

print("\n" + "=" * 60)
print("SCENARIO 3: USER SEGMENT UPGRADE")
print("=" * 60)
# Get medium value users
segment_dist = mobile_df['user_segment'].value_counts()
medium_users = segment_dist.get('Medium Value', 0)
# Assume 20% can be upgraded to high value
upgradeable = int(medium_users * 0.20)
revenue_uplift = upgradeable * (HIGH_VALUE_USER_MONTHLY_REVENUE - AVERAGE_REVENUE_PER_USER_MONTHLY) * 12

print(f"Medium Value Users: {medium_users:,}")
print(f"Upgradeable Users (20%): {upgradeable:,}")
print(f"Annual Revenue Uplift: ${revenue_uplift:,}")

print("\n" + "=" * 60)
print("TOTAL POTENTIAL ANNUAL IMPACT")
print("=" * 60)
total_impact = (revenue_impact + cac_saved) + (revenue_saved - intervention_cost) + revenue_uplift
print(f"💰 TOTAL: ${total_impact:,}")
print("=" * 60)