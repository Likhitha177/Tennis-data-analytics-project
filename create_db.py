import sqlite3

conn = sqlite3.connect("tennis_db.db")
cursor = conn.cursor()

with open("tennis_db.sql", "r") as file:
    sql_script = file.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Database and tables created successfully!")