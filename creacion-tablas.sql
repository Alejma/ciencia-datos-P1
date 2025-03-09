-- Crear la tabla de Clientes
CREATE TABLE customers (
    customer_id VARCHAR(50),
    name VARCHAR(100),  -- Puede ser NULL
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL CHECK (age > 0)
);

-- Crear la tabla de Categorías de Productos
CREATE TABLE categories (
    category_id SERIAL,
    category_name VARCHAR(50) UNIQUE NOT NULL
);

-- Crear la tabla de Métodos de Pago
CREATE TABLE payment_methods (
    payment_id SERIAL,
    payment_method VARCHAR(50) UNIQUE NOT NULL
);

-- Crear la tabla de Centros Comerciales
CREATE TABLE shopping_malls (
    mall_id SERIAL,
    mall_name VARCHAR(100) UNIQUE NOT NULL
);

-- Crear la tabla de Ventas (Hechos)
CREATE TABLE sales (
    invoice_no VARCHAR(50),
    customer_id VARCHAR(50),
    category_id INT,
    payment_id INT,
    mall_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    invoice_date DATE NOT NULL
);
