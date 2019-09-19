# -*- coding: utf-8 -*-

import os
import sys

# os.path.abspath(os.path.dirname(__file__))返回当前脚本文件的绝对路径 
basedir = os.path.abspath(os.path.dirname(__file__))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

SQLALCHEMY_DATABASE_URI= prefix + os.path.join(basedir, 'data-dev.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = os.getenv("SECRET_KEY", "secret string")