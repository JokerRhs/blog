import json
import math
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from back.models import Article, Category

web_blue = Blueprint('web_blue', __name__)

@web_blue.route('/', methods=['GET'])
def index():

    return render_template('/web/index.html')


@web_blue.route('/blog/', methods=['GET'])
def blog():
    page = 1
    return redirect(url_for('web_blue.sec_blog', page=page))



@web_blue.route('/blog/<int:page>/', methods=['GET'])
def sec_blog(page):
    if request.method == 'GET':
        art = Article.query.filter().order_by(-Article.art_time).offset((page-1)*6).limit(6).all()
        cate = Category.query.filter().all()
        count = Article.query.filter().count()
        page_sum = math.ceil(count/6)
        return render_template('/web/blog.html', art=art, cate=cate, page_sum=page_sum)


@web_blue.route('/single/', methods=['GET'])
def single():
    art = Article.query.filter().order_by(-Article.art_time).first()
    # id = art.art_id
    if not art:
        return redirect(url_for('web_blue.blog'))
    id = art.art_id
    return redirect(url_for('web_blue.single_post', id=id))


@web_blue.route('/single/<int:id>/', methods=['GET'])
def single_post(id):
    if request.method == 'GET':
        art = Article.query.filter(Article.art_id == id).first()
        return render_template('/web/single-post.html', art=art)





