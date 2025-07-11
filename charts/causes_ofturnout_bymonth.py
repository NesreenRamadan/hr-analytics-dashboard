import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#📌 1. Top Causes of Turnout by Month (Heatmap),
# Group by: Month + Reason_of_Leaving,Count number of employees who left for each cause, per month,
# Create heatmap: X-axis = months, Y-axis = causes, color = number of leave
# Load your combined Excel file
file_path = "combined_cleaned_data.xlsx"
df = pd.read_excel(file_path)

# Convert Exit_Date to datetime
df['Exit_Date'] = pd.to_datetime(df['Exit_Date'], errors='coerce')

# Extract month names
df['Month'] = df['Exit_Date'].dt.month_name()

# Group by Month + Reason of Leaving
grouped = df.groupby(['Age_Group', 'Reason_of_Leaving'], observed=True).size().unstack(fill_value=0)

# Pivot for heatmap format
pivot = grouped.pivot(index='Reason_of_Leaving', columns='Month', values='Count').fillna(0)

# Sort month columns in calendar order
ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
pivot = pivot[ordered_months]

# Create heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5)
plt.title("Top Causes of Turnout by Month")
plt.xlabel("Month")
plt.ylabel("Reason for Leaving")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
