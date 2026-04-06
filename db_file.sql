-- Active: 1775313214030@@127.0.0.1@3306
-- 1. Create Database
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- 2. Users Table (Role-Based Access)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    role ENUM('admin', 'employee')
);

-- 3. Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

-- 4. Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    cost_price DECIMAL(10,2) -- Added for Profit Analysis
);

-- 5. Orders Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 6. Order Items Table (The Analytics Core)
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    price_at_purchase DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 7. Payments Table
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    payment_method VARCHAR(50),
    payment_status VARCHAR(20),
    amount DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 8. Returns Table
CREATE TABLE returns (
    return_id INT PRIMARY KEY AUTO_INCREMENT,
    order_item_id INT,
    reason VARCHAR(100),
    refund_amount DECIMAL(10,2),
    FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id)
);

-- ---------------------------------------------------------
-- DUMMY DATA (Interconnected for Analysis)
-- ---------------------------------------------------------

-- Users
INSERT INTO users (name, email, role) VALUES 
('Varun Manager', 'varun@nexus.com', 'admin'),
('Rahul Staff', 'rahul@nexus.com', 'employee');

-- Customers
INSERT INTO customers (name, city, country) VALUES 
('Alice Johnson', 'New York', 'USA'),
('Bob Smith', 'London', 'UK'),
('Charlie Davis', 'Berlin', 'Germany'),
('Diana Prince', 'Paris', 'France'),
('Evan Wright', 'Tokyo', 'Japan');

-- Products (Mixing high-margin and low-margin items)
INSERT INTO products (name, category, price, cost_price) VALUES 
('iPhone 15', 'Electronics', 999.00, 600.00),
('Sony WH-1000XM5', 'Audio', 350.00, 200.00),
('MacBook Air', 'Laptops', 1200.00, 850.00),
('USB-C Cable', 'Accessories', 25.00, 5.00),
('Logitech Mouse', 'Accessories', 50.00, 30.00);

-- Orders (Scenario: Alice and Bob are frequent shoppers)
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES 
(1, '2024-03-01', 1024.00, 'Delivered'),
(1, '2024-03-15', 350.00, 'Delivered'),
(2, '2024-03-10', 1200.00, 'Shipped'),
(3, '2024-03-20', 50.00, 'Processing'),
(4, '2024-03-22', 25.00, 'Cancelled');

-- Order Items (Linking Orders to Products)
INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES 
(1, 1, 1, 999.00), -- Alice bought iPhone
(1, 4, 1, 25.00),  -- Alice bought Cable
(2, 2, 1, 350.00), -- Alice bought Sony Headphones
(3, 3, 1, 1200.00),-- Bob bought MacBook
(4, 5, 1, 50.00);  -- Charlie bought Mouse

-- Payments
INSERT INTO payments (order_id, payment_method, payment_status, amount) VALUES 
(1, 'Credit Card', 'Completed', 1024.00),
(2, 'PayPal', 'Completed', 350.00),
(3, 'Credit Card', 'Pending', 1200.00),
(4, 'Debit Card', 'Completed', 50.00);

-- Returns (Scenario: Alice returned the cable, highly useful for Decision Agent)
INSERT INTO returns (order_item_id, reason, refund_amount) VALUES 
(2, 'Defective', 25.00);