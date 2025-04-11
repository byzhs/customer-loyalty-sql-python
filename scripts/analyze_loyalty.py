import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("loyalty_data.db")

# SQL Queries
revenue_query = """
SELECT SUM(amount) AS total_revenue
FROM transactions;
"""
top_customers_query = """
SELECT c.first_name || ' ' || c.last_name AS customer_name,
       SUM(t.amount) AS total_spent
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY t.customer_id
ORDER BY total_spent DESC;
"""
top_products_query = """
SELECT p.product_name,
       COUNT(t.transaction_id) AS purchases
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_id
ORDER BY purchases DESC;
"""
monthly_revenue_query = """
SELECT strftime('%Y-%m', transaction_date) AS month,
       SUM(amount) AS total_revenue
FROM transactions
GROUP BY month
ORDER BY month;
"""
repeat_customers_query = """
SELECT c.customer_id,
       c.first_name || ' ' || c.last_name AS customer_name,
       COUNT(t.transaction_id) AS transaction_count
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id
ORDER BY transaction_count DESC;
"""

# Run Queries
revenue = pd.read_sql(revenue_query, conn)
top_customers = pd.read_sql(top_customers_query, conn)
top_products = pd.read_sql(top_products_query, conn)
monthly_revenue = pd.read_sql(monthly_revenue_query, conn)
repeat_customers = pd.read_sql(repeat_customers_query, conn)

conn.close()

# Print outputs
print("Total Revenue:\n", revenue)
print("\nTop Customers:\n", top_customers)
print("\nTop Purchased Products:\n", top_products)
print("\nMonthly Revenue:\n", monthly_revenue)
print("\nCustomer Transaction Counts:\n", repeat_customers)

# Visuals
plt.figure(figsize=(8, 5))
plt.bar(top_customers["customer_name"], top_customers["total_spent"], color="skyblue")
plt.title("Top Spending Customers")
plt.xlabel("Customer")
plt.ylabel("Total Spent ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_customers_chart.png")
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(top_products["product_name"], top_products["purchases"], color="lightgreen")
plt.title("Most Purchased Products")
plt.xlabel("Product")
plt.ylabel("Number of Purchases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_products_chart.png")
plt.show()

# Export
with pd.ExcelWriter("loyalty_report.xlsx", engine="openpyxl") as writer:
    revenue.to_excel(writer, sheet_name="Revenue", index=False)
    top_customers.to_excel(writer, sheet_name="Top Customers", index=False)
    top_products.to_excel(writer, sheet_name="Top Products", index=False)
    monthly_revenue.to_excel(writer, sheet_name="Monthly Revenue", index=False)
    repeat_customers.to_excel(writer, sheet_name="Customer Frequency", index=False)

print("✅ All data exported and visuals saved.")
