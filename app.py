import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="📊 Mutual Fund Investment Dashboard",
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
        df = pd.read_excel("dataset.xlsx")   # Excel
    except:
        df = pd.read_csv("dataset.csv")      # CSV fallback

    # Clean column names (remove spaces, unify casing)
    df.columns = df.columns.str.strip()

    # Debug → show available columns
    st.write("✅ Available columns in dataset:", list(df.columns))

    # If a Date column exists, convert it
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df.rename(columns={col: "Date"}, inplace=True)
            break

    return df

df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔎 Filters")

fund_col = None
cat_col = None
nav_col = None
ret_col = None

# Try to auto-detect key columns
for col in df.columns:
    if "fund" in col.lower():
        fund_col = col
    if "cat" in col.lower():
        cat_col = col
    if "nav" in col.lower():
        nav_col = col
    if "return" in col.lower():
        ret_col = col

# Show detected mapping
st.sidebar.write("📌 Column mapping detected:")
st.sidebar.write(f"Fund: {fund_col}, Category: {cat_col}, NAV: {nav_col}, Return: {ret_col}, Date: {'Date' if 'Date' in df.columns else '❌'}")

# Filters only if fund/category exist
if fund_col:
    funds = st.sidebar.multiselect("Select Fund(s)", df[fund_col].unique(), default=df[fund_col].unique()[:2])
    df = df[df[fund_col].isin(funds)]

if cat_col:
    categories = st.sidebar.multiselect("Select Category", df[cat_col].unique(), default=df[cat_col].unique())
    df = df[df[cat_col].isin(categories)]

# -------------------------------
# QUICK INSIGHTS
# -------------------------------
st.subheader("📌 Quick Insights")
col1, col2, col3 = st.columns(3)

if fund_col:
    col1.metric("Total Funds", len(df[fund_col].unique()))
if nav_col:
    col2.metric("Average NAV", f"{df[nav_col].mean():.2f}")
if ret_col:
    col3.metric("Max Return (%)", f"{df[ret_col].max():.2f}")

# -------------------------------
# VISUALIZATIONS
# -------------------------------
if "Date" in df.columns and nav_col and fund_col:
    st.subheader("📈 NAV Trend Over Time")
    fig1 = px.line(df, x="Date", y=nav_col, color=fund_col, title="NAV Trend")
    st.plotly_chart(fig1, use_container_width=True)

if cat_col and ret_col:
    st.subheader("📊 Category-wise Average Return")
    fig2 = px.bar(df.groupby(cat_col)[ret_col].mean().reset_index(),
                  x=cat_col, y=ret_col, color=cat_col,
                  title="Average Return by Category")
    st.plotly_chart(fig2, use_container_width=True)

if cat_col:
    st.subheader("🌀 Fund Distribution by Category")
    fig3 = px.pie(df, names=cat_col, title="Fund Distribution")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📄 Filtered Data")
st.dataframe(df)

st.download_button(
    label="📥 Download Filtered Data",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_mutual_funds.csv",
    mime="text/csv"
)
