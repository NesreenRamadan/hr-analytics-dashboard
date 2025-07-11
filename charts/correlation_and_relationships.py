import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the combined data
df = pd.read_excel("combined_cleaned_data.xlsx")


# 🔧 Fix common typos in 'Department'
df['Department'] = df['Department'].replace({
    'Administrativ': 'Administrative'
})

# Remove rows where Gender or Department is 'Unknown'
df = df[(df['Gender'] != 'Unknown') & (df['Department'] != 'Unknown')]

# Drop rows with missing values in numeric fields (Age, Years)
df = df.dropna(subset=['Age', 'Years'])

# Convert categorical fields to category type for consistency
df['Gender'] = df['Gender'].astype('category')
df['Department'] = df['Department'].astype('category')
df['Reason_of_Leaving'] = df['Reason_of_Leaving'].astype('category')

# ---------- PART 1: CORRELATION HEATMAP ----------
# Only select numerical columns for correlation
numerical_cols = ['Age', 'Years']
corr = df[numerical_cols].corr()

# Plot heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Correlation between Numerical Attributes")
plt.tight_layout()
plt.show()


# ---------- PART 2: AVERAGE AGE by REASON ----------
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Reason_of_Leaving', y='Age', ci=None)
plt.xticks(rotation=45, ha='right')
plt.title("Average Age by Reason of Leaving")
plt.ylabel("Average Age")
plt.xlabel("Reason of Leaving")
plt.tight_layout()
plt.show()


# ---------- PART 3: YEARS by GENDER ----------
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x='Gender', y='Years')
plt.title("Distribution of Years of Employment by Gender")
plt.ylabel("Years")
plt.xlabel("Gender")
plt.tight_layout()
plt.show()


# ---------- PART 4: AGE by DEPARTMENT ----------
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Department', y='Age')
plt.xticks(rotation=45)
plt.title("Distribution of Age by Department")
plt.ylabel("Age")
plt.xlabel("Department")
plt.tight_layout()
plt.show()


