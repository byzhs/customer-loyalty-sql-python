import sqlite3

conn = sqlite3.connect("loyalty_data.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    join_date TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    price REAL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    transaction_date TEXT,
    amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
''')

cursor.executemany('''
INSERT INTO customers (first_name, last_name, email, join_date)
VALUES (?, ?, ?, ?);
''', [
    ('John', 'Doe', 'john@example.com', '2024-01-01'),
    ('Jane', 'Smith', 'jane@example.com', '2024-02-10'),
    ('Alice', 'Lee', 'alice@example.com', '2024-03-15')
])

cursor.executemany('''
INSERT INTO products (product_name, price)
VALUES (?, ?);
''', [
    ('Product A', 25.99),
    ('Product B', 40.50),
    ('Product C', 15.75)
])

cursor.executemany('''
INSERT INTO transactions (customer_id, product_id, transaction_date, amount)
VALUES (?, ?, ?, ?);
''', [
    (1, 1, '2024-04-01', 25.99),
    (2, 2, '2024-04-02', 40.50),
    (1, 3, '2024-04-03', 15.75),
    (3, 1, '2024-04-04', 25.99),
    (2, 1, '2024-04-05', 25.99)
])

conn.commit()
conn.close()
print("✅ Database created and populated: db/loyalty_data.db")
