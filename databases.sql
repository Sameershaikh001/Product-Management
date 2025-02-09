CREATE DATABASE product_management;
USE product_management;
CREATE TABLE products (
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL
);
select * from products;