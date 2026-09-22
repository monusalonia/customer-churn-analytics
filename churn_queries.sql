-- Customer Churn & Cohort Analysis Queries
-- PostgreSQL / MySQL Compatible

-- 1. Overall Churn Rate & Monthly Revenue at Risk
SELECT 
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(AVG(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS lost_monthly_revenue
FROM customers;

-- 2. Churn Segmentation by Payment Method
SELECT 
    payment_method,
    COUNT(customer_id) AS total_users,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_users,
    ROUND(AVG(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;

-- 3. High-Risk Customer Identification (Tenure < 12 mos, Month-to-Month, Monthly Charges > $80)
SELECT 
    customer_id,
    tenure_months,
    contract,
    monthly_charges,
    payment_method
FROM customers
WHERE churn = 'No'
  AND contract = 'Month-to-month'
  AND tenure_months <= 12
  AND monthly_charges > 80.0
ORDER BY monthly_charges DESC
LIMIT 100;
