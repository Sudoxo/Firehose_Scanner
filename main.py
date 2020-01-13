import sqlite3
import urllib.request, json
import time
import os.path
from os import path

def int_to_time(x):
    return time.strftime('%H:%M:%S', time.gmtime(x+3600))
last = [0,"","",""]
def parse(c, conn):
    global last
    with urllib.request.urlopen("https://www.meneame.net/backend/sneaker2") as url:
        data = json.loads(url.read().decode())
    flag = 0
    for e in reversed(data['events']):
        lin = e['link']
        tit = e['title']
        act = e['type']
        wh = e['who']
        t = int_to_time(int(e['ts']))
        if(flag == 0):
            if(int(e['ts']) < last[0]):
                continue
            if(int(e['ts']) == last[0]):
                if(wh == last[1] and act == last[2] and lin == last[3]):
                    flag = 1
                continue
        flag = 1
        ############print(str(t) + "    " + tit)
        if(act == "post" or act == "new"):
            print("Inserted: " + tit)
            c.execute('INSERT INTO articles VALUES (?,?,?,?)', [tit, lin, wh, t])
            conn.commit()
                
        else:
            c.execute('SELECT count(*) FROM articles WHERE title = ?', [tit])
            if(c.fetchone()[0] == 1):
                #VOTES
                if(act == "vote"):
                    print("Inserted action: " + act + " on title: " + tit)
                    c.execute('INSERT INTO votes VALUES (?,?,?)', [tit, wh, t])
                    conn.commit()
                #PROBLEMS
                elif(act == "problem"):
                    print("Inserted action: " + act + " on title: " + tit)
                    c.execute('INSERT INTO problems VALUES (?,?,?)', [tit, wh, t])
                    conn.commit()
                #COMMENTS
                elif(act == "comment"):
                    print("Inserted action: " + act + " on title: " + tit)
                    c.execute('INSERT INTO comments VALUES (?,?,?)', [tit, wh, t])
                    conn.commit()
                #EDITS
                elif(act == "cedited"):
                    print("Inserted action: " + act + " on title: " + tit)
                    c.execute('INSERT INTO edits VALUES (?,?,?)', [tit, wh, t])
                    conn.commit()

    last[0] = int(data['events'][0]['ts'])
    last[1] = data['events'][0]['who']
    last[2] = data['events'][0]['type']
    last[3] = data['events'][0]['link']
def main():
    x = path.exists('articles.db')
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    #Create tables
    if(not x):
        c.execute('''CREATE TABLE articles
        (title varchar PRIMARY KEY, link varchar, who varchar, creation_time time)''')
        c.execute('''CREATE TABLE votes
        (title varchar, who varchar, action_time time, FOREIGN KEY (title) REFERENCES articles (title))''')
        c.execute('''CREATE TABLE problems
        (title varchar, who varchar, action_time time, FOREIGN KEY (title) REFERENCES articles (title))''')
        c.execute('''CREATE TABLE comments
        (title varchar, who varchar, action_time time, FOREIGN KEY (title) REFERENCES articles (title))''')
        c.execute('''CREATE TABLE edits
        (title varchar, who varchar, action_time time, FOREIGN KEY (title) REFERENCES articles (title))''')
        conn.commit()
    while(True):
        parse(c, conn)
    

main()
        


