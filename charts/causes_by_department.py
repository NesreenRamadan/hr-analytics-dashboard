import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Load the combined cleaned dataset ===
df = pd.read_excel("combined_cleaned_data.xlsx")

# === Drop rows with missing department or reason ===
df = df.dropna(subset=["Department", "Reason_of_Leaving"])

# === Group by Department and Reason of Leaving ===
grouped = df.groupby(["Department", "Reason_of_Leaving"]).size().unstack(fill_value=0)

# === Plot as heatmap ===
plt.figure(figsize=(14, 8))
sns.heatmap(grouped, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5)

plt.title("Top Causes of Turnout by Department")
plt.xlabel("Reason of Leaving")
plt.ylabel("Department")
plt.tight_layout()
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()
