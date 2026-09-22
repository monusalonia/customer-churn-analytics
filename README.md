# Customer Churn & Retention Analytics Dashboard

An end-to-end data analytics project uncovering customer attrition patterns and identifying high-value retention opportunities.

## Tech Stack
- **Data Analysis & Modeling:** Python (Pandas, NumPy)
- **Database Querying & Segmentation:** SQL (Window Functions, Aggregations)
- **Dashboard & Reporting:** Tableau / Power BI
- **Version Control:** Git & GitHub

## Business Context
Acquiring new customers costs 5x to 7x more than retaining existing ones. This project analyzes 7,000+ customer records to determine churn triggers across contract lengths, tenure cohorts, and billing options, providing data-driven recommendations to reduce subscriber attrition.

## Key Findings
1. **Contract Exposure:** Customers on month-to-month contracts exhibit an attrition rate ~5x higher than those on 1- or 2-year contracts.
2. **Critical Onboarding Window:** Over 60% of all churn occurs within the first 12 months of tenure.
3. **Payment Friction:** Accounts paying via Electronic Check display higher churn compared to credit card or automated bank transfer methods.

## Repository Contents
- `churn_analysis.py` — Complete data cleaning, cohort binning, and statistical aggregation pipeline.
- `churn_queries.sql` — Production queries calculating churn percentages, revenue risk, and target outreach lists.
