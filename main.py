import sqlite3
import urllib.request, json
import time
import os.path
from os import path

def int_to_time(x):
    return time.strftime('%H:%M:%S', time.gmtime(x+3600))

def parse(c, conn):
    with urllib.request.urlopen("https://www.meneame.net/backend/sneaker2") as url:
        data = json.loads(url.read().decode())
    for e in data['events']:
        lin = e['link']
        tit = e['title']
        act = e['type']
        wh = e['who']
        t = int_to_time(int(e['ts']))
        if(act == "post" or act == "new"):
            c.execute('SELECT count(*) FROM articles WHERE link = ? AND creation_time = ? AND who = ?',[lin,t,wh])
            if(c.fetchone()[0] == 0):
                print("Inserted: " + tit)
                c.execute('INSERT INTO articles VALUES (?,?,?,?)', [lin, tit, wh, t])
                conn.commit()
        else:
            c.execute('SELECT count(*) FROM articles WHERE link = ?', [lin])
            if(c.fetchone()[0] == 1):
                c.execute('SELECT count(*) FROM actions WHERE link = ? AND action_time = ? AND who = ?',[lin,t,wh])
                if(c.fetchone()[0] == 0):
                    print("Inserted action: " + act + " on title: " + tit)
                    c.execute('INSERT INTO actions VALUES (?,?,?,?)', [lin, act, wh, t])
                    conn.commit()
def main():
    x = path.exists('articles.db')
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    #Create tables
    if(not x):
        c.execute('''CREATE TABLE articles
        (link varchar, title varchar, who varchar, creation_time time)''')
        c.execute('''CREATE TABLE actions
        (link varchar, action varchar, who varchar, action_time time)''')
        conn.commit()
    while(True):
        parse(c, conn)
    

main()
        


