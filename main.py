# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
df_boston = pd.read_sql("""SELECT firstName, lastName FROM employees
                        JOIN offices USING (officeCode) 
                        WHERE city = 'Boston'""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""SELECT o.officeCode, o.city, o.country
                            FROM offices o
                            LEFT JOIN employees e
                                ON o.officeCode = e.officeCode
                            WHERE e.employeeNumber IS NULL;""", conn)

# STEP 3
df_employee = pd.read_sql("""SELECT e.firstName, e.lastName, o.city, o.state
                            FROM employees e
                            LEFT JOIN offices o
                                ON e.officeCode = o.officeCode
                            ORDER BY e.firstName, e.lastName;""", conn)

# STEP 4
df_contacts = pd.read_sql("""SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
                            FROM customers c
                            LEFT JOIN orders o 
                                ON c.customerNumber = o.customerNumber
                            WHERE o.orderNumber IS NULL
                            ORDER BY c.contactLastName ASC;""", conn)

# STEP 5
df_payment = pd.read_sql("""SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
                            FROM customers c
                            JOIN payments p 
                                ON c.customerNumber = p.customerNumber
                            ORDER BY CAST(p.amount AS REAL) DESC;""", conn)

# STEP 6
df_credit = pd.read_sql("""SELECT e.employeeNumber, e.firstName, e.lastName,
                                COUNT(c.customerNumber) AS total_customers
                            FROM employees e
                            JOIN customers c
                                ON e.employeeNumber = c.salesRepEmployeeNumber
                            GROUP BY e.employeeNumber, e.firstName, e.lastName
                            HAVING AVG(c.creditLimit) > 90000
                            ORDER BY total_customers DESC
                            LIMIT 4;""", conn)

# STEP 7
df_product_sold = pd.read_sql("""SELECT p.productName,
                                    COUNT(od.orderNumber) AS numorders,
                                    SUM(od.quantityOrdered) AS totalunits
                                FROM products p
                                JOIN orderdetails od
                                    ON p.productCode = od.productCode
                                GROUP BY p.productName
                                ORDER BY totalunits DESC;""", conn)

# STEP 8
df_total_customers = pd.read_sql("""SELECT p.productName, p.productCode,
                                        COUNT(DISTINCT c.customerNumber) AS numpurchasers
                                FROM products p
                                JOIN orderdetails od
                                    ON p.productCode = od.productCode
                                JOIN orders o
                                    ON od.orderNumber = o.orderNumber
                                JOIN customers c
                                    ON o.customerNumber = c.customerNumber
                                GROUP BY p.productName, p.productCode
                                ORDER BY numpurchasers DESC;""", conn)

# STEP 9
df_customers = pd.read_sql("""SELECT o.officeCode, o.city,
       COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e
    ON o.officeCode = e.officeCode
LEFT JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city;""", conn)

# STEP 10
df_under_20 = pd.read_sql("""WITH low_performing_products AS (
    SELECT p.productCode, COUNT(DISTINCT c.customerNumber) AS n_customers
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    JOIN customers c
        ON o.customerNumber = c.customerNumber
    GROUP BY p.productCode
    HAVING n_customers < 20)
SELECT 
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    o.officeCode
FROM employees e
JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord
    ON c.customerNumber = ord.customerNumber
JOIN orderdetails od
    ON ord.orderNumber = od.orderNumber
JOIN offices o
    ON e.officeCode = o.officeCode
JOIN low_performing_products lpp
    ON od.productCode = lpp.productCode
GROUP BY e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
ORDER BY e.lastName ASC, e.firstName ASC;

""", conn)

conn.close()