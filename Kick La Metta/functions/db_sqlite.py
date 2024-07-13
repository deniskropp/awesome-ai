import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def execute_query(conn, query):
    """Execute a single query."""
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def fetch_all(conn, query):
    """Fetch all results from a query."""
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except sqlite3.Error as e:
        print(e)
        return None

def main():
    database = "example.db"

    # Create a database connection
    conn = create_connection(database)
    with conn:
        # Example query to create a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY,
            name text NOT NULL,
            age integer
        );"""
        execute_query(conn, create_table_query)

        # Example query to insert data
        insert_query = """
        INSERT INTO users (name, age) VALUES ('Alice', 30),
                                              ('Bob', 25),
                                              ('Charlie', 35);"""
        execute_query(conn, insert_query)

        # Example query to fetch data
        select_query = "SELECT * FROM users;"
        rows = fetch_all(conn, select_query)

        for row in rows:
            print(row)

if __name__ == '__main__':
    main()
