"""
for now do nothing
"""
import json
import sys
import os


sys.path.append(__file__[:-11])
if sys.platform == "win32":
    dir = "\\"
else:
    dir = "/"

try:
    json.load(open(os.environ['HOME'] + dir + "task.json"))
except:
    json.dump ([], open(os.environ['HOME'] + dir + "task.json", "w"))