import psycopg2
from psycopg2 import sql

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
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

def create_tables(cursor):
    # Definir las sentencias SQL para crear las tablas
    create_customers_table = """
    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT NOT NULL,
        age INT NOT NULL CHECK (age > 0)
    );
    """
    
    create_categories_table = """
    CREATE TABLE categories (
        category_id BIGSERIAL PRIMARY KEY,
        category TEXT UNIQUE NOT NULL
    );
    """
    
    create_payment_methods_table = """
    CREATE TABLE payment_methods (
        payment_id BIGSERIAL PRIMARY KEY,
        payment_method TEXT UNIQUE NOT NULL
    );
    """
    
    create_shopping_malls_table = """
    CREATE TABLE shopping_malls (
        mall_id BIGSERIAL PRIMARY KEY,
        shopping_mall TEXT UNIQUE NOT NULL
    );
    """
    
    create_sales_table = """
    CREATE TABLE sales (
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
        except psycopg2.errors.DuplicateTable:
            print("La tabla ya existe.")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")

if __name__ == "__main__":
    create_database()
