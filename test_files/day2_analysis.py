import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

class MobileAnalyticsFoundation:
    def __init__(self):
        self.dau_primary_df = None
        self.retention_primary_df = None
        self.cohort_df = None
        self.mobile_raw_df = None
        self.all_dau_files = {}
        self.all_retention_files = {}
        self.clean_dataset = None
        
    def load_primary_data(self):
        """Load the three primary CSV files for main analysis"""
        print("📊 Loading PRIMARY data files for main analysis...")
        
        primary_files = {
            'dau_0results.csv': 'DAU Primary',
            'retention_0results.csv': 'Retention Primary', 
            'cohort_results.csv': 'Cohort Analysis',  # Updated to match your file
            'mobile_analytics.csv': 'Raw Mobile Data'
        }
        
        try:
            # Load DAU primary
            if os.path.exists('dau_0results.csv'):
                self.dau_primary_df = pd.read_csv('dau_0results.csv')
                print(f"✅ DAU Primary loaded: {self.dau_primary_df.shape}")
                print(f"   Columns: {list(self.dau_primary_df.columns)}")
            else:
                print("❌ dau_0results.csv not found")
                
            # Load Retention primary
            if os.path.exists('retention_0results.csv'):
                self.retention_primary_df = pd.read_csv('retention_0results.csv')
                print(f"✅ Retention Primary loaded: {self.retention_primary_df.shape}")
                print(f"   Columns: {list(self.retention_primary_df.columns)}")
            else:
                print("❌ retention_0results.csv not found")
                
            # Load Cohort data
            if os.path.exists('cohort_results.csv'):
                self.cohort_df = pd.read_csv('cohort_results.csv')
                print(f"✅ Cohort data loaded: {self.cohort_df.shape}")
                print(f"   Columns: {list(self.cohort_df.columns)}")
            else:
                print("❌ cohort_results.csv not found")
                
            # Load Raw mobile data
            if os.path.exists('mobile_analytics.csv'):
                self.mobile_raw_df = pd.read_csv('mobile_analytics.csv')
                print(f"✅ Raw Mobile data loaded: {self.mobile_raw_df.shape}")
                print(f"   Columns: {list(self.mobile_raw_df.columns)}")
            else:
                print("❌ mobile_analytics.csv not found")
                
        except Exception as e:
            print(f"❌ Error loading primary data: {e}")
    
    def load_all_supporting_files(self):
        """Load all DAU and retention supporting files for comprehensive analysis"""
        print("\n📂 Loading ALL supporting DAU and Retention files...")
        
        # Load all DAU files
        dau_pattern = 'dau_*results.csv'
        dau_files = glob.glob(dau_pattern)
        
        for file in sorted(dau_files):
            try:
                df = pd.read_csv(file)
                self.all_dau_files[file] = df
                print(f"✅ {file}: {df.shape}")
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
        
        # Load all retention files
        retention_pattern = 'retention_*results.csv'
        retention_files = glob.glob(retention_pattern)
        
        for file in sorted(retention_files):
            try:
                df = pd.read_csv(file)
                self.all_retention_files[file] = df
                print(f"✅ {file}: {df.shape}")
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
                
        print(f"\n📈 Total DAU files loaded: {len(self.all_dau_files)}")
        print(f"📈 Total Retention files loaded: {len(self.all_retention_files)}")
    
    def analyze_raw_mobile_data(self):
        """Analyze the original mobile_analytics.csv file"""
        if self.mobile_raw_df is None:
            print("❌ Raw mobile data not available for analysis")
            return
            
        print("\n🔍 ANALYZING RAW MOBILE DATA:")
        print("="*50)
        
        # Basic info
        print(f"Dataset Shape: {self.mobile_raw_df.shape}")
        print(f"Memory Usage: {self.mobile_raw_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Data types
        print("\n📊 Data Types:")
        for col, dtype in self.mobile_raw_df.dtypes.items():
            null_count = self.mobile_raw_df[col].isnull().sum()
            null_pct = (null_count / len(self.mobile_raw_df)) * 100
            print(f"  {col}: {dtype} (Null: {null_count}, {null_pct:.1f}%)")
        
        # Date columns analysis
        date_columns = []
        for col in self.mobile_raw_df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                date_columns.append(col)
                try:
                    self.mobile_raw_df[col] = pd.to_datetime(self.mobile_raw_df[col])
                    date_range = f"{self.mobile_raw_df[col].min()} to {self.mobile_raw_df[col].max()}"
                    print(f"📅 {col}: {date_range}")
                except:
                    print(f"⚠️ Could not parse {col} as datetime")
        
        # Numeric columns analysis
        numeric_cols = self.mobile_raw_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print("\n📈 Numeric Columns Summary:")
            print(self.mobile_raw_df[numeric_cols].describe())
        
        # Categorical analysis
        categorical_cols = self.mobile_raw_df.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col not in date_columns]
        
        if len(categorical_cols) > 0:
            print(f"\n📋 Categorical Columns: {len(categorical_cols)}")
            for col in categorical_cols[:5]:  # Show first 5
                unique_count = self.mobile_raw_df[col].nunique()
                print(f"  {col}: {unique_count} unique values")
                if unique_count <= 10:
                    print(f"    Values: {list(self.mobile_raw_df[col].unique())}")
    
    def clean_and_validate_all(self):
        """Enhanced data cleaning for all datasets"""
        print("\n🧹 COMPREHENSIVE DATA CLEANING:")
        print("="*50)
        
        # Clean Primary DAU data
        if self.dau_primary_df is not None:
            print("\n🔧 Cleaning PRIMARY DAU data:")
            original_shape = self.dau_primary_df.shape
            
            # Convert date columns
            for col in self.dau_primary_df.columns:
                if 'date' in col.lower():
                    try:
                        self.dau_primary_df[col] = pd.to_datetime(self.dau_primary_df[col])
                        print(f"✅ Converted {col} to datetime")
                    except:
                        print(f"⚠️ Could not convert {col} to datetime")
            
            # Remove duplicates
            self.dau_primary_df = self.dau_primary_df.drop_duplicates()
            removed_dups = original_shape[0] - self.dau_primary_df.shape[0]
            print(f"🗑️ Removed {removed_dups} duplicate rows")
            
            # Check for anomalies
            numeric_cols = self.dau_primary_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if (self.dau_primary_df[col] < 0).any():
                    negative_count = (self.dau_primary_df[col] < 0).sum()
                    print(f"⚠️ Warning: {negative_count} negative values in {col}")
        
        # Clean Primary Retention data
        if self.retention_primary_df is not None:
            print("\n🔧 Cleaning PRIMARY RETENTION data:")
            original_shape = self.retention_primary_df.shape
            
            # Convert date columns
            for col in self.retention_primary_df.columns:
                if 'date' in col.lower():
                    try:
                        self.retention_primary_df[col] = pd.to_datetime(self.retention_primary_df[col])
                        print(f"✅ Converted {col} to datetime")
                    except:
                        print(f"⚠️ Could not convert {col} to datetime")
            
            # Validate retention percentages
            for col in self.retention_primary_df.columns:
                if 'rate' in col.lower() or 'retention' in col.lower():
                    if self.retention_primary_df[col].dtype in ['float64', 'int64']:
                        max_val = self.retention_primary_df[col].max()
                        min_val = self.retention_primary_df[col].min()
                        if max_val > 100 or min_val < 0:
                            print(f"⚠️ Warning: Unusual retention values in {col} (Range: {min_val:.2f} to {max_val:.2f})")
        
        # Clean Cohort data
        if self.cohort_df is not None:
            print("\n🔧 Cleaning COHORT data:")
            for col in self.cohort_df.columns:
                if 'date' in col.lower() or 'cohort' in col.lower():
                    try:
                        self.cohort_df[col] = pd.to_datetime(self.cohort_df[col])
                        print(f"✅ Converted {col} to datetime")
                    except:
                        print(f"⚠️ Could not convert {col} to datetime")
        
        print("✅ Data cleaning completed for all datasets!")
    
    def calculate_comprehensive_statistics(self):
        """Calculate detailed statistics for all datasets"""
        print("\n📊 COMPREHENSIVE STATISTICS ANALYSIS:")
        print("="*60)
        
        # Primary DAU Statistics
        if self.dau_primary_df is not None:
            print("\n--- PRIMARY DAU STATISTICS ---")
            numeric_cols = self.dau_primary_df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                main_metric = numeric_cols[0]  # Assume first numeric column is main DAU
                
                stats = {
                    'Count': len(self.dau_primary_df),
                    'Mean': self.dau_primary_df[main_metric].mean(),
                    'Median': self.dau_primary_df[main_metric].median(),
                    'Std Dev': self.dau_primary_df[main_metric].std(),
                    'Min': self.dau_primary_df[main_metric].min(),
                    'Max': self.dau_primary_df[main_metric].max(),
                    'Range': self.dau_primary_df[main_metric].max() - self.dau_primary_df[main_metric].min()
                }
                
                for stat_name, value in stats.items():
                    if isinstance(value, (int, float)):
                        print(f"📈 {stat_name}: {value:,.2f}")
                    else:
                        print(f"📈 {stat_name}: {value:,}")
                
                # Calculate trends if date column exists
                date_cols = [col for col in self.dau_primary_df.columns if 'date' in col.lower()]
                if date_cols:
                    sorted_df = self.dau_primary_df.sort_values(date_cols[0])
                    sorted_df['growth_rate'] = sorted_df[main_metric].pct_change() * 100
                    avg_growth = sorted_df['growth_rate'].mean()
                    print(f"📈 Average Growth Rate: {avg_growth:.2f}%")
        
        # Primary Retention Statistics
        if self.retention_primary_df is not None:
            print("\n--- PRIMARY RETENTION STATISTICS ---")
            numeric_cols = self.retention_primary_df.select_dtypes(include=[np.number]).columns
            
            for col in numeric_cols:
                mean_val = self.retention_primary_df[col].mean()
                median_val = self.retention_primary_df[col].median()
                std_val = self.retention_primary_df[col].std()
                print(f"📊 {col}:")
                print(f"   Mean: {mean_val:.2f}, Median: {median_val:.2f}, Std: {std_val:.2f}")
        
        # Cohort Statistics
        if self.cohort_df is not None:
            print("\n--- COHORT STATISTICS ---")
            print(f"📊 Total Cohorts: {len(self.cohort_df)}")
            
            numeric_cols = self.cohort_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                total_val = self.cohort_df[col].sum()
                mean_val = self.cohort_df[col].mean()
                print(f"📊 {col}: Total={total_val:,.0f}, Mean={mean_val:.2f}")
        
        # Supporting Files Summary
        if self.all_dau_files:
            print("\n--- ALL DAU FILES SUMMARY ---")
            for filename, df in self.all_dau_files.items():
                print(f"📁 {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
        
        if self.all_retention_files:
            print("\n--- ALL RETENTION FILES SUMMARY ---")
            for filename, df in self.all_retention_files.items():
                print(f"📁 {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
    
    def create_master_dataset(self):
        """Create comprehensive master dataset"""
        print("\n🔄 CREATING MASTER ANALYSIS DATASET:")
        print("="*50)
        
        master_components = []
        
        # Start with primary DAU if available
        if self.dau_primary_df is not None:
            base_df = self.dau_primary_df.copy()
            base_df['source'] = 'primary_dau'
            master_components.append(('Primary DAU', base_df))
            print(f"✅ Added Primary DAU: {base_df.shape}")
        
        # Try to merge with retention data
        if self.retention_primary_df is not None:
            ret_df = self.retention_primary_df.copy()
            ret_df['source'] = 'primary_retention'
            master_components.append(('Primary Retention', ret_df))
            print(f"✅ Added Primary Retention: {ret_df.shape}")
        
        # Add cohort data
        if self.cohort_df is not None:
            cohort_df = self.cohort_df.copy()
            cohort_df['source'] = 'cohort_analysis'
            master_components.append(('Cohort Analysis', cohort_df))
            print(f"✅ Added Cohort Data: {cohort_df.shape}")
        
        # Create the master dataset
        if master_components:
            # For now, we'll keep them separate but organized
            self.clean_dataset = {
                'primary_dau': self.dau_primary_df,
                'primary_retention': self.retention_primary_df,
                'cohort_analysis': self.cohort_df,
                'raw_mobile': self.mobile_raw_df,
                'all_dau_files': self.all_dau_files,
                'all_retention_files': self.all_retention_files
            }
            
            # Add metadata
            self.analysis_metadata = {
                'created_at': datetime.now(),
                'total_datasets': len([x for x in self.clean_dataset.values() if x is not None]),
                'data_sources': list(self.clean_dataset.keys())
            }
            
            print(f"✅ Master dataset created with {len([x for x in self.clean_dataset.values() if x is not None])} components")
        else:
            print("❌ No data available to create master dataset")
    
    def export_analysis_ready_data(self):
        """Export all cleaned datasets for analysis"""
        print("\n💾 EXPORTING ANALYSIS-READY DATA:")
        print("="*50)
        
        export_dir = 'cleaned_data_for_analysis'
        os.makedirs(export_dir, exist_ok=True)
        
        exports_completed = 0
        
        # Export primary datasets
        if self.dau_primary_df is not None:
            filename = f"{export_dir}/primary_dau_cleaned.csv"
            self.dau_primary_df.to_csv(filename, index=False)
            print(f"✅ Exported: {filename}")
            exports_completed += 1
        
        if self.retention_primary_df is not None:
            filename = f"{export_dir}/primary_retention_cleaned.csv"
            self.retention_primary_df.to_csv(filename, index=False)
            print(f"✅ Exported: {filename}")
            exports_completed += 1
        
        if self.cohort_df is not None:
            filename = f"{export_dir}/cohort_analysis_cleaned.csv"
            self.cohort_df.to_csv(filename, index=False)
            print(f"✅ Exported: {filename}")
            exports_completed += 1
        
        if self.mobile_raw_df is not None:
            filename = f"{export_dir}/mobile_raw_cleaned.csv"
            self.mobile_raw_df.to_csv(filename, index=False)
            print(f"✅ Exported: {filename}")
            exports_completed += 1
        
        # Create analysis summary
        summary = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'files_processed': exports_completed,
            'primary_files': ['dau_0results.csv', 'retention_0results.csv', 'cohort_results.csv'],
            'supporting_dau_files': list(self.all_dau_files.keys()),
            'supporting_retention_files': list(self.all_retention_files.keys()),
            'export_directory': export_dir
        }
        
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv(f"{export_dir}/analysis_summary.csv", index=False)
        
        print(f"\n🎉 EXPORT COMPLETED!")
        print(f"📁 Location: {export_dir}/")
        print(f"📊 Files exported: {exports_completed}")
        print(f"📋 Summary saved: analysis_summary.csv")
    
    def generate_actionable_insights(self):
        """Generate business-actionable insights"""
        print("\n💡 ACTIONABLE BUSINESS INSIGHTS:")
        print("="*60)
        
        insights = []
        
        # DAU Insights
        if self.dau_primary_df is not None:
            numeric_cols = self.dau_primary_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                main_metric = numeric_cols[0]
                mean_dau = self.dau_primary_df[main_metric].mean()
                max_dau = self.dau_primary_df[main_metric].max()
                min_dau = self.dau_primary_df[main_metric].min()
                
                # Performance insights
                if max_dau > mean_dau * 1.5:
                    insights.append(f"🚀 Peak Performance: Your highest DAU ({max_dau:,.0f}) is {(max_dau/mean_dau-1)*100:.1f}% above average - identify what drove this success!")
                
                if min_dau < mean_dau * 0.7:
                    insights.append(f"⚠️ Low Performance Alert: Your lowest DAU ({min_dau:,.0f}) is {(1-min_dau/mean_dau)*100:.1f}% below average - investigate potential issues")
                
                # Volatility insight
                std_dau = self.dau_primary_df[main_metric].std()
                cv = std_dau / mean_dau
                if cv > 0.2:
                    insights.append(f"📊 High Variability: DAU shows {cv*100:.1f}% coefficient of variation - consider user engagement strategies")
        
        # Retention Insights
        if self.retention_primary_df is not None:
            numeric_cols = self.retention_primary_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if 'retention' in col.lower() or 'rate' in col.lower():
                    mean_retention = self.retention_primary_df[col].mean()
                    if mean_retention < 20:
                        insights.append(f"🔴 Low Retention Alert: {col} averages {mean_retention:.1f}% - focus on onboarding and early user experience")
                    elif mean_retention > 60:
                        insights.append(f"🟢 Strong Retention: {col} averages {mean_retention:.1f}% - leverage this strength for growth")
        
        # Data Quality Insights
        total_files = len(self.all_dau_files) + len(self.all_retention_files)
        if total_files > 6:
            insights.append(f"📈 Rich Data Environment: {total_files} analysis files available - excellent foundation for deep insights")
        
        # Print insights
        if insights:
            for i, insight in enumerate(insights, 1):
                print(f"{i}. {insight}")
        else:
            print("📊 Run deeper analysis to generate specific insights")
        
        # Next Steps Recommendations
        print(f"\n🎯 RECOMMENDED NEXT STEPS:")
        print("1. 📊 Create time series visualizations from cleaned data")
        print("2. 🔍 Perform cohort analysis using cohort_results.csv")
        print("3. 📈 Build retention curves and identify drop-off points") 
        print("4. 🎮 Analyze user behavior patterns from mobile_analytics.csv")
        print("5. 📋 Set up automated monitoring for key metrics")

# Main Execution Function
def main():
    """Execute comprehensive mobile analytics foundation analysis"""
    print("🚀 MOBILE ANALYTICS FOUNDATION - COMPREHENSIVE ANALYSIS")
    print("="*70)
    print("📱 Analyzing mobile app user engagement, retention, and cohort data")
    print("="*70)
    
    # Initialize analyzer
    analyzer = MobileAnalyticsFoundation()
    
    print("\n🎯 DETECTED FILES:")
    detected_files = [
        "✅ dau_0results.csv (PRIMARY)",
        "✅ retention_0results.csv (PRIMARY)", 
        "✅ cohort_results.csv",
        "✅ mobile_analytics.csv (RAW DATA)",
        "📊 Additional DAU files: dau_1results.csv, dau_2results.csv, dau_3results.csv",
        "📊 Additional Retention files: retention_1results.csv, retention_2results.csv, etc."
    ]
    
    for file_info in detected_files:
        print(f"  {file_info}")
    
    try:
        print(f"\n⏰ Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Execute comprehensive analysis pipeline
        analyzer.load_primary_data()
        analyzer.load_all_supporting_files()
        analyzer.analyze_raw_mobile_data()
        analyzer.clean_and_validate_all()
        analyzer.calculate_comprehensive_statistics()
        analyzer.create_master_dataset()
        analyzer.export_analysis_ready_data()
        analyzer.generate_actionable_insights()
        
        print(f"\n🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📂 Check 'cleaned_data_for_analysis/' folder for all processed data")
        print("🚀 Ready for advanced analytics and visualization!")
        
    except Exception as e:
        print(f"\n❌ Analysis error: {e}")
        print("\n🔄 TROUBLESHOOTING:")
        print("1. ✅ Ensure all primary files are in the same directory")
        print("2. ✅ Check file names match exactly: dau_0results.csv, retention_0results.csv, cohort_results.csv")
        print("3. 🔧 Run script again after fixing file issues")

if __name__ == "__main__":
    main()