import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('%s/%s' % (dir_path, 'models'))
from model import *
from bottle import get, post, request, run, static_file, redirect
import json
import pdb

@get('/new')
def new():
    return static_file('create.html', root=dir_path)

@post('/new')
def create():
    record = Record()
    record.parse_json(request.params.dict)
    uuid = record.new_id()
    record.save()
    redirect('/record/%s' % uuid)

@post('/record/<uuid>')
def show(uuid):
    record = Record()
    return record.load(uuid)

@get('/record/<uuid>')
def show(uuid):
    record = Record()
    record.load(uuid)
    return static_file('index.html', dir_path)

@post('/record/<uuid>/readings')
def reading(uuid):
    record = Record()
    return record.load(uuid)

@get('/record/<uuid>/readings')
def reading(uuid):
    record = Record()
    record.load(uuid)
    return {'readings': record.get_readings()}

@get('/js/<filename>')
def js(filename):
    return static_file(filename, root='%s/%s' % (dir_path, 'js'))

@get('/css/<filename>')
def css(filename):
    return static_file(filename, root='%s/%s' %(dir_path, 'css'))

@get('/<filename>')
def html(filename):
    return static_file('%s.html' % filename, root=dir_path)

@get('/test')
def index():
    return static_file('index.html', root=dir_path)

run(host='0.0.0.0', port=80, debug=False)
