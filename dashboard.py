import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="⛽ Gasoline Price Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("/Users/aidynbekmussa/Desktop/Managing_Data/final_project/gasoline_prices.csv")
    df["period"] = pd.to_datetime(df["period"])
    return df

df = load_data()

# Region emojis
region_emojis = {
    "California": "🌴 California",
    "Texas": "🤠 Texas",
    "New York": "🗽 New York",
    "Florida": "🌞 Florida",
    "Washington": "🌲 Washington",
    "Massachusetts": "🎓 Massachusetts",
    "Colorado": "🏔️ Colorado",
    "Ohio": "🏙️ Ohio",
    "U.S.": "🇺🇸 U.S.",
    "Chicago": "🌃 Chicago",
    "Denver": "🏞️ Denver",
    "Houston": "🚀 Houston",
    "Boston, MA": "🏫 Boston",
    "Seattle, WA": "☕ Seattle",
    "Miami, FL": "🌴 Miami",
    "San Francisco": "🌉 San Francisco",
    "New York City": "🗽 NYC",
}

# State codes for the choropleth map
state_codes = {
    "California": "CA",
    "Texas": "TX",
    "New York": "NY",
    "Florida": "FL",
    "Washington": "WA",
    "Massachusetts": "MA",
    "Colorado": "CO",
    "Ohio": "OH",
    "Illinois": "IL",
    "Minnesota": "MN",
    "Nevada": "NV",
    "Georgia": "GA",
    "Oregon": "OR",
    "Arizona": "AZ",
}

# --- UI Header ---
st.title("⛽ U.S. Gasoline Price Trends (1993–2025)")
st.markdown("Compare weekly gasoline prices across U.S. regions using EIA data.")

# --- Filters ---
regions = sorted(df["region"].unique())
display_regions = [region_emojis.get(r, r) for r in regions]
region_map = {region_emojis.get(r, r): r for r in regions}

selected_display = st.multiselect("🗺️ Select regions:", display_regions, default=["🇺🇸 U.S.", "🌴 California", "🤠 Texas"])
selected_regions = [region_map[r] for r in selected_display]

min_date = df["period"].min().date()
max_date = df["period"].max().date()

col1, col2 = st.columns([1, 1])
with col1:
    date_range = st.slider("🗓️ Select date range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))
with col2:
    granularity = st.radio("🧪 Time Aggregation", ["Weekly", "Monthly Avg", "4-Week Rolling Avg"], horizontal=False)

# --- Filter data ---
df_filtered = df[
    (df["region"].isin(selected_regions)) &
    (df["period"].dt.date.between(date_range[0], date_range[1]))
].copy()

# --- Apply aggregation ---
if granularity == "Monthly Avg":
    df_filtered["month"] = df_filtered["period"].dt.to_period("M").dt.to_timestamp()
    df_filtered = df_filtered.groupby(["month", "region"])["value"].mean().reset_index()
    df_filtered.rename(columns={"month": "period"}, inplace=True)
elif granularity == "4-Week Rolling Avg":
    df_filtered = df_filtered.sort_values(["region", "period"])
    df_filtered["value"] = df_filtered.groupby("region")["value"].transform(lambda x: x.rolling(4, min_periods=1).mean())

# --- Line chart ---
log_scale = st.checkbox("Use Log Scale")
fig = px.line(
    df_filtered,
    x="period",
    y="value",
    color="region",
    title="Gasoline Prices Over Time",
    labels={"value": "USD per Gallon", "period": "Date", "region": "Region"},
    template="plotly_white",
    log_y=log_scale
)
fig.update_layout(hovermode="x unified", height=600)
st.plotly_chart(fig, use_container_width=True)

# --- Summary Table ---
latest_date = df["period"].max()
cutoff_date = latest_date - pd.Timedelta(days=30)

summary = []
for region in selected_regions:
    region_df = df[df["region"] == region].copy()
    latest_price = region_df[region_df["period"] == latest_date]["value"].mean()
    last_month_avg = region_df[(region_df["period"] >= cutoff_date) & (region_df["period"] < latest_date)]["value"].mean()
    change = latest_price - last_month_avg
    pct = (change / last_month_avg) * 100 if last_month_avg else 0
    emoji_name = region_emojis.get(region, region)
    arrow = "📉" if change < 0 else "📈"
    summary.append([emoji_name, f"${latest_price:.3f}", f"${last_month_avg:.3f}", f"{arrow} {change:+.3f}", f"{pct:+.2f}%"])

summary_df = pd.DataFrame(summary, columns=["Region", "Latest Price", "Last Month Avg", "Change ($)", "Change (%)"])
st.markdown("### 📋 Summary Table: Latest vs Monthly Average")
st.markdown("*(Scroll right on mobile →)*")
st.dataframe(summary_df, use_container_width=True)

# --- CSV Download ---
csv = df_filtered.to_csv(index=False)
st.download_button("📥 Download filtered data", csv, "filtered_gasoline_prices.csv", "text/csv")

# --- Choropleth map — show all available states
st.markdown("### 🗺️ Latest Prices by State")

map_df = df[df["period"] == latest_date].copy()
map_df = map_df[map_df["region"].isin(state_codes.keys())].copy()
map_df["state_code"] = map_df["region"].map(state_codes)

if not map_df.empty:
    fig_map = px.choropleth(
        map_df,
        locations="state_code",
        locationmode="USA-states",
        color="value",
        hover_name="region",
        scope="usa",
        color_continuous_scale="Reds",
        labels={"value": "USD per Gallon"},
        title="Latest Gasoline Prices by State"
    )
    fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("No data available for mapped states on the latest date.")