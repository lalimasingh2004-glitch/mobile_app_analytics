import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import uuid

class MobileAnalyticsGenerator:
    def __init__(self, seed=42):
        """Generate realistic mobile app analytics data"""
        np.random.seed(seed)
        random.seed(seed)
        self.fake = Faker()
        Faker.seed(seed)
        
        # App characteristics
        self.app_name = "FitTracker Pro"
        self.app_category = "Health & Fitness"
        
        # User behavior patterns
        self.user_segments = {
            'power_users': 0.15,      # 15% highly engaged
            'regular_users': 0.35,    # 35% moderately engaged  
            'casual_users': 0.35,     # 35% low engagement
            'churned_users': 0.15     # 15% barely active
        }
        
        # Device distribution (realistic mobile market share)
        self.device_distribution = {
            'Android': 0.72,
            'iOS': 0.28
        }
        
        # Acquisition channels
        self.acquisition_channels = {
            'organic': 0.35,
            'paid_social': 0.20,
            'app_store': 0.15,
            'paid_search': 0.12,
            'referral': 0.08,
            'email': 0.05,
            'direct': 0.05
        }
    
    def generate_users(self, num_users=50000):
        """Generate user base with realistic characteristics"""
        users = []
        
        for i in range(num_users):
            # Determine user segment
            segment_rand = random.random()
            if segment_rand < 0.15:
                segment = 'power_users'
            elif segment_rand < 0.50:
                segment = 'regular_users'
            elif segment_rand < 0.85:
                segment = 'casual_users'
            else:
                segment = 'churned_users'
            
            # Generate user characteristics based on segment
            user = {
                'user_id': f"user_{str(uuid.uuid4())[:8]}",
                'segment': segment,
                'device_type': np.random.choice(
                    list(self.device_distribution.keys()),
                    p=list(self.device_distribution.values())
                ),
                'acquisition_channel': np.random.choice(
                    list(self.acquisition_channels.keys()),
                    p=list(self.acquisition_channels.values())
                ),
                'install_date': self.fake.date_between(
                    start_date='-365d', end_date='-30d'
                ),
                'country': self.fake.country_code(),
                'age_group': np.random.choice(
                    ['18-24', '25-34', '35-44', '45-54', '55+'],
                    p=[0.25, 0.35, 0.25, 0.10, 0.05]
                )
            }
            users.append(user)
        
        return pd.DataFrame(users)
    
    def generate_daily_activities(self, users_df, start_date, end_date):
        """Generate daily user activities"""
        activities = []
        
        # Convert dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        for current_date in pd.date_range(start, end):
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Weekend effect (higher usage on weekends)
            is_weekend = current_date.weekday() >= 5
            weekend_multiplier = 1.3 if is_weekend else 1.0
            
            for _, user in users_df.iterrows():
                # Determine if user is active today based on segment
                segment = user['segment']
                
                # Activity probability by segment
                activity_probs = {
                    'power_users': 0.85 * weekend_multiplier,
                    'regular_users': 0.45 * weekend_multiplier,
                    'casual_users': 0.15 * weekend_multiplier,
                    'churned_users': 0.02
                }
                
                # Check if user installed app before this date
                install_date = pd.to_datetime(user['install_date'])
                if current_date < install_date:
                    continue
                
                # Days since install affects retention
                days_since_install = (current_date - install_date).days
                retention_decay = max(0.1, 1 - (days_since_install * 0.002))
                
                final_activity_prob = activity_probs[segment] * retention_decay
                
                if random.random() < final_activity_prob:
                    # User is active today - generate session data
                    session_data = self._generate_session_data(user, date_str, segment)
                    activities.extend(session_data)
        
        return pd.DataFrame(activities)
    
    def _generate_session_data(self, user, date_str, segment):
        """Generate session data for an active user"""
        sessions = []
        
        # Number of sessions per day by segment
        session_counts = {
            'power_users': np.random.poisson(4) + 1,
            'regular_users': np.random.poisson(2) + 1,
            'casual_users': np.random.poisson(1) + 1,
            'churned_users': 1
        }
        
        num_sessions = min(session_counts[segment], 8)  # Cap at 8 sessions
        
        for session in range(num_sessions):
            # Session duration varies by segment (minutes)
            duration_ranges = {
                'power_users': (8, 45),
                'regular_users': (3, 20),
                'casual_users': (1, 8),
                'churned_users': (0.5, 3)
            }
            
            min_dur, max_dur = duration_ranges[segment]
            session_duration = np.random.uniform(min_dur, max_dur)
            
            # Screens viewed correlates with session duration
            screens_viewed = max(1, int(session_duration / 2) + np.random.poisson(1))
            
            # App opens (first session of day counts as app open)
            app_opens = 1 if session == 0 else 0
            
            session_data = {
                'user_id': user['user_id'],
                'date': date_str,
                'session_duration': round(session_duration, 2),
                'screens_viewed': screens_viewed,
                'app_opens': app_opens,
                'device_type': user['device_type'],
                'user_acquisition_channel': user['acquisition_channel'],
                'user_segment': segment
            }
            
            sessions.append(session_data)
        
        return sessions
    
    def calculate_metrics(self, activities_df, users_df):
        """Calculate key metrics and add to dataset"""
        # Group by user and date for daily aggregations
        daily_user_data = activities_df.groupby(['user_id', 'date']).agg({
            'session_duration': 'sum',
            'screens_viewed': 'sum', 
            'app_opens': 'sum',
            'device_type': 'first',
            'user_acquisition_channel': 'first',
            'user_segment': 'first'
        }).reset_index()
        
        # Calculate DAU by date
        daily_active_users = activities_df.groupby('date')['user_id'].nunique().reset_index()
        daily_active_users.columns = ['date', 'daily_active_users']
        
        # Merge DAU back to user data
        daily_user_data = daily_user_data.merge(daily_active_users, on='date')
        
        # Calculate retention rates by cohort
        retention_data = self._calculate_retention(activities_df, users_df)
        daily_user_data = daily_user_data.merge(retention_data, on='date', how='left')
        
        # Fill missing retention rates
        daily_user_data['retention_rate'] = daily_user_data['retention_rate'].fillna(
            daily_user_data.groupby('user_segment')['retention_rate'].transform('mean')
        )
        
        return daily_user_data
    
    def _calculate_retention(self, activities_df, users_df):
        """Calculate retention rates by date"""
        retention_rates = []
        
        # Get unique dates
        dates = sorted(activities_df['date'].unique())
        
        for date in dates:
            current_date = pd.to_datetime(date)
            
            # Users who could be active (installed before this date)
            eligible_users = users_df[
                pd.to_datetime(users_df['install_date']) <= current_date
            ]
            
            # Users who were actually active
            active_users = activities_df[
                activities_df['date'] == date
            ]['user_id'].unique()
            
            # Calculate retention
            if len(eligible_users) > 0:
                retention_rate = (len(active_users) / len(eligible_users)) * 100
            else:
                retention_rate = 0
                
            retention_rates.append({
                'date': date,
                'retention_rate': round(retention_rate, 2)
            })
        
        return pd.DataFrame(retention_rates)
    
    def generate_complete_dataset(self, num_users=50000, days=90):
        """Generate complete realistic mobile analytics dataset"""
        print(f"Generating dataset for {num_users:,} users over {days} days...")
        
        # Generate users
        print("1. Generating user base...")
        users_df = self.generate_users(num_users)
        
        # Generate date range (last N days)
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Generate activities
        print("2. Generating daily activities...")
        activities_df = self.generate_daily_activities(users_df, start_date, end_date)
        
        # Calculate metrics
        print("3. Calculating metrics...")
        final_dataset = self.calculate_metrics(activities_df, users_df)
        
        # Add some realistic noise and edge cases
        final_dataset = self._add_realistic_variations(final_dataset)
        
        print(f"✅ Dataset generated: {len(final_dataset):,} records")
        print(f"📊 Date range: {final_dataset['date'].min()} to {final_dataset['date'].max()}")
        print(f"👥 Unique users: {final_dataset['user_id'].nunique():,}")
        print(f"📱 Device split: {final_dataset['device_type'].value_counts().to_dict()}")
        
        return final_dataset
    
    def _add_realistic_variations(self, df):
        """Add realistic data variations and edge cases"""
        # Add some missing data (realistic scenario)
        missing_indices = np.random.choice(
            df.index, 
            size=int(len(df) * 0.02),  # 2% missing data
            replace=False
        )
        df.loc[missing_indices, 'user_acquisition_channel'] = 'unknown'
        
        # Add some outliers (power users with extreme usage)
        power_user_indices = df[df['user_segment'] == 'power_users'].index
        outlier_indices = np.random.choice(
            power_user_indices,
            size=int(len(power_user_indices) * 0.05),
            replace=False
        )
        
        # Extreme session durations for outliers
        df.loc[outlier_indices, 'session_duration'] *= np.random.uniform(2, 5, size=len(outlier_indices))
        df.loc[outlier_indices, 'screens_viewed'] *= np.random.randint(2, 4, size=len(outlier_indices))
        
        return df

# Usage Example
def main():
    # Initialize generator
    generator = MobileAnalyticsGenerator(seed=42)
    
    # Generate dataset
    # Small dataset for testing: 1,000 users, 30 days
    # Medium dataset: 10,000 users, 60 days  
    # Large dataset: 50,000 users, 90 days
    
    dataset = generator.generate_complete_dataset(
        num_users=10000,  # Adjust based on your needs
        days=60
    )
    
    # Save to CSV
    filename = "mobile_analytics.csv"
    dataset.to_csv(filename, index=False)
    print(f"\n💾 Dataset saved as '{filename}'")
    
    # Display sample and statistics
    print("\n📋 Sample data:")
    print(dataset.head(10))
    
    print("\n📊 Dataset summary:")
    print(dataset.describe())
    
    print("\n🎯 Column overview:")
    for col in dataset.columns:
        print(f"  • {col}: {dataset[col].dtype} ({dataset[col].nunique()} unique values)")
    
    return dataset

if __name__ == "__main__":
    
    dataset = main()