import streamlit as st
import pandas as pd
import os
import plotly.express as px
import calendar
import streamlit as st
import numpy as np
import joblib
# Set page config
st.set_page_config(layout="wide")
st.title("📊Behind the Exit: Exploring Why Employees Leave")
st.markdown("Prepared by Nesreen & Nour | Supervisor: Dr. Hussein Hazimeh")

# Load Excel Data
@st.cache_data
def load_data():
    return pd.read_excel("combined_cleaned_data.xlsx")

df = load_data()
# Fix inconsistent department names
df["Department"] = df["Department"].replace({
    "Administrativ": "Administrative",
    "admin": "Administrative",
    "Admin/General": "Administrative",
    # Add more mappings if needed
})
# Normalize column names
df.rename(columns=lambda x: x.strip().lower(), inplace=True)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")


df.rename(columns={
    'Reason_of_Leaving': 'turnover_reason',
    'Month': 'month_name',
    'Department': 'department',
    'Gender': 'gender',
    'Age': 'age',
    'Years': 'years'
}, inplace=True)

# Remove unknown genders if present
df = df[df['gender'].str.lower() != 'unknown']
# Normalize column name
df.rename(columns={'reason_of_leaving': 'turnover_reason'}, inplace=True)

# Convert numeric month to month name (create a new column)
df['month_name'] = df['month'].apply(
    lambda x: calendar.month_name[int(x)] if pd.notnull(x) and str(x).isdigit() and 1 <= int(x) <= 12 else None
)
# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to section:", [
    "Overview",
    "Correlation Analysis",
    "Employment Duration",
    "Turnover by Reason",
    "Age & Department Insights",
    #"Classification Model",
    "Download Data",
])

# Sidebar Filters
st.sidebar.markdown("### Filters")
selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(df['gender'].dropna().unique().tolist()), key="gender_filter")
selected_dept = st.sidebar.selectbox("Select Department", ["All"] + sorted(df['department'].dropna().unique().tolist()), key="dept_filter")

if selected_gender != "All":
    df = df[df["gender"] == selected_gender]
if selected_dept != "All":
    df = df[df["department"] == selected_dept]

chart_path = "charts"

# OVERVIEW
if section == "Overview":
    st.markdown("<h1 style='font-size: 30px; color: white;'>📊 HR Analytics Dashboard – Overview</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🎯 **Project Objectives**")
    st.markdown("""
    This interactive dashboard provides data-driven insights into employee resignation patterns, helping HR professionals make informed decisions.
    """)

    st.markdown("#### 🧭 Key Goals:")
    st.markdown("""
    - 📌 **Identify departments** with the highest turnover rates  
    - 👥 **Analyze resignation causes** based on gender, age, and seasonality  
    - 📈 **Explore employment duration** trends across roles and departments  
    - 💡 **Support proactive HR policies** for retention and workforce planning
    """)

    st.markdown("#### 🔍 Why it matters:")
    st.info("Understanding why employees leave empowers HR teams to improve satisfaction, reduce costs, and retain top talent.")

    st.markdown("---")


# CORRELATION
# 📊 Correlation Analysis Section
elif section == "Correlation Analysis":
    st.markdown("<h1 style='font-size: 30px; color: white;'>📊  Correlation between Age and Years of Experience</h1>", unsafe_allow_html=True)
    #st.markdown("## 📊 Correlation between Age and Years of Experience")
    
    if 'age' in df.columns and 'years' in df.columns:
        corr_df = df[['age', 'years']].corr()

        fig = px.imshow(
            corr_df,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title="Correlation between Numerical Attributes",
            labels=dict(x="Attributes", y="Attributes", color="Correlation"),
            width=600,
            height=500
        )
        st.plotly_chart(fig, use_container_width=False)

        st.markdown("""
        🔍 **Insight:** There's usually a positive correlation between age and years of work.

        ✅ Conclusion:
There is a strong positive correlation (0.76) between employee age and years of work. 
This indicates that, as expected, older employees tend to have spent more years at the organization.
 This relationship can help in workforce planning and identifying long-serving employees nearing retirement or requiring retention efforts.
        """)

    else:
        st.warning("⚠️ Could not find 'Age' and 'Years' columns to generate correlation heatmap.")



