# Test script to verify environment setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta

print("✅ All packages imported successfully!")
print(f"✅ Pandas version: {pd.__version__}")
print(f"✅ NumPy version: {np.__version__}")

# Test basic functionality
df = pd.DataFrame({
    'date': pd.date_range('2023-07-01', periods=10),
    'users': np.random.randint(7000, 8000, 10)
})

print("✅ Test DataFrame created:")
print(df.head())
print("\n🎉 Environment setup complete!")