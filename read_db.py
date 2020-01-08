import sqlite3


def read_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM articles'):
        print(row)
    print("#################")
    for row in c.execute('SELECT * FROM actions'):
        print(row)
    conn.close()

read_db()
    
