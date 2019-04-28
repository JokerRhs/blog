import math
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for, session

from back.function import login_required
from back.models import User, db, Category, Article

back_blue = Blueprint('back_blue', __name__)


@back_blue.route('/f_t/', methods=['GET', 'POST'])
def add_tab():
    db.create_all()
    return '创建表成功'


@back_blue.route('/d_t/', methods=['GET', 'POST'])
def del_tab():
    db.drop_all()
    return '删除表成功'


@back_blue.route('/reg_zc/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = request.form.get('admin')
        time = datetime.now()
        if username and password:
            try:
                user = User()
                user.save_update(username, password, admin, time)
                return redirect(url_for('back_blue.login'))
            except:

                return render_template('back/register.html', error='用户名已存在')
        else:
            return render_template('back/register.html', error='用户名和密码不能为空')


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method == 'POST':
        us_num = request.form.get('us_num')
        password = request.form.get('password')
        user = User.query.filter(User.us_num == us_num).first()
        if user and user.password == password:
            session['username'] = user.username

            return redirect(url_for('back_blue.index', admin=user.username))

        else:
            return render_template('back/login.html', error='用户名和密码错误')


@back_blue.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        username = session['username']
        return render_template('back/index.html', admin=username)


@back_blue.route('/article/', methods=['GET', 'POST'])
@login_required
def article():
    if request.method == 'GET':
        page = 1
        return redirect(url_for('back_blue.sec_article', page=page))


@back_blue.route('/article/<int:page>/', methods=['GET', 'POST'])
@login_required
def sec_article(page):
    if request.method == 'GET':
        username = session['username']
        count = Article.query.count()
        content = Article.query.filter().order_by(-Article.art_time).offset((page - 1) * 6).limit(6).all()
        page_sum = math.ceil(count / 6)
        return render_template('back/article.html', admin=username, content=content, count=count, page_sum=page_sum)


@back_blue.route('/add-article/', methods=['GET', 'POST'])
@login_required
def add_article():
    if request.method == 'GET':
        username = session['username']
        content = Category.query.all()
        return render_template('back/add-article.html', admin=username, content=content)

    if request.method == 'POST':
        title = request.form.get('title').encode()
        content = request.form.get('content')
        des = request.form.get('describe')
        tag = request.form.get('tags')
        category = request.form.get('category')
        vis = request.form.get('visibility')
        # pic = request.form.get('img')
        time = datetime.now()
        art = Article()
        art.save_update(title, content, des, tag, time, vis, category)
        return redirect(url_for('back_blue.article'))


@back_blue.route('/update-article/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_article(id):
    if request.method == 'GET':
        username = session['username']
        art = Article.query.filter_by(art_id=id).all()
        content = Category.query.all()
        return render_template('back/update-article.html', art=art, id=id, admin=username, content=content)

    if request.method == 'POST':
        title = request.form.get('title').encode()
        content = request.form.get('content')
        des = request.form.get('describe')
        tag = request.form.get('tags')
        category = request.form.get('category')
        vis = request.form.get('visibility')
        # pic = request.form.get('img')
        time = datetime.now()
        art = Article.query.filter_by(art_id=id).first()
        art.update(title, content, des, tag, time, vis, category)
        return redirect(url_for('back_blue.article'))


@back_blue.route('/del-article/<int:id>/', methods=['GET', 'POST'])
@login_required
def del_article(id):
    if request.method == 'GET':
        art = Article.query.filter_by(art_id=id).first()
        art.delete()
        return redirect(url_for('back_blue.article'))


@back_blue.route('/category/', methods=['GET', 'POST'])
@login_required
def category():
    if request.method == 'GET':
        content = Category.query.all()
        count = Category.query.count()
        username = session['username']
        return render_template('back/category.html', admin=username, content=content, count=count)
    if request.method == 'POST':
        name = request.form.get('name')
        sec_name = request.form.get('sec_name')
        des = request.form.get('describe')
        time = datetime.now()
        try:
            cate = Category()
            cate.save_update(name, sec_name, time, des)
            content = Category.query.all()
            return redirect(url_for('back_blue.category', content=content))
        except:
            return render_template('/back/category.html')


@back_blue.route('/update-category/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_category(id):
    if request.method == 'GET':
        username = session['username']
        cate = Category.query.filter_by(cate_id=id).first()
        return render_template('/back/update-category.html', admin=username, cate=cate, id=id)

    if request.method == 'POST':
        name = request.form.get('name')
        sec_name = request.form.get('sec_name')
        des = request.form.get('describe')
        try:
            cate = Category.query.filter_by(cate_id=id).first()
            cate.update(name, sec_name, des)
            db.session.commit()
            return redirect(url_for('back_blue.category'))
        except:
            return render_template('/back/category.html')


@back_blue.route('/del-category/<int:id>/', methods=['GET'])
@login_required
def del_category(id):
    if request.method == 'GET':
        cate = Category.query.filter_by(cate_id=id).first()
        cate.delete()
        return redirect(url_for('back_blue.category'))
