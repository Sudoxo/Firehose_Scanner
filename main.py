import urllib.request, json
import time

def int_to_time(x):
    return time.strftime('%H:%M:%S', time.gmtime(x+3600))

f = open("log.txt","w+", encoding = "utf-8")

with urllib.request.urlopen("https://www.meneame.net/backend/sneaker2") as url:
    data = json.loads(url.read().decode())

for e in data['events']:
    f.write("\n################\n")
    f.write("hora: " + int_to_time(int(e['ts'])) + "\n")
    f.write("SUB: " + e['sub_name']+ "\n")
    f.write("acción: " + e['type']+ "\n")
    f.write("me/co: " + e['votes'] + '/' + e['com'] + "\n")
    f.write("noticia: " + e['title']+ "\n")
    f.write("quién/qué: " + e['who']+ "\n")
    f.write("estado: " + e['status'])

