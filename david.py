import mysql.connector

def fetchall_query(query, params=None):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='31356mysql29@',
        database='retail_store'
    )
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    conn.close()
    return results

# 1. List all customers.
query1 = "SELECT * FROM Customers"
customers = fetchall_query(query1)
print("All Customers:", customers)

# 2. Find all orders placed in January 2023.
query2 = """
SELECT * FROM Orders
WHERE OrderDate BETWEEN '2023-01-01' AND '2023-01-31'
"""
orders_january = fetchall_query(query2)
print("Orders in January 2023:", orders_january)

# 3. Get the details of each order, including the customer name and email.
query3 = """
SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, Orders.OrderDate 
FROM Orders
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
"""
order_details = fetchall_query(query3)
print("Order Details:", order_details)

# 4. List the products purchased in a specific order (e.g., OrderID = 1).
order_id = 1
query4 = """
SELECT Products.ProductName, OrderItems.Quantity 
FROM OrderItems
JOIN Products ON OrderItems.ProductID = Products.ProductID
WHERE OrderItems.OrderID = %s
"""
order_products = fetchall_query(query4, (order_id,))
print(f"Products in Order {order_id}:", order_products)

# 5. Calculate the total amount spent by each customer.
query5 = """
SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, 
SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName
"""
total_spent = fetchall_query(query5)
print("Total Spent by Each Customer:", total_spent)

# 6. Find the most popular product (the one that has been ordered the most).
query6 = """
SELECT Products.ProductID, Products.ProductName, 
SUM(OrderItems.Quantity) AS TotalQuantityOrdered
FROM OrderItems
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Products.ProductID, Products.ProductName
ORDER BY TotalQuantityOrdered DESC
LIMIT 1
"""
most_popular_product = fetchall_query(query6)
print("Most Popular Product:", most_popular_product)

# 7. Get the total number of orders and the total sales amount for each month in 2023.
query7 = """
SELECT DATE_FORMAT(OrderDate, '%Y-%m') AS Month, 
COUNT(DISTINCT Orders.OrderID) AS TotalOrders, 
SUM(Products.Price * OrderItems.Quantity) AS TotalSalesAmount
FROM Orders
JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
WHERE YEAR(OrderDate) = 2023
GROUP BY DATE_FORMAT(OrderDate, '%Y-%m')
"""
monthly_sales = fetchall_query(query7)
print("Monthly Sales in 2023:", monthly_sales)

# 8. Find customers who have spent more than $1000.
query8 = """
SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, 
SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName
HAVING TotalSpent > 1000
"""
big_spenders = fetchall_query(query8)
print("Customers who spent more than $1000:", big_spenders)