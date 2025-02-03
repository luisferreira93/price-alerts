import psycopg2

from db.price import Price


def connect_db():
    conn = psycopg2.connect(
        dbname="mydatabase",  # Default database name in the PostgreSQL container
        user="postgres",    # Default user
        password="postgres",  # Password you set when starting the container
        host="localhost",   # Since you're running Docker locally
        port="5433"         # Default PostgreSQL port
    )
    cursor = conn.cursor()

    try:
        # Execute your SELECT query (you can change the table name to the one you're interested in)
        cursor.execute("SELECT * FROM prices;")  # Change to your desired table

        # Fetch the results
        rows = cursor.fetchall()

        # Process and display the results
        for row in rows:
            print(row)

    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the cursor and connection
    return conn


def insert_price(connection, product: Price):
    cursor = connection.cursor()
    
    try:
        # Define the SQL INSERT query
        insert_query = """
        INSERT INTO prices (name, category, price, link, last_discount, last_update, store)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Prepare the data to be inserted (mapping from the PriceDTO object)
        data = (
            product.name,
            product.category,
            product.price,
            product.link,
            product.last_discount,
            product.last_update,
            product.store
        )
        
        # Execute the query
        cursor.execute(insert_query, data)
        
        # Commit the transaction
        connection.commit()
        print(f"Product {product.name} inserted successfully.")
    
    except Exception as e:
        print(f"An error occurred while inserting product {product.name}: {e}")
        connection.rollback()  # Rollback in case of error
    
    finally:
        cursor.close()

def close_db(connection):
    connection.close()