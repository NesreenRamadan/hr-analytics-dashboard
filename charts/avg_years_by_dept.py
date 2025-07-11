import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined Excel file
df = pd.read_excel('combined_cleaned_data.xlsx')

# Drop rows with missing values in Years or Department
df = df.dropna(subset=['Years', 'Department'])

# 🔧 Clean Department names (correct common typos)
df['Department'] = df['Department'].replace({
    'Administrativ': 'Administrative',  # typo correction (missing 'e')
    'Administative': 'Administrative',  # common variation
    'Adminstrative': 'Administrative',  # common typo
    'Admin': 'Administrative'          # even short forms if needed
})

# Group by Department and calculate average employment duration
avg_years_by_dept = df.groupby('Department')['Years'].mean().sort_values(ascending=False)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_years_by_dept.index, y=avg_years_by_dept.values,
            hue=avg_years_by_dept.index, palette='Blues_d', legend=False)
plt.title('Average Employment Duration by Department', fontsize=16)
plt.xlabel('Department')
plt.ylabel('Average Years of Employment')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
