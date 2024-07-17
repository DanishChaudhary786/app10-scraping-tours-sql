import sqlite3

# Establish a connection to the database
connection = sqlite3.connect("example.db")
cursor = connection.cursor()


# Query data
# cursor.execute("insert into events values('AJ','AJ','17-07-2024')")
cursor.execute("SELECT * FROM events")

rows = cursor.fetchall()
print(rows)

# Insert many rows
# new_rows = [('AK', 'AKC', '17-07-2024'),
#             ('AJ', 'AJ', '17-07-2024'),
#             ('AJK', 'AJK', '17-07-2024')]
#
# cursor.executemany("insert into events values(?,?,?)", new_rows)
cursor.execute("DELETE FROM events WHERE name = ''")
connection.commit()


# Close the connection
connection.close()
