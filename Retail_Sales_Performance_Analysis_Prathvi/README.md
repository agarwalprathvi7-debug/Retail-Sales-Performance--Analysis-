# Retail Sales Performance Analysis

**HCL Training College Project**  
**Student:** Prathvi Agarwal  
**Roll No.:** 2026B01010436  
**Section:** CSE 10

## 1. Project overview
This beginner-friendly Python project analyses synthetic retail order data. It demonstrates data loading, inspection, cleaning, revenue calculations, grouping, ranking, descriptive statistics, outlier detection, charts, and business recommendations.

The dataset is synthetic and created for academic practice. It is not actual company/customer data.

## 2. Technologies
- Python
- NumPy
- Pandas
- Matplotlib

## 3. Folder structure
```text
Retail_Sales_Performance_Analysis_Prathvi/
├── data/
│   ├── retail_sales.csv
│   └── cleaned_retail_sales.csv
├── src/
│   └── README.txt
├── SRS/
│   └── Retail_Sales_Performance_Analysis_SRS.docx
├── outputs/
│   ├── analysis_tables/
│   ├── charts/
│   ├── business_recommendations.txt
│   └── project_summary.json
├── main.py
├── requirements.txt
├── README.md
└── GITHUB_UPLOAD_INSTRUCTIONS.md
```

## 4. Setup and run
1. Install Python 3.10 or later.
2. Open this folder in VS Code.
3. Open the terminal in VS Code.
4. Create and activate a virtual environment (recommended):
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `python main.py`

If `data/retail_sales.csv` is missing, the script generates it automatically. Running the script regenerates cleaned data, output tables, recommendations, and charts.

## 5. Dataset fields
- `Order_ID`: unique order identifier
- `Order_Date`: date of order
- `Customer_ID`: synthetic customer identifier
- `City`: customer/order city (some raw values are intentionally missing)
- `Product`: product name
- `Category`: product category
- `Quantity`: units sold
- `Unit_Price`: price per unit
- `Revenue`: order revenue
- `Payment_Method`: payment type

## 6. Analysis performed
- Inspects rows, columns, data types, missing values, and duplicate order IDs.
- Removes duplicate orders using `Order_ID`.
- Replaces missing City values with `Unknown`.
- Converts Order_Date to datetime.
- Recalculates and verifies Revenue as Quantity × Unit_Price.
- Calculates total revenue, total quantity, number of orders, and average order value.
- Finds top 10 products, top 10 customers, and city revenue ranking.
- Calculates monthly revenue and the best month.
- Compares payment methods and summarises product categories with `groupby`.
- Detects revenue outliers using the 1.5 × IQR rule.
- Calculates mean, median, and population standard deviation using NumPy.
- Saves four charts and data tables.

## 7. Important outputs
- `data/cleaned_retail_sales.csv`
- `outputs/analysis_tables/` (all analysis CSVs)
- `outputs/charts/` (four PNG charts)
- `outputs/business_recommendations.txt`
- `outputs/project_summary.json`

## 8. Notes
The generated dataset contains deliberate missing City values and duplicate orders so that cleaning steps can be demonstrated. Outliers are flagged for review, not automatically deleted. The IQR method identifies statistical extremes; it does not prove that a transaction is incorrect.
