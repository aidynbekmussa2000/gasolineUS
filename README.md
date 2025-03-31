# ⛽ U.S. Gasoline Price Tracker Dashboard

This project is a data analytics dashboard that tracks and visualizes historical gasoline prices across the United States. Using data from the U.S. Energy Information Administration (EIA), it provides interactive insights into regional price trends, monthly averages, and recent changes for decision-makers, small businesses, and everyday drivers.

Built as part of a university data management course, the system demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline and integrates with a PostgreSQL database and interactive Streamlit dashboard for real-time analysis.

---

## 📊 Features

- **Interactive Streamlit Dashboard**: Explore gasoline price trends over time with region filters, date sliders, and aggregation options.
- **Summary Table**: Quickly compare the latest price to the previous month's average with dollar and percentage changes.
- **Data Aggregation**: Toggle between weekly and monthly views.
- **Downloadable Data**: Export filtered data for further use.

---

## 🧠 Project Highlights

- **Business Use Case**: Support for consumers and analysts to understand gasoline pricing trends, regional differences, and market movements.
- **ETL Pipeline**: Automated script pulls weekly gasoline data from the EIA API, processes it using Pandas, and stores it in PostgreSQL.
- **Technologies Used**:
  - `Python` for data extraction and transformation
  - `Streamlit` for dashboard development
  - `PostgreSQL` for persistent storage and queryability
  - `Plotly` for high-quality interactive charts

---

## 🛠️ How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gasoline-price-tracker.git
cd gasoline-price-tracker
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create `.env` or configure your PostgreSQL credentials in the code.

4. Run the Streamlit app:
```bash
streamlit run dashboard.py
```

---

## 🗃️ Data Source
- **U.S. Energy Information Administration (EIA)**
- Public API: https://www.eia.gov/opendata/

---

## 🚀 Future Improvements
- Add price prediction using machine learning
- Enable user-uploaded local gas prices for crowdsourcing
- Advanced analytics tab (e.g., volatility, seasonality)
- Dockerize the entire pipeline for deployment

---

## 📬 Contact
Feel free to reach out via GitHub issues or aidynbekmussa@gmail.com if you have any questions or suggestions!

---

