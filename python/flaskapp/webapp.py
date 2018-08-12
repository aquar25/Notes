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
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
    


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)



