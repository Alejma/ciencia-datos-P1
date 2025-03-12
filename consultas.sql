-- i. Total de ventas por categoría de producto (sin category_name)
-- Esta consulta SQL realiza un análisis de ventas agrupadas por categoría.
-- Selecciona el número total de ventas, la cantidad de unidades vendidas y el importe total de ventas para cada categoría.
-- Utiliza una unión (JOIN) entre las tablas 'sales' y 'categories' basada en 'category_id'.
-- Agrupa los resultados por 'category_id' y los ordena en orden descendente según el importe total de ventas.
SELECT 
    COUNT(s.invoice_no) AS numero_ventas,
    SUM(s.quantity) AS unidades_vendidas,
    SUM(s.quantity * s.price) AS importe_total
FROM 
    sales s
JOIN 
    categories c ON s.category_id = c.category_id
GROUP BY 
    c.category_id
ORDER BY 
    importe_total DESC;

-- ii. Clientes con mayor volumen de compras
-- Esta consulta SQL identifica a los clientes con el mayor volumen de compras.
-- Selecciona el número de compras, la cantidad de unidades compradas y el importe total de compras para cada cliente.
-- Utiliza una unión (JOIN) entre las tablas 'sales' y 'customers' basada en 'customer_id'.
-- Agrupa los resultados por 'customer_id' y 'name' y los ordena en orden descendente según el importe total de compras.

SELECT 
    c.customer_id,
    c.name,
    COUNT(s.invoice_no) AS numero_compras,
    SUM(s.quantity) AS unidades_compradas,
    SUM(s.quantity * s.price) AS importe_total
FROM 
    sales s
JOIN 
    customers c ON s.customer_id = c.customer_id
GROUP BY 
    c.customer_id, c.name
ORDER BY 
    importe_total DESC
LIMIT 10;

-- iii. Métodos de pago más utilizados
-- Esta consulta SQL analiza los métodos de pago más utilizados en las transacciones.
-- Selecciona el método de pago, el número de transacciones y el importe total de las transacciones para cada método.
-- Utiliza una unión (JOIN) entre las tablas 'sales' y 'payment_methods' basada en 'payment_id'.
-- Agrupa los resultados por 'payment_method' y los ordena en orden descendente
-- según el número de transacciones.
SELECT 
    p.payment_method,
    COUNT(s.invoice_no) AS numero_transacciones,
    SUM(s.quantity * s.price) AS importe_total
FROM 
    sales s
JOIN 
    payment_methods p ON s.payment_id = p.payment_id
GROUP BY 
    p.payment_method
ORDER BY 
    numero_transacciones DESC;

-- iv. Comparación de ventas por mes
-- Esta consulta SQL compara las ventas mensuales de los años 2021, 2022 y 2023.
-- Selecciona el mes, el importe total de ventas para cada año y el importe total de ventas para cada mes.
-- Utiliza la función EXTRACT para extraer el mes de la fecha de la factura.
-- Agrupa los resultados por mes y los ordena en orden ascendente según el mes.
SELECT
    EXTRACT(MONTH FROM invoice_date) AS mes,
    SUM(CASE WHEN EXTRACT(YEAR FROM invoice_date) = 2021
     THEN quantity * price END) AS "2021",
    SUM(CASE WHEN EXTRACT(YEAR FROM invoice_date) = 2022 
    THEN quantity * price END) AS "2022",
    SUM(CASE WHEN EXTRACT(YEAR FROM invoice_date) = 2023 
    THEN quantity * price END) AS "2023",
    SUM(quantity * price) AS total
FROM sales
GROUP BY mes
ORDER BY mes;


-- Consulta adicional: Ventas por centro comercial
-- Esta consulta SQL analiza las ventas por centro comercial en términos de número de ventas, unidades vendidas e importe total.
-- Selecciona el nombre del centro comercial, el número de ventas, unidades vendidas e importe total para cada centro comercial.
-- Utiliza una unión (JOIN) entre las tablas 'sales' y 'shopping_malls' basada en 'mall_id'.
-- Agrupa los resultados por 'mall_name' y los ordena en orden descendente según el importe total de ventas.

SELECT 
    m.mall_name,
    COUNT(s.invoice_no) AS numero_ventas,
    SUM(s.quantity) AS unidades_vendidas,
    SUM(s.quantity * s.price) AS importe_total
FROM 
    sales s
JOIN 
    shopping_malls m ON s.mall_id = m.mall_id
GROUP BY 
    m.mall_name
ORDER BY 
    importe_total DESC;

-- Creación de índices para optimizar las consultas
-- Se crean índices en las tablas 'sales' y 'categories' para acelerar las consultas.

CREATE INDEX idx_sales_customer ON sales(customer_id);
CREATE INDEX idx_sales_category ON sales(category_id);
CREATE INDEX idx_sales_payment ON sales(payment_id);
CREATE INDEX idx_sales_mall ON sales(mall_id);
CREATE INDEX idx_sales_date ON sales(invoice_date);
CREATE INDEX idx_sales_date_category ON sales(invoice_date, category_id);

-- Vista materializada para acelerar la consulta 
-- de ventas por categoría (sin category_name)
-- Se crea una vista materializada 'mv_sales_by_category' para almacenar los resultados de la consulta de ventas por categoría.
-- La vista materializada se actualiza automáticamente cuando se realizan cambios en las tablas subyacentes.
CREATE MATERIALIZED VIEW mv_sales_by_category AS
SELECT 
    COUNT(s.invoice_no) AS numero_ventas,
    SUM(s.quantity) AS unidades_vendidas,
    SUM(s.quantity * s.price) AS importe_total
FROM 
    sales s
JOIN 
    categories c ON s.category_id = c.category_id
GROUP BY 
    c.category_id
ORDER BY 
    importe_total DESC;

-- Comando para refrescar la vista materializada
-- REFRESH MATERIALIZED VIEW mv_sales_by_category;
