"""
Customer Churn & Retention Analytics
Author: Monu Salonia
Tools: Python (Pandas, NumPy)
"""

import numpy as np
import pandas as pd


def generate_churn_dataset(n_customers: int = 7000) -> pd.DataFrame:
    """Generates realistic customer account and churn data."""
    np.random.seed(42)

    customer_ids = [f"CUST-{i:05d}" for i in range(1, n_customers + 1)]
    tenure_months = np.random.randint(1, 72, size=n_customers)
    contract_types = np.random.choice(
        ["Month-to-month", "One year", "Two year"],
        size=n_customers,
        p=[0.55, 0.25, 0.20],
    )
    internet_service = np.random.choice(
        ["DSL", "Fiber optic", "No"], size=n_customers, p=[0.40, 0.45, 0.15]
    )
    payment_method = np.random.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
        size=n_customers,
        p=[0.35, 0.20, 0.25, 0.20],
    )

    monthly_charges = np.where(
        internet_service == "Fiber optic",
        np.random.uniform(70.0, 115.0, size=n_customers),
        np.where(
            internet_service == "DSL",
            np.random.uniform(40.0, 75.0, size=n_customers),
            np.random.uniform(18.0, 25.0, size=n_customers),
        ),
    )
    monthly_charges = np.round(monthly_charges, 2)
    total_charges = np.round(
        monthly_charges * tenure_months * np.random.uniform(0.95, 1.05), 2
    )

    churn_prob = np.where(
        contract_types == "Month-to-month", 0.40, 0.08
    ) + np.where(tenure_months < 12, 0.15, -0.05)
    churn_prob = np.clip(churn_prob, 0.05, 0.85)

    churn = np.where(np.random.rand(n_customers) < churn_prob, "Yes", "No")

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "tenure_months": tenure_months,
            "contract": contract_types,
            "internet_service": internet_service,
            "payment_method": payment_method,
            "monthly_charges": monthly_charges,
            "total_charges": total_charges,
            "churn": churn,
        }
    )

    df.loc[15:20, "total_charges"] = np.nan
    return df


def clean_and_process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans null values and engineers tenure tiers."""
    df_clean = df.copy()

    df_clean["total_charges"] = df_clean["total_charges"].fillna(
        df_clean["tenure_months"] * df_clean["monthly_charges"]
    )

    bins = [0, 12, 24, 48, 72]
    labels = ["0-1 Year", "1-2 Years", "2-4 Years", "4+ Years"]
    df_clean["tenure_cohort"] = pd.cut(
        df_clean["tenure_months"], bins=bins, labels=labels
    )

    df_clean["churn_numeric"] = (df_clean["churn"] == "Yes").astype(int)
    return df_clean


def run_churn_insights(df: pd.DataFrame):
    """Computes key retention metrics for business decision makers."""
    total_customers = len(df)
    churned_customers = df["churn_numeric"].sum()
    overall_churn_rate = (churned_customers / total_customers) * 100

    print("=== CUSTOMER RETENTION & CHURN SUMMARY ===")
    print(f"Total Base: {total_customers:,}")
    print(f"Churned: {churned_customers:,}")
    print(f"Overall Churn Rate: {overall_churn_rate:.2f}%\n")

    print("--- 1. Churn Rate by Contract Type ---")
    contract_summary = (
        df.groupby("contract")["churn_numeric"]
        .agg(
            Total="count",
            Churned="sum",
            Churn_Rate=lambda x: f"{x.mean()*100:.1f}%",
        )
        .reset_index()
    )
    print(contract_summary.to_string(index=False))

    print("\n--- 2. Churn Rate by Tenure Cohort ---")
    cohort_summary = (
        df.groupby("tenure_cohort")["churn_numeric"]
        .agg(
            Total="count",
            Churned="sum",
            Churn_Rate=lambda x: f"{x.mean()*100:.1f}%",
        )
        .reset_index()
    )
    print(cohort_summary.to_string(index=False))

    df.to_csv("customer_churn_cleaned.csv", index=False)
    print("\n[SUCCESS] Cleaned data exported as 'customer_churn_cleaned.csv'")


if __name__ == "__main__":
    raw_df = generate_churn_dataset(n_customers=7000)
    clean_df = clean_and_process_data(raw_df)
    run_churn_insights(clean_df)
