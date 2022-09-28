"""
for now do nothing
"""
import json
import sys
import os


sys.path.append(__file__[:-11])

#if not config file detected, create it
path = os.path.join(os.environ['HOME'],  ".task.json" )
try:
    json.load(open(path))
except:
    json.dump ([], open(path, 'w'))
