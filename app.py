from flask import Flask, render_template

app = Flask(__name__)

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 关于我
@app.route('/about')
def about():
    pass

# 登录
@app.route('/login')
def login():
    pass

@app.route('/test')
def test():
    return render_template('card.html')

