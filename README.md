# gasolineUS

# ⛽ U.S. Gasoline Price Tracker Dashboard

## 📄 Project Overview
This project presents a fully functional data analytics dashboard that visualizes historical gasoline price trends across U.S. regions from 2003 to 2025. It is designed as a term project for a Managing Data course, focused on engineering a Big Data pipeline using real-world energy data.

---

## 📊 Objective
The goal is to create an ETL (Extract, Transform, Load) pipeline and analytical dashboard that allows users (drivers, small business owners, policymakers) to:
- Compare weekly gasoline prices by region
- Identify pricing trends over time
- View changes in price vs monthly averages

---

## 📐 Data Source
**U.S. Energy Information Administration (EIA) API**
- Dataset: Weekly Retail Gasoline Prices
- Regions: All 50 states, major metro areas, and PADD zones
- Frequency: Weekly

---

## 🤹 Use Case
A public-facing gasoline price dashboard that helps:
- Drivers plan fuel expenses by location
- Small businesses optimize delivery costs
- Journalists and researchers monitor fuel inflation

---

## 🛠️ Technologies Used
| Layer | Tools |
|-------|-------|
| **ETL** | Python (requests, pandas) |
| **Storage** | PostgreSQL |
| **Analytics** | Plotly, Streamlit |
| **Dashboard** | Streamlit Web App |

---

## 🏛️ Features
- **Interactive time-series plots** for all U.S. regions
- **Dynamic filters** by region and date range
- **Weekly/monthly aggregation** toggle
- **Summary metrics** table with:
  - Latest price
  - Previous month average
  - $ and % change with emojis
- **Data download** button (CSV)





