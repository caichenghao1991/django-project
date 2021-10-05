import json
with open('data.json') as f:
    dic = json.load(f)
    print(dic['age'])