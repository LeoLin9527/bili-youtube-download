"""
@file:__init__.py
@time:2020/7/26-20:06
"""
from flask import Flask

from utils.bli_download import BiliBili

app = Flask(__name__)
bl_download = BiliBili()

from app.views import *
