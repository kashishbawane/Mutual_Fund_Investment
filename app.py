import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Mutual Fund Investment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Mutual Fund Investment Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("dataset.xlsx")  # If Excel
    except:
        df = pd.read_csv("dataset.csv")    # If CSV fallback
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔎 Filters")
funds = st.sidebar.multiselect("Select Fund(s)", df["Fund_Name"].unique(), default=df["Fund_Name"].unique()[:2])
categories = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Fund_Name"].isin(funds)) & (df["Category"].isin(categories))]

# -------------------------------
# QUICK INSIGHTS
# -------------------------------
st.subheader("📌 Quick Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Funds Selected", len(filtered_df["Fund_Name"].unique()))
with col2:
    st.metric("Average NAV", f"{filtered_df['NAV'].mean():.2f}")
with col3:
    st.metric("Max Return (%)", f"{filtered_df['Return'].max():.2f}")

# -------------------------------
# VISUALIZATIONS
# -------------------------------
st.subheader("📈 NAV Trend Over Time")
fig1 = px.line(filtered_df, x="Date", y="NAV", color="Fund_Name", title="NAV Trend")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Category-wise Average Return")
fig2 = px.bar(filtered_df.groupby("Category")["Return"].mean().reset_index(),
              x="Category", y="Return", color="Category", title="Average Return by Category")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🌀 Fund Distribution by Category")
fig3 = px.pie(filtered_df, names="Category", title="Fund Distribution")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_mutual_funds.csv",
    mime="text/csv"
)
