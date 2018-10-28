from bottle import get, post, request, run
import json
import pdb

@post('/new')
def create():
    f = open('data.json', 'w')
    pdb.set_trace()
    json.dump(str(request.body), f)

def printKeys(obj):
        for key, value in obj.items():
                print(key)

def printValues(obj):
        for key, value in obj.items():
                print(value)

run(host='0.0.0.0', port=9000, debug=True)