# EMPLOYMENT DURATION
# Fix inconsistent department names
elif section == "Employment Duration":
    st.subheader("📈 Average Employment Duration by Department")
    st.markdown("This chart compares how long employees stay in each department, on average.")

    # --- Filters ---
    gender_filter = st.selectbox("Select gender", ["All"] + sorted(df["gender"].dropna().unique().tolist()))
    year_filter = st.selectbox("Select Year", ["All"] + sorted(df["source_year"].dropna().unique().tolist()))

    # --- Apply Filters ---
    filtered_df = df.copy()
    if gender_filter != "All":
        filtered_df = filtered_df[filtered_df["gender"] == gender_filter]
    if year_filter != "All":
        filtered_df = filtered_df[filtered_df["source_year"] == year_filter]

    # --- Calculate average years of work by department ---
    avg_years_by_dept = (
        filtered_df.groupby("department")["years"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    # --- Plotly chart ---
    fig = px.bar(
        avg_years_by_dept,
        x="department",
        y="years",
        color="years",
        title="Average Employment Duration by Department",
        labels={"years": "Average Years of Employment"},
        color_continuous_scale="Blues",
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)
    # --- Insights ---
    st.markdown("""
    🔍 **Insight:** Admin/General show longest stays; Quality/Safety face high turnover.

    ✅ Conclusion:Employees in the Administrative and General departments tend to have the longest average employment duration, exceeding 6.5 years. 
    In contrast, Quality and Safety has the shortest average, with just over 3 years, indicating a potential issue with retention or role structure in that department.
    These insights can guide targeted retention strategies and workforce planning.
    """)

    #st.markdown("## 📊 Distribution of Years of Work by Gender")
    st.markdown("<h1 style='font-size: 30px; color: white;'>📊 Distribution of Years of Work by Gender</h1>", unsafe_allow_html=True)

    if 'gender' in df.columns and 'years' in df.columns and not df.empty:
        # Remove unknown genders
        filtered_df = df[df['gender'].str.lower() != 'unknown']

        fig = px.histogram(
            filtered_df,
            x="years",
            color="gender",
            marginal="box",  # Optional: adds a box plot above the histogram
            barmode="overlay",
            title="Distribution of Years of Work by Gender",
            nbins=30
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        🔍 **Insight:** Different genders may show different distributions in experience levels.
        
        ✅ Conclusion: Both female and male employees share a similar employment duration distribution, with a median around 4–5 years.
         The range and spread of values, including outliers, are also comparable, suggesting gender does not significantly influence how long employees stay at the organization. 
         This balance indicates fair retention across genders.
        """)
    else:
        st.warning("⚠️ Chart cannot be displayed. Required columns not found or filtered DataFrame is empty.")

elif section == "Turnover by Reason":
    st.subheader("📊 Top Causes of Turnover Analysis")
    st.markdown("Explore why employees are leaving based on **month**, **gender**, **age group**, and **department**.")

    # Age Group bins
    bins = [0, 24, 34, 44, 54, 64, 150]
    labels = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
    
    # --- Chart 1: By Month ---
    st.markdown("### 📅 Turnover Reasons by Month")

    if 'turnover_reason' in df.columns and 'month_name' in df.columns:
        month_reason = df.groupby(["month_name", "turnover_reason"]).size().unstack().fillna(0)
        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        month_reason = month_reason.loc[[month for month in month_order if month in month_reason.index]]

        month_reason = month_reason.loc[month_reason.index.intersection(month_order)]
        fig_month = px.imshow(
            month_reason.T,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            labels=dict(x="Month", y="Reason of Leaving", color="Count"),
            title="Top Causes of Turnover by Month"
        )
        st.plotly_chart(fig_month, use_container_width=True)
        st.markdown("""
        ✅ Conclusion:
This heatmap reveals seasonal patterns in employee resignation behavior.
June and November experience spikes in resignations, often due to personal/social motives and better job offers.
HR departments can:
Prepare retention strategies before these peak months.
Schedule job postings and succession planning accordingly.
Investigate deeper causes during high-turnover seasons for policy updates.""")
    else:
        st.warning("⚠️ Missing columns: 'month_name' or 'turnover_reason'.")

    # --- Chart 2: By Gender ---
    st.markdown("### 👥 Turnover Reasons by Gender")
    if 'turnover_reason' in df.columns and 'gender' in df.columns:
        gender_reason = df.groupby(["turnover_reason", "gender"]).size().reset_index(name="count")
        fig_gender = px.bar(
            gender_reason,
            x="turnover_reason",
            y="count",
            color="gender",
            barmode="group",
            title="Top Causes of Turnover by Gender",
            labels={"turnover_reason": "Reason for Leaving", "count": "Number of Employees"},
        )
        fig_gender.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown("""
        ✅ Conclusion:
This chart highlights that turnover motivations vary significantly by gender:
Female turnover is largely socially or personally driven.
Male turnover is career-driven, indicating a higher sensitivity to job offers or promotions.
📌 Recommendation: HR should tailor retention strategies based on gender:
For female employees, consider flexible policies, wellness programs, and work-life balance.
For male employees, focus on growth paths, salary reviews, and job enrichment.""")

    else:
        st.warning("⚠️ Missing columns: 'turnover_reason' or 'gender'.")
    # --- Chart 3: By Age Group ---
    st.markdown("### 👶👵 Turnover Reasons by Age Group")
    if 'turnover_reason' in df.columns and 'age_group' in df.columns:
        age_reason = df.groupby(["age_group", "turnover_reason"]).size().unstack().fillna(0)
        fig_age = px.imshow(
            age_reason,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            labels=dict(x="Reason for Leaving", y="Age Group", color="Count"),
            title="Top Causes of Turnover by Age Group"
        )
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("""✅ Conclusion:
               Turnover is heavily concentrated among younger employees, especially those under 35, due to social needs and career advancement.
                Retention efforts should focus on the 25–34 age group, offering:
               Career development paths
             Social belonging initiatives
              Work-life flexibility
O             older employees are more stable, indicating long-term loyalty, possibly due to nearing retirement or job security needs.""")

    else:
        st.warning("⚠️ Missing columns: 'turnover_reason' or 'age_group'.")
        
        
    # --- Chart 4: By Department ---
    st.markdown("### 🏢 Turnover Reasons by Department")
    if 'turnover_reason' in df.columns and 'department' in df.columns:
        dept_reason = df.groupby(["department", "turnover_reason"]).size().unstack().fillna(0)
        fig_dept = px.imshow(
            dept_reason,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="PuBu",
            labels=dict(x="Reason for Leaving", y="Department", color="Count"),
            title="Top Causes of Turnover by Department"
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown("""✅ Conclusion:
    
Nursing staff turnover is a critical issue, likely due to emotional exhaustion, job stress, or better external offers. 
It requires immediate retention strategies:
Improved working conditions
Wellness and social support programs
Clear career growth paths
Other departments show standard attrition due to personal and professional motivations.
HR should prioritize Nursing, followed by Allied Medical and General, when designing targeted employee engagement or retention plans.
📌 Recommendation: Conduct internal surveys in the Nursing unit to understand burnout and relocation factors, then act on improving satisfaction and retention.""")

    else:
        st.warning("⚠️ Missing columns: 'turnover_reason' or 'department'.")
        
elif section == "Age & Department Insights":
    st.markdown("## 📈 Age & Department Insights")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    #st.subheader("🎯 Age Distribution & Leaving Reasons Analysis")

    # -------------------------
    # 1. Interactive Boxplot: Age by Department
    # -------------------------
    #st.markdown("### 📦 Distribution of Age by Department")
    st.markdown("<h1 style='font-size: 30px; color: white;'>🎯 Age Distribution & Leaving Reasons Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 30px; color: white;'>Distribution of Age by Department</h1>", unsafe_allow_html=True)
    fig_age_dept = px.box(
        df,
        x="department",
        y="age",
        points="outliers",
        color="department",
        title="Distribution of Age by Department",
        labels={"age": "Employee Age", "department": "Department"},
    )
    fig_age_dept.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig_age_dept, use_container_width=True)
    st.markdown("""✅ Conclusion:
   
Nursing and Allied Medical teams are relatively younger, which aligns with the higher turnover we saw earlier (younger employees tend to explore more job opportunities).
Older age in HR and Engineering/IT suggests greater job stability, likely tied to experience and career development.
Retention programs in Nursing/Medical should consider mentorship, career path clarity, and early engagement strategies for younger employees.
📌 Recommendation: Tailor retention strategies by department age profiles — offer growth and stability to young teams, and recognition and flexibility to older ones.""")
    
    # -------------------------
    # 2. Interactive Bar Chart: Average Age by Reason for Leaving
    # -------------------------
    st.markdown("### 📊 Average Age by Reason for Leaving")

    if "turnover_reason" in df.columns:
        avg_age_by_reason = df.groupby("turnover_reason")["age"].mean().reset_index()
        avg_age_by_reason = avg_age_by_reason.sort_values("age", ascending=False)

        fig_avg_age_reason = px.bar(
            avg_age_by_reason,
            x="turnover_reason",
            y="age",
            title="Average Age by Reason for Leaving",
            labels={"age": "Average Age", "turnover_reason": "Reason"},
            color="age",
        )
        fig_avg_age_reason.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_avg_age_reason, use_container_width=True)
        st.markdown("""✅ Conclusion:
    
Younger employees leave for education, stress, or relocation, while older employees leave due to transfers or strategic reasons.
Targeted action plans:
Offer flexible study leave for <25 age group.
Investigate internal transfer policies — ensure smooth transitions and team restructuring.
Improve workplace conditions (hours, conflict resolution) to retain younger staff.""")

    else:
        st.warning("🚨 Column 'turnover_reason' not found in the dataset.")
        

elif section == "Download Data":
    st.subheader("📁 Download Cleaned HR Data")
    st.markdown("Click below to download the fully cleaned and merged HR dataset used in this dashboard.")
    st.download_button(
        label="Download Excel File",
        data=open("combined_cleaned_data.xlsx", "rb"),
        file_name="combined_cleaned_data.xlsx"
                )
