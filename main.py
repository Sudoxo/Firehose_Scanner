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
                #VOTES
                if(act == "vote"):
                    c.execute('SELECT count(*) FROM votes WHERE link = ? AND action_time = ? AND who = ?',[lin,t,wh])
                    if(c.fetchone()[0] == 0):
                        print("Inserted action: " + act + " on title: " + tit)
                        c.execute('INSERT INTO votes VALUES (?,?,?)', [lin, wh, t])
                        conn.commit()
                #PROBLEMS
                elif(act == "problem"):
                    c.execute('SELECT count(*) FROM problems WHERE link = ? AND action_time = ? AND who = ?',[lin,t,wh])
                    if(c.fetchone()[0] == 0):
                        print("Inserted action: " + act + " on title: " + tit)
                        c.execute('INSERT INTO problems VALUES (?,?,?)', [lin, wh, t])
                        conn.commit()
                #COMMENTS
                elif(act == "comment"):
                    c.execute('SELECT count(*) FROM comments WHERE link = ? AND action_time = ? AND who = ?',[lin,t,wh])
                    if(c.fetchone()[0] == 0):
                        print("Inserted action: " + act + " on title: " + tit)
                        c.execute('INSERT INTO comments VALUES (?,?,?)', [lin, wh, t])
                        conn.commit()
                #EDITS
                elif(act == "cedited"):
                    c.execute('SELECT count(*) FROM edits WHERE link = ? AND action_time = ? AND who = ?',[lin,t,wh])
                    if(c.fetchone()[0] == 0):
                        print("Inserted action: " + act + " on title: " + tit)
                        c.execute('INSERT INTO edits VALUES (?,?,?)', [lin, wh, t])
                        conn.commit()
def main():
    x = path.exists('articles.db')
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    #Create tables
    if(not x):
        c.execute('''CREATE TABLE articles
        (link varchar, title varchar, who varchar, creation_time time)''')
        c.execute('''CREATE TABLE votes
        (link varchar, who varchar, action_time time)''')
        c.execute('''CREATE TABLE problems
        (link varchar, who varchar, action_time time)''')
        c.execute('''CREATE TABLE comments
        (link varchar, who varchar, action_time time)''')
        c.execute('''CREATE TABLE edits
        (link varchar, who varchar, action_time time)''')
        conn.commit()
    while(True):
        parse(c, conn)
    

main()
        


