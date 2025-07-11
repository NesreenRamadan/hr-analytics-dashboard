import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined data
df = pd.read_excel("combined_cleaned_data.xlsx")

# Drop rows with missing gender or reason
df = df.dropna(subset=["Gender", "Reason_of_Leaving"])
# Exclude 'Unknown' gender
df = df[(df["Gender"].notna()) & (df["Gender"] != "Unknown")]
# 👉 Exclude 'Unknown'
df = df[df["Gender"] != "Unknown"]
# Group by Gender and Reason_of_Leaving, count how many left for each
grouped = df.groupby(["Gender", "Reason_of_Leaving"]).size().reset_index(name='Count')

# Pivot for grouped bar chart
pivot_df = grouped.pivot(index="Reason_of_Leaving", columns="Gender", values="Count").fillna(0)

# Sort by total turnout across genders
pivot_df["Total"] = pivot_df.sum(axis=1)
pivot_df = pivot_df.sort_values(by="Total", ascending=False).drop(columns="Total")

# Plot
pivot_df.plot(kind="bar", figsize=(14, 7), colormap="Paired")

plt.title("Top Causes of Turnover by Gender")
plt.xlabel("Reason of Leaving")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y')
plt.legend(title="Gender")
plt.show()
