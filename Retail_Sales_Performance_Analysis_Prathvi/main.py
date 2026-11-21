"""
Retail Sales Performance Analysis
Student: Prathvi Agarwal | Roll No.: 2026B01010436 | Section: CSE 10

A beginner-friendly end-to-end retail data analysis project.
Run from the project folder:
    python main.py

The script creates a synthetic dataset if data/retail_sales.csv is missing,
cleans the data, performs analysis, exports CSV tables, and saves charts.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# All paths are based on this file's location, so the project works from
# VS Code, Command Prompt, or another working directory.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
TABLE_DIR = OUTPUT_DIR / "analysis_tables"
RAW_FILE = DATA_DIR / "retail_sales.csv"
CLEAN_FILE = DATA_DIR / "cleaned_retail_sales.csv"


def create_synthetic_dataset(file_path=RAW_FILE, rows=1200, seed=42):
    """Create realistic sample orders with a few intentional data issues."""
    rng = np.random.default_rng(seed)

    products = {
        "Electronics": {
            "Wireless Mouse": 699, "Keyboard": 1299, "Headphones": 1999,
            "USB-C Hub": 2499, "Power Bank": 1599
        },
        "Clothing": {
            "T-Shirt": 599, "Jeans": 1499, "Hoodie": 1799,
            "Sneakers": 2499, "Jacket": 2999
        },
        "Home & Kitchen": {
            "Water Bottle": 399, "Mixer Grinder": 3299, "Bedsheet": 999,
            "Cookware Set": 2199, "Desk Lamp": 899
        },
        "Books": {
            "Python Basics": 499, "Data Science Guide": 799,
            "Business Strategy": 599, "Fiction Novel": 349,
            "Mathematics Handbook": 449
        }
    }
    cities = ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Lucknow",
              "Ghaziabad", "Jaipur", "Pune", "Chennai", "Kolkata"]
    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
    customers = [f"CUST{n:04d}" for n in range(1, 251)]

    start = pd.Timestamp("2025-01-01")
    end = pd.Timestamp("2025-12-31")
    date_offsets = (end - start).days

    records = []
    for i in range(rows):
        category = rng.choice(list(products.keys()), p=[0.30, 0.28, 0.24, 0.18])
        product = rng.choice(list(products[category].keys()))
        unit_price = products[category][product]
        quantity = int(rng.integers(1, 6))
        # Small realistic price variation, rounded to two decimal places.
        unit_price = round(float(unit_price * rng.uniform(0.94, 1.06)), 2)
        order_date = start + pd.Timedelta(days=int(rng.integers(0, date_offsets + 1)))
        records.append({
            "Order_ID": f"ORD{i+1:05d}",
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Customer_ID": rng.choice(customers),
            "City": rng.choice(cities),
            "Product": product,
            "Category": category,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Revenue": round(quantity * unit_price, 2),
            "Payment_Method": rng.choice(payment_methods, p=[0.38, 0.22, 0.20, 0.12, 0.08])
        })

    df = pd.DataFrame(records)

    # Intentionally add a small number of missing City values for cleaning practice.
    missing_indices = rng.choice(df.index, size=18, replace=False)
    df.loc[missing_indices, "City"] = np.nan

    # Add exact duplicate order rows so duplicate detection can be demonstrated.
    duplicate_rows = df.sample(12, random_state=seed)
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Add a few unusually high-value orders to make outlier analysis meaningful.
    high_indices = rng.choice(df.index[:rows], size=5, replace=False)
    df.loc[high_indices, "Quantity"] = 20
    df.loc[high_indices, "Revenue"] = (
        df.loc[high_indices, "Quantity"] * df.loc[high_indices, "Unit_Price"]
    ).round(2)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Created synthetic dataset: {file_path} ({len(df)} rows)")


def inspect_and_clean_data():
    """Load raw data, inspect quality, remove duplicate orders, and clean City."""
    if not RAW_FILE.exists():
        create_synthetic_dataset()

    df = pd.read_csv(RAW_FILE)
    print("\n--- DATASET INSPECTION ---")
    print("First five rows:\n", df.head())
    print("\nDataset shape:", df.shape)
    print("\nColumn data types:\n", df.dtypes)
    print("\nMissing values by column:\n", df.isna().sum())

    duplicate_count = int(df.duplicated(subset=["Order_ID"]).sum())
    print("\nDuplicate Order_ID count:", duplicate_count)

    # Keep the first copy of each Order_ID.
    df = df.drop_duplicates(subset=["Order_ID"], keep="first").copy()

    # Replace missing or blank City values with a clear category.
    df["City"] = df["City"].fillna("Unknown")
    df["City"] = df["City"].replace(r"^\s*$", "Unknown", regex=True)

    # Convert dates to pandas datetime. Invalid dates become NaT and are removed.
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date", "Quantity", "Unit_Price"])

    # Ensure numeric fields have numeric data types.
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    df = df.dropna(subset=["Quantity", "Unit_Price"])
    df["Quantity"] = df["Quantity"].astype(int)

    # Recalculate Revenue from its components, rather than trusting raw values.
    df["Revenue"] = (df["Quantity"] * df["Unit_Price"]).round(2)

    df.to_csv(CLEAN_FILE, index=False)
    print("\nCleaned dataset saved:", CLEAN_FILE)
    print("Cleaned dataset shape:", df.shape)
    print("Missing values after cleaning:\n", df.isna().sum())
    return df


def save_table(df, filename):
    """Save an analysis table in outputs/analysis_tables."""
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(TABLE_DIR / filename, index=True)
    print("Saved table:", TABLE_DIR / filename)


def create_charts(df, monthly_revenue, category_summary, city_revenue, payment_summary):
    """Create four clear charts and save them as PNG files."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Monthly revenue trend.
    plt.figure(figsize=(10, 5))
    monthly_revenue.plot(kind="line", marker="o")
    plt.title("Monthly Retail Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "monthly_revenue.png", dpi=150)
    plt.close()

    # 2. Revenue by product category.
    plt.figure(figsize=(9, 5))
    category_summary["Revenue"].sort_values(ascending=False).plot(kind="bar")
    plt.title("Revenue by Product Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "category_revenue.png", dpi=150)
    plt.close()

    # 3. Top five cities by revenue.
    plt.figure(figsize=(9, 5))
    city_revenue.head(5).sort_values().plot(kind="barh")
    plt.title("Top 5 Cities by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("City")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_cities.png", dpi=150)
    plt.close()

    # 4. Revenue by payment method.
    plt.figure(figsize=(8, 5))
    payment_summary["Revenue"].sort_values(ascending=False).plot(kind="bar")
    plt.title("Revenue by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Revenue")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "payment_methods.png", dpi=150)
    plt.close()


def perform_analysis(df):
    """Calculate requested KPIs, rankings, summaries, and IQR outliers."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_revenue = float(df["Revenue"].sum())
    total_quantity = int(df["Quantity"].sum())
    order_count = int(df["Order_ID"].nunique())
    average_order_value = total_revenue / order_count if order_count else 0

    # Revenue verification: all row revenues must match Quantity * Unit_Price.
    expected_revenue = (df["Quantity"] * df["Unit_Price"]).round(2)
    revenue_verified = bool(np.allclose(df["Revenue"], expected_revenue))

    top_products = (df.groupby("Product")["Revenue"].sum()
                    .sort_values(ascending=False).head(10).to_frame())
    city_revenue = df.groupby("City")["Revenue"].sum().sort_values(ascending=False)
    monthly_revenue = (df.set_index("Order_Date").resample("M")["Revenue"]
                       .sum())
    monthly_revenue.index = monthly_revenue.index.strftime("%Y-%m")
    best_month = monthly_revenue.idxmax()
    best_month_revenue = float(monthly_revenue.max())

    top_customers = (df.groupby("Customer_ID")["Revenue"].sum()
                     .sort_values(ascending=False).head(10).to_frame())
    payment_summary = df.groupby("Payment_Method").agg(
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Revenue=("Revenue", "sum")
    ).sort_values("Revenue", ascending=False)

    category_summary = df.groupby("Category").agg(
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Average_Order_Revenue=("Revenue", "mean")
    ).sort_values("Revenue", ascending=False)

    # IQR outlier rule: values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR.
    q1 = df["Revenue"].quantile(0.25)
    q3 = df["Revenue"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df["Revenue"] < lower_bound) | (df["Revenue"] > upper_bound)].copy()

    # NumPy descriptive statistics.
    revenue_values = df["Revenue"].to_numpy()
    numpy_stats = pd.DataFrame({
        "Metric": ["Mean Revenue", "Median Revenue", "Standard Deviation Revenue"],
        "Value": [
            float(np.mean(revenue_values)),
            float(np.median(revenue_values)),
            float(np.std(revenue_values, ddof=0))
        ]
    }).set_index("Metric")

    kpis = pd.DataFrame({
        "Metric": ["Total Revenue", "Total Quantity Sold", "Number of Orders",
                   "Average Order Value", "Revenue Calculation Verified"],
        "Value": [total_revenue, total_quantity, order_count,
                  average_order_value, revenue_verified]
    }).set_index("Metric")

    save_table(kpis, "key_metrics.csv")
    save_table(top_products, "top_10_products_by_revenue.csv")
    save_table(city_revenue.to_frame("Revenue"), "city_revenue_ranking.csv")
    save_table(monthly_revenue.to_frame("Revenue"), "monthly_revenue.csv")
    save_table(top_customers, "top_10_customers.csv")
    save_table(payment_summary, "payment_method_summary.csv")
    save_table(category_summary, "category_summary.csv")
    save_table(outliers, "revenue_outliers_iqr.csv")
    save_table(numpy_stats, "numpy_revenue_statistics.csv")

    create_charts(df, monthly_revenue, category_summary, city_revenue, payment_summary)

    # Recommendations are generated from the actual calculated results.
    best_category = category_summary.index[0]
    best_city = city_revenue.index[0]
    best_payment = payment_summary.index[0]
    weakest_payment = payment_summary.index[-1]
    best_product = top_products.index[0]
    recommendations = [
        f"Prioritise inventory planning for {best_category}, the highest-revenue category.",
        f"Review local marketing and stock availability in {best_city}, the top city by revenue.",
        f"Keep the {best_payment} payment experience reliable because it contributes the most revenue.",
        f"Investigate customer experience and checkout friction for {weakest_payment}, the lowest-revenue payment method.",
        f"Use targeted bundles or related-product offers around {best_product}, the top product by revenue."
    ]
    rec_text = "\n".join(f"{i}. {rec}" for i, rec in enumerate(recommendations, 1))
    (OUTPUT_DIR / "business_recommendations.txt").write_text(rec_text, encoding="utf-8")

    summary = {
        "total_revenue": round(total_revenue, 2),
        "total_quantity": total_quantity,
        "order_count": order_count,
        "average_order_value": round(average_order_value, 2),
        "revenue_verified": revenue_verified,
        "best_month": best_month,
        "best_month_revenue": round(best_month_revenue, 2),
        "top_category": best_category,
        "top_city": best_city,
        "top_payment_method": best_payment,
        "outlier_count": int(len(outliers)),
        "numpy_mean_revenue": float(np.mean(revenue_values)),
        "numpy_median_revenue": float(np.median(revenue_values)),
        "numpy_std_revenue": float(np.std(revenue_values, ddof=0)),
        "recommendations": recommendations
    }
    (OUTPUT_DIR / "project_summary.json").write_text(
        json.dumps(summary, indent=4), encoding="utf-8"
    )

    print("\n--- KEY RESULTS ---")
    print(kpis)
    print("\nBest month:", best_month, "| Revenue:", round(best_month_revenue, 2))
    print("\nTop products:\n", top_products)
    print("\nCity ranking:\n", city_revenue)
    print("\nIQR outlier count:", len(outliers))
    print("\nNumPy statistics:\n", numpy_stats)
    print("\nBusiness recommendations:\n", rec_text)
    print("\nAnalysis complete. Check the outputs folder.")


def main():
    """Run the full project workflow."""
    for folder in [DATA_DIR, OUTPUT_DIR, CHART_DIR, TABLE_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
    df = inspect_and_clean_data()
    perform_analysis(df)


if __name__ == "__main__":
    main()
