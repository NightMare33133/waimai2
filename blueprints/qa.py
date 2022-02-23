from flask import Blueprint,render_template,g,request,redirect,url_for,flash
from decorators import login_required
from .forms import QuestionForm,AnswerForm,WaiMaiForm
from models import CommentModel,AnswerModel,UserModel,XiaDan
from exts import db
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import config
import os
from datetime import datetime



bp = Blueprint("qa",__name__,url_prefix="/")


@bp.route("/")
@login_required
def index():
    comments = CommentModel.query.order_by(db.text('-create_time')).all()
    return render_template("index.html",comments=comments)


@bp.route("/restaurant")
@login_required
def restaurant():
    #判断登录

    return render_template("restaurant.html")


@bp.route("/user_homepage")
@login_required
def user_homepage():
    #判断登录

    return render_template("user_homepage.html")


@bp.route("/rider")
@login_required
def rider():
    #判断登录
    user = g.user
    money = user.money
    waimai = XiaDan.query.order_by(db.text('-create_time')).all()
    return render_template("rider.html",waimai=waimai,money=money)


@bp.route("/admin")
@login_required
def admin():
    #判断登录
    user = UserModel.query.order_by(db.text('-join_time')).all()
    waimai = XiaDan.query.order_by(db.text('-create_time')).all()
    comments = CommentModel.query.all()
    answer = AnswerModel.query.all()
    return render_template("admin.html",user=user,waimai=waimai,comments=comments,answer=answer)


@bp.route("/restaurant",methods=['GET','POST'])
@login_required
def comment():
    #判断登录
    if request.method == 'GET':
        return render_template("restaurant.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
        else:
            flash("标题或内容格式错误！")
            return redirect(url_for("qa.restaurant"))

        icon = request.files.get('icon')
        ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)
            file_path = os.path.join(config.UPLOAD_ICON_DIR, icon_name)
            # print(file_path)
            icon.save(file_path)
            path = '/upload/icon/'
            icon2 = os.path.join(path, icon_name)
        question = CommentModel(title=title, content=content, author=g.user, icon=icon2)
        db.session.add(question)
        db.session.commit()
        return redirect("/")


@bp.route("/comment/<int:comment_id>")
def comment_detail(comment_id):
    comment = CommentModel.query.get(comment_id)
    return render_template("detail.html",comment=comment)

@bp.route("/answer/<int:comment_id>",methods=['POST'])
def answer(comment_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content, author=g.user, comment_id=comment_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("qa.comment_detail", comment_id=comment_id))
    else:
        flash("表单验证失败！")
        return redirect(url_for("qa.comment_detail", comment_id=comment_id))

@bp.route("/search")
def search():
    q = request.args.get('q')
    comments = CommentModel.query.filter(or_(CommentModel.title.contains(q),CommentModel.content.contains(q)))
    return render_template("index.html",comments=comments)


@bp.route('/user/<username>')
@login_required
def user():

    return render_template('user_homepage.html')

@bp.route('/order',methods=["GET",'POST'])
@login_required
def order():
    if request.method == 'POST':

        return render_template('order.html')
    else:
        return render_template('/')

@bp.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = CommentModel.query.get(comment_id)
    if comment:
        try:
            db.session.delete(comment)
            db.session.commit()
        except Exception as e:

            flash("删除评论出错")
            db.session.rollback()
    else:
        flash("评论找不到")
    return redirect(url_for('qa.index'))

#用户信息修改
@bp.route('/change',methods=['GET','POST'])
@login_required
def user_change():
    if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            icon = request.files.get('icon')
            # print(icon)
            ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']
            icon_name = icon.filename
            suffix = icon_name.rsplit('.')[-1]

            if suffix in ALLOWED_EXTENSIONS:
                icon_name = secure_filename(icon_name)
                file_path = os.path.join(config.UPLOAD_ICON_DIR,icon_name)
                print(file_path)
                icon.save(file_path)
                user = g.user
                path = '/upload/icon/'
                user.icon = os.path.join(path,icon_name)
                db.session.commit()
                return redirect(url_for('qa.user_homepage'))
            else:
                render_template('user_homepage.html', user=g.user,msg='必须是jpg,png,gif,bmp格式的文件')
            user = g.user
            user.username = username
            user.password = password
            user.email = email
            db.session.commit()

            # users = UserModel.query.all()
            # for user1 in users:
            #     if user1.email == email:
            #         return render_template('user_homepage.html',user=g.user,msg='此邮箱已被注册')




    return render_template('user_homepage.html',user=g.user)


@bp.route("/send", methods=['GET','POST'])
@login_required
def send():
    if request.method == "GET":
        return render_template("order.html")
    else:
        form = WaiMaiForm(request.form)
        dish = form.dish.data
        delivery_address = form.address.data
        telephone_number = form.telephone.data

        waimai = XiaDan(delivery_address=delivery_address,telephone_number=telephone_number,dish=dish)
        db.session.add(waimai)
        db.session.commit()
        return redirect(url_for("qa.index"))

@bp.route("/take_orders/<int:dish_id>", methods=['GET','POST'])
@login_required
def take_orders(dish_id):
    if request.method == "GET":
        return render_template("rider.html")
    else:
        results = XiaDan.query.all()
        # state = 1
        # arrival_time = datetime.now()
        # dish.state = state
        # dish.arrival_time = arrival_time

        results[dish_id-1].arrival_time = datetime.now()
        results[dish_id-1].state = 1
        user = g.user
        money = user.money
        user.money = money+10
        db.session.commit()
        return redirect(url_for("qa.rider"))

@bp.route('/delete_dish/<int:dish_id>')
@login_required
def delete_dish(dish_id):
    dish =XiaDan.query.get(dish_id)
    if comment:
        try:
            db.session.delete(dish)
            db.session.commit()
        except Exception as e:

            flash("删除评论出错")
            db.session.rollback()
    else:
        flash("评论找不到")
    return redirect(url_for('qa.admin'))