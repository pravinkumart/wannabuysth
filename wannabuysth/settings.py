# coding=utf8
__author__ = 'Alexander.Li'

DEBUG = True
LOCAL = True

TIMEOUT = 3600

if LOCAL:
    DB_URI = "postgresql+psycopg2://miaomi:1314520z@localhost/mobileapp"
else:
    DB_URI = "postgresql+psycopg2://miaomi:1314520z@125.65.46.33/mobileapp"

SECRET_KEY = "011556654433221changge!"


MEDIA_ROOT = "/static"

