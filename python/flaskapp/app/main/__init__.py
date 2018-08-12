#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors