import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Gasoline Price Dashboard", layout="wide")

@st.cache_data

def load_data():
    df = pd.read_csv("/Users/aidynbekmussa/Desktop/Managing_Data/final_project/gasoline_prices.csv")
    df["period"] = pd.to_datetime(df["period"])
    return df

df = load_data()

st.title("⛽ U.S. Gasoline Price Trends (2003–2025)")
st.markdown("Compare weekly gasoline prices across U.S. regions using EIA data.")

# Sidebar filters
regions = sorted(df["region"].unique())
selected_regions = st.multiselect("Select regions:", regions, default=["U.S.", "California", "Texas"])

min_date = df["period"].min().date()
max_date = df["period"].max().date()
date_range = st.slider("Select date range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))

aggregation = st.selectbox("Time Aggregation", ["Weekly", "Monthly Average", "4-Week Rolling Average"])

# Filter data
filtered = df[
    (df["region"].isin(selected_regions)) &
    (df["period"].dt.date.between(date_range[0], date_range[1]))
]

# Apply aggregation
if aggregation == "Monthly Average":
    filtered = filtered.copy()
    filtered["month"] = filtered["period"].dt.to_period("M").dt.to_timestamp()
    filtered = filtered.groupby(["month", "region"], as_index=False)["value"].mean()
    filtered.rename(columns={"month": "period"}, inplace=True)
elif aggregation == "4-Week Rolling Average":
    filtered = filtered.sort_values("period")
    filtered = filtered.groupby("region")["value"].rolling(window=4, min_periods=1).mean().reset_index()
    filtered = filtered.rename(columns={"level_1": "index"}).merge(df.reset_index(), left_on="index", right_on="index")
    filtered = filtered[["period", "region", "value"]]

# Plot
fig = px.line(
    filtered,
    x="period",
    y="value",
    color="region",
    title="Weekly Gasoline Prices by Region",
    labels={"value": "USD per Gallon", "period": "Date", "region": "Region"},
    template="plotly_white"
)
fig.update_layout(hovermode="x unified", height=600)

st.plotly_chart(fig, use_container_width=True)

# Summary table: Latest price vs monthly average
latest_period = df["period"].max()
last_month = latest_period - pd.DateOffset(days=30)

summary_rows = []
for region in selected_regions:
    region_df = df[df["region"] == region].copy()
    latest_price = region_df[region_df["period"] == latest_period]["value"].mean()
    last_month_avg = region_df[(region_df["period"] >= last_month) & (region_df["period"] < latest_period)]["value"].mean()
    delta = latest_price - last_month_avg
    pct_change = (delta / last_month_avg) * 100 if last_month_avg else None
    summary_rows.append({
        "region": region,
        "Latest Price": round(latest_price, 3),
        "Last Month Avg": round(last_month_avg, 3),
        "Change ($)": round(delta, 3),
        "Change (%)": round(pct_change, 2) if pct_change is not None else None
    })

summary_df = pd.DataFrame(summary_rows)
st.markdown("### 📋 Summary Table: Latest vs Monthly Average")
st.dataframe(summary_df, use_container_width=True)

# Download button
csv = filtered.to_csv(index=False)
st.download_button("📥 Download filtered data", csv, "filtered_gasoline_prices.csv", "text/csv")
