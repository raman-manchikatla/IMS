import sqlite3

conn = sqlite3.connect('mynewsql.db')
cur = conn.cursor()
#cur.execute('create table student(sid int, sname varchar(20))')
cur.execute('insert into student values (1,"raman")')
conn.commit()

