import sqlite3


def read_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    print("#################")
    print("ARTICLES:")
    for row in c.execute('SELECT * FROM articles'):
        print(row)
    print("#################")
    print("VOTES:")
    for row in c.execute('SELECT * FROM votes'):
        print(row)
    print("#################")
    print("PROBLEMS:")
    for row in c.execute('SELECT * FROM problems'):
        print(row)
    print("#################")
    print("COMMENTS:")
    for row in c.execute('SELECT * FROM comments'):
        print(row)
    print("#################")
    print("EDITS:")
    for row in c.execute('SELECT * FROM edits'):
        print(row)
    conn.close()

read_db()
    
