import sys
import json
import os


path = os.path.join(os.environ['HOME'], "task.json")
l = []

def load():
    global l
    l = json.load(open(path))

def save():
    global l
    try:
        json.dump(l, open(path,"w"))
    except:
        print("Failed to write file")
        exit(1)

def show():
    global l
    print ("id | Note")
    for element in l:
        print(str(element[0]), ' | ', element[1])

def add(*args):
    global l
    print (*args)
    id = len(l) + 1
    text = " ".join(*args)
    l.append([id, text])

def rem(id):
    global l
    for element in l:
        if element[0] == id:
            l.remove(element)

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
    save()
    return 0

if __name__ == "__main__":
    exit (main())
