import sys
import json
import os
import time
import random


path = os.path.join(os.environ['HOME'], ".task.json")
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
    timestamp = time.time()
    text = " ".join(*args)
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
    save()
    return 0

if __name__ == "__main__":
    exit (main())
