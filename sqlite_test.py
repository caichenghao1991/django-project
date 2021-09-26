import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute('UPDATE auth_user(id, password, is_superuser, username, email) values (1, "123456",))')
for i in cursor.fetchall():
    print(i)
