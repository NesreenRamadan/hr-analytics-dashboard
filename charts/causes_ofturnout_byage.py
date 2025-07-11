import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your combined Excel file
df = pd.read_excel("combined_cleaned_data.xlsx")

# Drop rows with missing Age or Reason_of_Leaving
df = df.dropna(subset=["Age", "Reason_of_Leaving"])

# Categorize Age into groups
bins = [0, 25, 35, 45, 55, 65, 100]
labels = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# Group by Age_Group and Reason_of_Leaving
grouped = df.groupby(['Age_Group', 'Reason_of_Leaving']).size().unstack(fill_value=0)

# Plot heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(grouped, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Top Causes of Turnout by Age Group")
plt.ylabel("Age Group")
plt.xlabel("Reason for Leaving")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
