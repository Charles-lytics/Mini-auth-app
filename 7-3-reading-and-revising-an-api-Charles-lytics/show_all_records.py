import sqlite3

def showRecords():
    title = "All Records From the Table Users: "
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(title)
    for row in rows:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
    conn.close()

showRecords()
