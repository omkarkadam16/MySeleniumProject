import pandas as pd

# Define data
data = {
    "UID": ["38", "28", "27"],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save as an Excel file
df.to_excel("UID.xlsx", index=False)

print("✅ Excel file 'test_data.xlsx' created successfully!")