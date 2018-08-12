#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, escape, session
from flask import copy_current_request_context
from threading import Thread
from time import sleep
from flask import abort

import sqlite3

app = Flask(__name__)

@app.route('/bad')
def bad_handle():
    abort(404)

@app.route('/love/<name>')
def love_handle(name):
    return '<h1>Robot love %s !</h1>' % name, 400

@app.route('/')
def home():    
    #return render_template('result.html', the_title='Your Future is here', result=result)
    return "index"

@app.route('/list')
def show_list():
    srcs = ['a', 'b', 'c', 'd']
    return render_template('result.html', the_title='Your Future is here', comments=srcs, vsrc='../static/files/Structure Basics - Making Things Look 3D-en.mp4')

@app.route('/play')
def play_video():
    return render_template('player.html', the_title='Your Future is here', 
        vsrc='../static/files/Structure Basics - Making Things Look 3D-en.mp4')

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)



