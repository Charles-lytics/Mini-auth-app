import sqlite3
from users import users

def main():
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    for user in users:
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user['user_id'],))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (user_id, username, password, auth_level) VALUES (?, ?, ?, ?)",
                           (user['user_id'], user['username'], user['password'], user['auth_level']))

    conn.commit()
    conn.close()

    print("Data inserted successfully.")

if __name__ == '__main__':
    main()