# -*- coding: utf-8 -*-
from flask import Flask, render_template
# from models import Navcard
from flask_sqlalchemy import SQLAlchemy
import click


app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)

# 主页
@app.route('/')
def index():
    return render_template('frontend/index.html')

# 关于我
@app.route('/about')
def about():
    pass

# 登录
@app.route('/login')
def login():
    pass

@app.route('/admin')
def admin():
    return render_template('backend/main.html')

@app.route('/test')
def test():
    cards = Navcard.query.all()
    return render_template('frontend/card.html', cards=cards)



# ---------------------------------------------------------------
@app.cli.command()
def generate():
    db.drop_all()
    db.create_all()
    test_name = "磨削和"
    test_url = "https://shan333.cn"
    test_image = "China.jpg"
    for _ in range(5):
        navcard_new = Navcard(name = test_name, url = test_url, image = test_image)
        db.session.add(navcard_new)
    db.session.commit()
    click.echo("数据生成完毕！")

# 先建立表
@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database.')


# 导航卡片
class Navcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(200))  # 网站名
    url = db.Column(db.String(255))  # 网站地址
    image = db.Column(db.String(200))  # 网站缩略图地址