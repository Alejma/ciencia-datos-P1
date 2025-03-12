import psycopg2
from psycopg2 import sql
import pandas as pd
import os

def create_database():
    # Parámetros de conexión 
    conn_params = {
        'host': 'localhost',
        'user': 'postgres',
        'password': '1975', 
        'port': '5432'
    }
    
    # Nombre de la base de datos 
    db_name = 'store_db'
    
    # Conectar a postgres para crear la base de datos
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Crear la base de datos si no existe
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Base de datos '{db_name}' creada exitosamente.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"La base de datos '{db_name}' ya existe.")
    
    # Cerrar la conexión
    cursor.close()
    conn.close()
    
    # Actualizar los parámetros para conectar a la nueva base de datos
    conn_params['dbname'] = db_name
    
    # Conectar a la nueva base de datos
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cursor = conn.cursor()
        print(f"Conectado a la base de datos '{db_name}'.")
        
        # Crear las tablas
        create_tables(cursor)
        
        # Cargar datos desde el CSV
        load_data_from_csv(conn)
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

def create_tables(cursor):
    # Definir las sentencias SQL para crear las tablas
    create_customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT DEFAULT NULL,
        email TEXT DEFAULT NULL,
        gender TEXT NOT NULL,
        age INT NOT NULL CHECK (age > 0)
    );
    """
    
    create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        category_id BIGSERIAL PRIMARY KEY,
        category TEXT UNIQUE NOT NULL
    );
    """
    
    create_payment_methods_table = """
    CREATE TABLE IF NOT EXISTS payment_methods (
        payment_id BIGSERIAL PRIMARY KEY,
        payment_method TEXT UNIQUE NOT NULL
    );
    """
    
    create_shopping_malls_table = """
    CREATE TABLE IF NOT EXISTS shopping_malls (
        mall_id BIGSERIAL PRIMARY KEY,
        shopping_mall TEXT UNIQUE NOT NULL
    );
    """
    
    create_sales_table = """
    CREATE TABLE IF NOT EXISTS sales (
        invoice_no TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
        category_id BIGINT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
        payment_id BIGINT NOT NULL REFERENCES payment_methods(payment_id) ON DELETE CASCADE,
        mall_id BIGINT NOT NULL REFERENCES shopping_malls(mall_id) ON DELETE CASCADE,
        quantity INT NOT NULL CHECK (quantity > 0),
        price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
        invoice_date TIMESTAMP NOT NULL
    );
    """
    
    # Lista de todas las sentencias SQL a ejecutar
    create_statements = [
        create_customers_table,
        create_categories_table,
        create_payment_methods_table,
        create_shopping_malls_table,
        create_sales_table
    ]
    
    # Ejecutar cada sentencia SQL
    for statement in create_statements:
        try:
            cursor.execute(statement)
            print("Tabla creada exitosamente.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")

def load_data_from_csv(conn):
    # Ruta al archivo CSV
    csv_path = os.path.join("dataset", "customer_shopping_data.csv")
    
    try:
        # Cargar el CSV en un DataFrame
        df = pd.read_csv(csv_path)
        print(f"CSV cargado correctamente: {len(df)} registros encontrados.")
        
        cursor = conn.cursor()
        
        # Insertar categorías únicas
        unique_categories = df['category'].unique()
        for category in unique_categories:
            try:
                cursor.execute(
                    "INSERT INTO categories (category) VALUES (%s) ON CONFLICT (category) DO NOTHING",
                    (category,)
                )
            except Exception as e:
                print(f"Error al insertar categoría {category}: {e}")
        
        # Insertar métodos de pago únicos
        unique_payment_methods = df['payment_method'].unique()
        for payment_method in unique_payment_methods:
            try:
                cursor.execute(
                    "INSERT INTO payment_methods (payment_method) VALUES (%s) ON CONFLICT (payment_method) DO NOTHING",
                    (payment_method,)
                )
            except Exception as e:
                print(f"Error al insertar método de pago {payment_method}: {e}")
        
        # Insertar centros comerciales únicos
        unique_malls = df['shopping_mall'].unique()
        for mall in unique_malls:
            try:
                cursor.execute(
                    "INSERT INTO shopping_malls (shopping_mall) VALUES (%s) ON CONFLICT (shopping_mall) DO NOTHING",
                    (mall,)
                )
            except Exception as e:
                print(f"Error al insertar centro comercial {mall}: {e}")
        
        # Insertar clientes únicos con name y email como NULL por defecto
        unique_customers = df[['customer_id', 'gender', 'age']].drop_duplicates()
        for _, customer in unique_customers.iterrows():
            try:
                cursor.execute(
                    "INSERT INTO customers (customer_id, name, email, gender, age) VALUES (%s, NULL, NULL, %s, %s) ON CONFLICT (customer_id) DO NOTHING",
                    (customer['customer_id'], customer['gender'], customer['age'])
                )
            except Exception as e:
                print(f"Error al insertar cliente {customer['customer_id']}: {e}")
        
        # Insertar ventas
        for _, row in df.iterrows():
            try:
                # Obtener IDs de referencia
                cursor.execute("SELECT category_id FROM categories WHERE category = %s", (row['category'],))
                category_id = cursor.fetchone()[0]
                
                cursor.execute("SELECT payment_id FROM payment_methods WHERE payment_method = %s", (row['payment_method'],))
                payment_id = cursor.fetchone()[0]
                
                cursor.execute("SELECT mall_id FROM shopping_malls WHERE shopping_mall = %s", (row['shopping_mall'],))
                mall_id = cursor.fetchone()[0]
                
                # Formatear la fecha
                try:
                    # Intentar convertir fecha si es necesario
                    invoice_date = pd.to_datetime(row['invoice_date'])
                except:
                    invoice_date = row['invoice_date']
                
                # Insertar venta
                cursor.execute(
                    """
                    INSERT INTO sales 
                    (invoice_no, customer_id, category_id, payment_id, mall_id, quantity, price, invoice_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (invoice_no) DO NOTHING
                    """,
                    (
                        row['invoice_no'], 
                        row['customer_id'], 
                        category_id, 
                        payment_id, 
                        mall_id, 
                        row['quantity'], 
                        row['price'], 
                        invoice_date
                    )
                )
            except Exception as e:
                print(f"Error al insertar venta {row['invoice_no']}: {e}")
        
        conn.commit()
        print("Datos cargados correctamente en la base de datos.")
        
    except Exception as e:
        print(f"Error al cargar datos desde CSV: {e}")
        conn.rollback()

if __name__ == "__main__":
    create_database()