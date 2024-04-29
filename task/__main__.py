import sys
import json
import os
import time
import random
import webdav
from datetime import datetime


path = os.path.join(os.environ['HOME'], ".task.json")
config = f"{os.environ["HOME"]}/.task.cfg"
l = []

def load():
    global l
    l = json.load(open(path))

def save():
    global l
    l.sort(key=lambda x: x[1])
    try:
        json.dump(l, open(path,"w"))
    except:
        print("Failed to write file")
        exit(1)

def search_id(id):
    global l
    token = 0
    for element in l:
        if element[0] == id:
            token = element
            break
    return token

def show():
    def parse(num):
        if num < 10:
            return "  " + str(num)
        elif num < 100:
            return " " + str(num)
        else:
            return str(num)

    global l
    extra = sys.argv[2:]
    print ("  #  |    id   | Note")
    count = 1
    for element in l:
        if 'done' in extra or 'all' in extra:
            print(parse(count), ' | ', element[0], '|', element[-1])
            count += 1
        else:
            if 'undone' == element[2]:
                print(parse(count), ' | ', element[0], '|',  element[-1])
                count += 1

def add(*args):
    global l
    id = random.randint(100000,999999)
    timestamp = 0
    arg_list = args[0]
    args_list = args[0]
    for arg in arg_list:
        if "--time=" in arg or "-t=" in arg:
            st = arg.replace("--time=", "")
            timestamp = int(os.popen(f"date --date='{st}' +%s").read())
            args_list.remove(arg)
    if timestamp == 0:
        timestamp = time.time()
    text = " ".join(args_list)
    status = 'undone'
    l.append([id, timestamp, status, text])

def rem(id):
    global l
    element = search_id(id)
    l.remove(element)

def done(id):
    global l
    position = l.index(search_id(id))
    l[position][2] = 'done'

def sync():
    global l, config
    wv = object
    if os.path.exists(config):
        wv = webdav.Webdav.parse(config)
    else:
        print("Error please configure", config)
        print('{"ssl": true, "username": "example_username", "password": "example_passwd", "hostname": "example.domain.com", "port": 1234}', end="", file=open(config, "w"))
        return 1
    if len(sys.argv) == 3 and sys.argv[2] in ["force", "-f"]:
        pass
    else:
        response = wv.get(".task.json")
        cloud = json.loads(response)
        l_list = []
        for i in l:
            l_list.append(i[0])
        for i in cloud:
            if not i[0] in l_list:
                l.append(i)
    wv.put(path)
    return 0

def agenda():
    def parse_missed(element_list):
        for element in element_list:
            t = element[1]
            tt = time.time()
            text = element[-1]
            id = element[0]
            token = (tt - t) // (3600 * 24)
            if not token > 1:
                token = str((tt - t) // (3600)) + "h"
            else:
                token = str(token) + "d"
            yield f"[{id}] {token} {text}"

    def parse_today(element_list):
        for element in element_list:
            text = element[-1]
            id = element[0]
            yield f"[{id}] {text}"

    def parse_week(element_list):
        for element in element_list:
            t = element[1]
            text = element[-1]
            id = element[0]
            token = datetime.fromtimestamp(t)
            yield f"[{id}] {token.strftime('%d/%m')} {text}"

    global l
    token = l
    token.sort(key=lambda x: x[1])
    start = datetime.now()
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(hour=23, minute=59, second=59, microsecond=0)
    week = time.time() + (3600 * 24 * 7)
    month = week + (3600 * 24 * 7 * 4)
    missed = []
    today = []
    within_next_week = []
    within_next_month = []
    for element in token:
        if element[1] < start.timestamp() and element[-2] == "undone":
            missed.append(element)
        elif element[1] >= start.timestamp() and element[1] <= end.timestamp() and element[-2] == "undone":
            today.append(element)
        elif element[1] > end.timestamp() and element[1] <= week and element[-2] == "undone":
            within_next_week.append(element)
        elif element[1] > week and element[1] <= month and element[-2] == "undone":
            within_next_month.append(element)
        else:
            pass
    if len(missed) != 0:
        print("Missed")
        print("\n".join(parse_missed(missed)))
    if len(today) != 0:
        print("Today", datetime.now().strftime("%d/%m"))
        print("\n".join(parse_today(today)))
    if len(within_next_week) != 0:
        print("Next Week")
        print("\n".join(parse_week(within_next_week)))
    if len(within_next_month) != 0:
        print("Next Month")
        print("\n".join(parse_week(within_next_month)))
    return 0

def main():
    load()
    if len(sys.argv) < 2:
        show()
        return 1
    elif sys.argv[1] == "show":
        show()
    elif sys.argv[1] == "add":
        add(sys.argv[2:])
    elif sys.argv[1] in ["del", "rem"]:
        rem(int(sys.argv[2]))
    elif sys.argv[1] == "done":
        done(int(sys.argv[2]))
    elif sys.argv[1] == "sync":
        sync()
    elif sys.argv[1] == "agenda":
        agenda()
    save()
    return 0

if __name__ == "__main__":
    exit (main())
