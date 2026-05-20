[README.md](https://github.com/user-attachments/files/28069148/README.md)
# ☕ Cafe Sales Analysis

> Exploratory data analysis on 90 days of cafe transactions to surface revenue drivers, peak hours, and operational opportunities.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8-11557C)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4C72B0)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

This project analyzes **7,392 transactions** across **90 days** (Jan – Mar 2024) from a small cafe to answer three questions a real owner would care about:

1. **Which products generate the most revenue?**
2. **When does the cafe earn the most — and least?**
3. **What operational changes would lift revenue?**

The analysis covers product performance, hourly and weekly patterns, payment methods, and translates findings into concrete recommendations.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Core language |
| **Pandas** | Data manipulation & aggregation |
| **NumPy** | Numerical operations |
| **Matplotlib** | Static visualizations |
| **Seaborn** | Statistical charts (heatmap) |
| **Jupyter Notebook** | Interactive analysis & reporting |

---

## 📂 Project Structure

```
cafe-sales-analysis/
├── data/
│   └── cafe_sales.csv          # Transaction dataset (7,392 rows)
├── src/
│   ├── generate_data.py        # Synthetic data generator (reproducible)
│   └── analyze.py              # Full analysis pipeline
├── notebooks/
│   └── cafe_sales_analysis.ipynb  # Interactive walkthrough
├── images/                     # Exported charts
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
# Clone and enter the project
git clone https://github.com/<your-username>/cafe-sales-analysis.git
cd cafe-sales-analysis

# Install dependencies
pip install -r requirements.txt

# (Optional) Regenerate the dataset
python src/generate_data.py

# Run the full analysis
python src/analyze.py

# Or explore interactively
jupyter notebook notebooks/cafe_sales_analysis.ipynb
```

---

## 📊 Key Findings

### 1. Top Products by Revenue
**Sandwich** leads with **15%** of total revenue, followed by **Cheesecake (14.3%)**. Food items dominate over beverages despite lower transaction count — a classic volume-vs-value insight.

![Product Performance](images/01_product_performance.png)

### 2. Bimodal Daily Pattern
Revenue has two clear peaks: a morning coffee rush around **9:00** and a stronger evening peak at **19:00**. The **14:00 – 16:00** window is the slowest period every day.

![Hourly Pattern](images/02_hourly_pattern.png)

### 3. Weekends Generate +37% Revenue
Saturday and Sunday outperform weekdays by **~37%** in revenue. Interestingly, the average basket size is nearly identical — the uplift comes from **traffic volume**, not bigger orders.

![Weekday Pattern](images/03_weekday_pattern.png)

### 4. Hottest Cells: Sunday Evening
The Hour × Day heatmap shows Sunday 19:00 – 20:00 and Saturday 9:00 – 10:00 are the highest-priority shifts for full staffing.

![Heatmap](images/04_hour_day_heatmap.png)

### 5. Card Dominates Payments
Card payments account for **63%** of revenue; cash is still meaningful at **25%**; mobile is growing at **12%**.

![Payment Methods](images/05_payment_methods.png)

---

## 💡 Recommendations

| Recommendation | Rationale |
|---|---|
| Increase stock of high-margin food items (Sandwich, Cheesecake) during the 18:00 – 20:00 shift | Evening peak coincides with food-heavy orders |
| Add one extra staff member to weekend morning and evening shifts | +37% weekend traffic but same basket size → bottleneck is throughput |
| Launch a 14:00 – 16:00 happy-hour bundle (tea + dessert) | Smooth out the consistently slow afternoon window |
| Keep card + mobile payment infrastructure prioritized | Together they handle 75% of revenue |

---

## 🔍 Analysis Methodology

1. **Data Quality:** Checked for missing values, duplicates, and type consistency.
2. **Aggregations:** Used `groupby()` and `pivot_table()` to slice revenue across products, hours, and days.
3. **Visual Design:** Used a consistent color palette to highlight insights (red = focal point, blue = baseline).
4. **Interpretation:** Every chart is paired with a written finding — visuals support claims, they don't replace them.

---

## 📈 What I Learned

- Choosing the right aggregation level changes the story (e.g. revenue vs unit count gives different top-sellers).
- Heatmaps are powerful for two-dimensional pattern discovery — far better than two separate bar charts.
- Comparing weekend vs weekday with both revenue *and* basket size reveals whether growth comes from traffic or ticket size.
- A clean README and reproducible pipeline are as valuable as the analysis itself.

---

## 📝 License

MIT — free to use, learn from, and adapt.

---

## 👋 Contact

**Ceren Benzer**
📍 Istanbul, Türkiye
💼 [LinkedIn](https://linkedin.com/in/cerenbenzer)
📧 cerenbenzer2004@gmail.com

*Open to data analyst / data science internship opportunities — Summer 2026.*
