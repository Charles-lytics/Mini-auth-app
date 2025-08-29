import sqlite3

def main():
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    # Check if the table already exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
    ''')
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                auth_level REAL NOT NULL
            );
        ''')
        print("Table created successfully.")
    else:
        print("Table already exists.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()