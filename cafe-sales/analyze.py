"""
Cafe Sales Analysis
===================
Exploratory data analysis on 90 days of cafe transactions.

Author: Ceren Benzer
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Style configuration
sns.set_style("whitegrid")
plt.rcParams.update({
    "figure.dpi": 100,
    "savefig.dpi": 150,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
})

PALETTE = {
    "primary":   "#2E5266",
    "secondary": "#6E8898",
    "accent":    "#E2C044",
    "highlight": "#D7263D",
    "neutral":   "#9FB1BC",
}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cafe_sales.csv"
IMG_PATH = Path(__file__).resolve().parent.parent / "images"
IMG_PATH.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# 1. LOAD & INSPECT
# ---------------------------------------------------------------------------
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def summarize(df):
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Transactions   : {len(df):,}")
    print(f"Date range     : {df['date'].min().date()}  →  {df['date'].max().date()}")
    print(f"Unique products: {df['product'].nunique()}")
    print(f"Total revenue  : {df['total'].sum():,} TL")
    print(f"Avg. basket    : {df['total'].mean():.2f} TL")
    print(f"Missing values : {df.isna().sum().sum()}")
    print()


# ---------------------------------------------------------------------------
# 2. PRODUCT PERFORMANCE
# ---------------------------------------------------------------------------
def product_performance(df):
    """Revenue and quantity by product."""
    perf = (
        df.groupby("product")
        .agg(revenue=("total", "sum"),
             units_sold=("quantity", "sum"),
             transactions=("transaction_id", "count"))
        .sort_values("revenue", ascending=False)
    )
    perf["revenue_share_%"] = (perf["revenue"] / perf["revenue"].sum() * 100).round(1)
    return perf


def plot_product_performance(perf, save_as="01_product_performance.png"):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Revenue by product
    perf_sorted = perf.sort_values("revenue", ascending=True)
    colors = [PALETTE["highlight"] if i == len(perf_sorted) - 1
              else PALETTE["primary"] for i in range(len(perf_sorted))]
    axes[0].barh(perf_sorted.index, perf_sorted["revenue"], color=colors)
    axes[0].set_title("Revenue by Product (90 days)")
    axes[0].set_xlabel("Revenue (TL)")
    for i, v in enumerate(perf_sorted["revenue"]):
        axes[0].text(v + 2000, i, f"{v:,.0f}", va="center", fontsize=9)

    # Revenue share donut
    top5 = perf.head(5)
    others_revenue = perf["revenue"].iloc[5:].sum()
    labels = list(top5.index) + ["Others"]
    sizes = list(top5["revenue"]) + [others_revenue]
    colors2 = [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"],
               PALETTE["highlight"], PALETTE["neutral"], "#cccccc"]
    axes[1].pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
                colors=colors2, wedgeprops=dict(width=0.4, edgecolor="white"))
    axes[1].set_title("Revenue Share — Top 5 Products")

    plt.tight_layout()
    plt.savefig(IMG_PATH / save_as, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {save_as}")


# ---------------------------------------------------------------------------
# 3. PEAK HOUR ANALYSIS
# ---------------------------------------------------------------------------
def hourly_pattern(df):
    return (
        df.groupby("hour")
        .agg(revenue=("total", "sum"),
             transactions=("transaction_id", "count"))
        .reset_index()
    )


def plot_hourly_pattern(hourly, save_as="02_hourly_pattern.png"):
    fig, ax = plt.subplots(figsize=(12, 5))

    peak_hour = hourly.loc[hourly["revenue"].idxmax(), "hour"]
    colors = [PALETTE["highlight"] if h == peak_hour else PALETTE["primary"]
              for h in hourly["hour"]]

    bars = ax.bar(hourly["hour"], hourly["revenue"], color=colors, edgecolor="white")
    ax.set_title("Hourly Revenue Distribution")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Revenue (TL)")
    ax.set_xticks(hourly["hour"])

    # Annotate peak
    peak_val = hourly["revenue"].max()
    ax.annotate(f"Peak: {peak_hour}:00\n{peak_val:,.0f} TL",
                xy=(peak_hour, peak_val),
                xytext=(peak_hour + 1.5, peak_val * 0.85),
                fontsize=10, fontweight="bold", color=PALETTE["highlight"],
                arrowprops=dict(arrowstyle="->", color=PALETTE["highlight"]))

    plt.tight_layout()
    plt.savefig(IMG_PATH / save_as, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {save_as}")


# ---------------------------------------------------------------------------
# 4. WEEKDAY vs WEEKEND
# ---------------------------------------------------------------------------
def weekday_analysis(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]
    daily = (
        df.groupby("day_of_week")
        .agg(revenue=("total", "sum"),
             transactions=("transaction_id", "count"),
             avg_basket=("total", "mean"))
        .reindex(order)
    )
    return daily


def plot_weekday_analysis(daily, save_as="03_weekday_pattern.png"):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    weekend_mask = daily.index.isin(["Saturday", "Sunday"])
    colors = [PALETTE["highlight"] if w else PALETTE["primary"] for w in weekend_mask]

    axes[0].bar(daily.index, daily["revenue"], color=colors)
    axes[0].set_title("Revenue by Day of Week")
    axes[0].set_ylabel("Revenue (TL)")
    axes[0].tick_params(axis="x", rotation=30)

    axes[1].bar(daily.index, daily["avg_basket"], color=colors)
    axes[1].set_title("Average Basket Size by Day")
    axes[1].set_ylabel("Avg. transaction (TL)")
    axes[1].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.savefig(IMG_PATH / save_as, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {save_as}")


# ---------------------------------------------------------------------------
# 5. HEATMAP: HOUR × DAY
# ---------------------------------------------------------------------------
def plot_heatmap(df, save_as="04_hour_day_heatmap.png"):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]
    pivot = (
        df.pivot_table(index="day_of_week", columns="hour",
                       values="total", aggfunc="sum")
        .reindex(order)
    )

    fig, ax = plt.subplots(figsize=(13, 5))
    sns.heatmap(pivot, cmap="YlOrRd", annot=False, linewidths=0.5,
                cbar_kws={"label": "Revenue (TL)"}, ax=ax)
    ax.set_title("Revenue Heatmap — Hour × Day of Week")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(IMG_PATH / save_as, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {save_as}")


# ---------------------------------------------------------------------------
# 6. PAYMENT METHODS
# ---------------------------------------------------------------------------
def payment_breakdown(df):
    return (
        df.groupby("payment_method")
        .agg(revenue=("total", "sum"),
             transactions=("transaction_id", "count"))
        .sort_values("revenue", ascending=False)
    )


def plot_payment_breakdown(pay, save_as="05_payment_methods.png"):
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = [PALETTE["primary"], PALETTE["accent"], PALETTE["secondary"]]
    ax.pie(pay["revenue"], labels=pay.index, autopct="%1.1f%%",
           colors=colors, startangle=90,
           wedgeprops=dict(width=0.4, edgecolor="white"))
    ax.set_title("Revenue Share by Payment Method")
    plt.tight_layout()
    plt.savefig(IMG_PATH / save_as, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {save_as}")


# ---------------------------------------------------------------------------
# 7. KEY INSIGHTS
# ---------------------------------------------------------------------------
def print_insights(df, perf, hourly, daily, pay):
    print("=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)

    top_product = perf.index[0]
    top_share = perf.iloc[0]["revenue_share_%"]
    print(f"1. TOP PRODUCT: {top_product} accounts for {top_share}% of total revenue.")

    peak_hour = hourly.loc[hourly["revenue"].idxmax(), "hour"]
    print(f"2. PEAK HOUR : {peak_hour}:00 generates the highest revenue.")

    weekend_rev = daily.loc[["Saturday", "Sunday"], "revenue"].mean()
    weekday_rev = daily.loc[["Monday", "Tuesday", "Wednesday",
                             "Thursday", "Friday"], "revenue"].mean()
    uplift = (weekend_rev / weekday_rev - 1) * 100
    print(f"3. WEEKEND   : {uplift:+.1f}% revenue uplift vs. weekdays.")

    card_share = (pay.loc["Card", "revenue"] / pay["revenue"].sum() * 100)
    print(f"4. PAYMENT   : Card payments dominate at {card_share:.1f}% of revenue.")

    morning = df[df["hour"].between(8, 11)]["total"].sum()
    afternoon = df[df["hour"].between(12, 16)]["total"].sum()
    evening = df[df["hour"].between(17, 22)]["total"].sum()
    print(f"5. SHIFTS    : Morning {morning:,} TL | Afternoon {afternoon:,} TL | Evening {evening:,} TL")
    print()
    print("RECOMMENDATIONS")
    print("-" * 60)
    print(f"• Stock more {top_product} during {peak_hour}:00 peak.")
    print(f"• Schedule extra staff on weekends ({uplift:+.0f}% traffic).")
    print(f"• Promote bundles during low-traffic 14:00–16:00 window.")
    print()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    df = load_data()
    summarize(df)

    print("Running analyses & generating charts…\n")

    perf = product_performance(df)
    plot_product_performance(perf)

    hourly = hourly_pattern(df)
    plot_hourly_pattern(hourly)

    daily = weekday_analysis(df)
    plot_weekday_analysis(daily)

    plot_heatmap(df)

    pay = payment_breakdown(df)
    plot_payment_breakdown(pay)

    print()
    print_insights(df, perf, hourly, daily, pay)


if __name__ == "__main__":
    main()
