#coding=utf8
__author__ = 'alex'

import logging
from tempfile import NamedTemporaryFile
from flask import Blueprint, render_template, abort, g, request, redirect, url_for, session, flash, send_file
from utils import *

index = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')


@index.route("/help")
def help():
    return render_template("help.html", **locals())
