# -*- coding: utf-8 -*-
"""
Copyright (c) [2019] [name of copyright holder]
   [navSystem] is licensed under the Mulan PSL v1.
   @author: ShanSan
   @email: yeshan1329441308@gmail.com
   @License: See the Mulan PSL v1 for more details.
"""


from flask import Flask, render_template, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
# from models import Navcard
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, current_user, login_user, LoginManager

from forms import NavcardForm, LoginForm
import click
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manage = LoginManager(app)


# ----------------------------------------------------------
# 前台
# 主页
@app.route('/')
def index():
    return render_template('frontend/index.html')

# 关于我
@app.route('/about')
def about():
    pass

# ----------------------------------------------------------
# 后台

# 
@app.route('/admin')
def admin():
    return render_template('backend/main.html')

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 已经登录
    if current_user.is_authenticated:
        print("已经登录过")
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        passwrod = form.password.data
        
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(passwrod):
                login_user(admin) # 验证成功，登入账户
                print('验证成功')
                return redirect(url_for('admin'))
            print("账号密码不正确")
        else:
            print("管理员不存在")    
    return render_template('backend/login.html', form=form)

# 测试
@app.route('/test')
def test():
    cards = Navcard.query.all()
    return render_template('frontend/card.html', cards=cards)

@app.route('/card/new', methods=['GET', 'POST'])
def new_card():
    # 新增卡片表单逻辑
    form = NavcardForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        image = form.thumnail.data
        navcard = Navcard(name=name, url=url, image=image)
        db.session.add(navcard)
        db.session.commit()
        print("添加成功")
        return redirect(url_for('index'))
    return render_template('backend/new_card.html', form=form)

# 卡片管理
@app.route('/card/manage')
def manage_card():
    cards = Navcard.query.all()
    return render_template('backend/manage_card.html', cards=cards)

# 删除卡片
@app.route('/card/<int:card_id>/delete', methods=['POST'])
def delete_card(card_id):
    card = Navcard.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('manage_card'))

# 卡片编辑
@app.route('/card/<int:card_id>/edit', methods=['POST', 'GET'])
def edit_card(card_id):
    form = NavcardForm()
    # 获取卡片对应id
    card = Navcard.query.get_or_404(card_id)
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        image = form.thumnail.data
        navcard = Navcard(name=name, url=url, image=image)
        db.session.add(navcard)
        db.session.commit()
        print("添加成功")
        return redirect(url_for('manage_card'))
    form.name.data = card.name
    form.url.data = card.url
    form.thumnail.data = card.image
    return render_template('/backend/edit_card.html', form=form)

# ---------------------------------------------------------------
# 生成测试数据
@app.cli.command()
def generate():
    db.drop_all()
    db.create_all()
    test_name = "大美中国"
    test_url = "https://shan333.cn"
    test_image = "https://cdn.jsdelivr.net/gh/ssmath/mypic/img/20190919131205.jpg"
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

# 创建管理用户
@app.cli.command()
def initadmin():
    db.drop_all()
    db.create_all()
    admin = Admin(username = "admin")
    admin.set_password("helloworld")
    db.session.add(admin)
    db.session.commit()
    print("创建用户成功")


# -------------------------------------------------------------------
# 数据库模型
# 导航卡片
class Navcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(200))  # 网站名
    url = db.Column(db.String(255))  # 网站地址
    image = db.Column(db.String(200))  # 网站缩略图地址


# UserMixin表示通过认证的用户
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # 对密码进行hash编码
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# ----------------------------------------------------------
# current.user的使用需要定义一个load函数
@login_manage.user_loader
def load_user(user_id):
    user = Admin.query.get(int(user_id))
    return user