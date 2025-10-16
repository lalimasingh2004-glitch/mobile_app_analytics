# metrics_extractor.py
import pandas as pd

print("📊 Extracting Key Metrics for Presentation...\n")

# Load data
dua_df = pd.read_csv("data/advanced_dua.csv")
ret_df = pd.read_csv("data/advanced_retention.csv")
mobile_df = pd.read_csv("data/mobile_analytics.csv")

dua_df['date'] = pd.to_datetime(dua_df['date'])
mobile_df['date'] = pd.to_datetime(mobile_df['date'])
ret_df['first_date'] = pd.to_datetime(ret_df['first_date'])

# Calculate key metrics
print("=" * 60)
print("KEY METRICS FOR PRESENTATION")
print("=" * 60)

print("\n📱 USER ENGAGEMENT METRICS:")
print(f"  • Average Daily Active Users: {dua_df['dau'].mean():,.0f}")
print(f"  • Peak DAU: {dua_df['dau'].max():,.0f}")
print(f"  • Average Session Duration: {dua_df['avg_session_duration'].mean():.1f} minutes")
print(f"  • Total App Opens: {mobile_df['app_opens'].sum():,.0f}")
print(f"  • Avg Screens per Session: {dua_df['avg_screens_per_session'].mean():.1f}")

print("\n🔄 RETENTION METRICS:")
print(f"  • Average Retention Rate: {ret_df['retention_rate'].mean():.1f}%")
print(f"  • Average Churn Rate: {ret_df['churn_rate'].mean():.1f}%")
print(f"  • Best Retention Period: {ret_df['retention_rate'].max():.1f}%")

print("\n👥 USER SEGMENTS:")
segment_stats = mobile_df.groupby('user_segment').agg({
    'session_duration': 'mean',
    'screens_viewed': 'mean',
    'user_id': 'nunique'
}).round(1)
print(segment_stats)

print("\n📱 DEVICE BREAKDOWN:")
device_stats = mobile_df.groupby('device_type')['user_id'].nunique()
print(device_stats)

print("\n🎯 ACQUISITION CHANNELS:")
channel_stats = mobile_df.groupby('user_acquisition_channel').agg({
    'session_duration': 'mean',
    'user_id': 'nunique'
}).round(1)
print(channel_stats)

print("\n💡 GROWTH TRENDS:")
dua_df['dau_growth'] = dua_df['dau'].pct_change() * 100
print(f"  • Average DAU Growth Rate: {dua_df['dau_growth'].mean():.2f}%")
print(f"  • Peak Growth Rate: {dua_df['dau_growth'].max():.2f}%")

print("\n" + "=" * 60)
print("Metrics extracted successfully!")