import pandas as pd

# Load the Parquet file into a pandas DataFrame
df = pd.read_parquet("isoloops_cleaned.parquet")

# Check the first few rows
print(df.head())  # Shows the first 5 rows by default
print(df.info())  # Shows column names, data types, and number of non-null entries