import json

env = {}
with open('config.json') as f:
    env = json.load(f)
