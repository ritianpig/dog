from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
import os
import json

app = Flask(__name__)
db = SQLAlchemy()

migrate = Migrate()
migrate.init_app(app, db)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    article_name = db.Column(db.String(200))
    appid = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    column_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    main_events = db.Column(db.Text)
    countcollect = db.Column(db.Integer)
    countlike = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    imageNum = db.Column(db.Integer)
    is_audit = db.Column(db.Integer)
    is_collect = db.Column(db.Integer)
    is_like = db.Column(db.Integer)
    url = db.Column(db.String(200))


class Webchat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    webchat = db.Column(db.String(200))
    conduct = db.Column(db.String(200))
    color = db.Column(db.String(50))


class Show1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_str = db.Column(db.String(200))


class Show6(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_str1 = db.Column(db.String(200))
    show_str2 = db.Column(db.String(200))
    show_str3 = db.Column(db.String(200))
    show_str4 = db.Column(db.String(200))
    show_str5 = db.Column(db.String(200))
    show_str6 = db.Column(db.String(200))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200))
    user_name = db.Column(db.String(100))


class UserLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200))
    article_id = db.Column(db.Integer)


class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200))
    article_id = db.Column(db.Integer)


class Ad1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic_url = db.Column(db.String(200))
    ad_str = db.Column(db.String(200))


class Ad2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic_url = db.Column(db.String(200))
    head_url = db.Column(db.String(200))
    name = db.Column(db.String(20))
    Wx = db.Column(db.String(100))
    content = db.Column(db.TEXT)


class Article_view(ModelView):
    form_columns = ('article_id', 'article_name', 'content',
                    'main_events', 'create_date', 'countcollect',
                    'countlike')
    column_list = ('article_id', 'article_name', 'create_date',
                   'countcollect', 'countlike')
    column_labels = dict(
        article_id=u'文章ID',
        article_name=u'文章名',
        content=u'文章内容',
        main_events=u'注意事项',
        create_date=u'文章创建日期',
        countcollect=u'文章浏览数',
        countlike=u'文章收藏数'
    )
    create_modal = True
    edit_modal = True
    can_export = True


admin = Admin(name='Admin', endpoint='admin')
file_path = os.path.join(os.path.dirname(__file__), 'static')
# admin.add_view(Userview(Sdk,db.session,name='sdk_f'))
admin.add_view(FileAdmin(file_path, '/static/', name='upload'))
admin.add_view(Article_view(Article, db.session, name='article'))
admin.add_view(ModelView(Webchat, db.session, name='webchat'))
admin.add_view(ModelView(Show1, db.session, name='搜索推荐'))
admin.add_view(ModelView(Show6, db.session, name='首页6推荐位'))
admin.add_view(ModelView(Ad1, db.session, name='Ad1'))
admin.add_view(ModelView(Ad2, db.session, name='Ad2'))

app.config.from_object('config')
db.init_app(app)
db.create_all(app=app)
admin.init_app(app)
app.secret_key = 'qw123098'
app.config['JSON_AS_ASCII'] = False


# 返回文章数据(已测试)
@app.route('/dog', methods=["GET", "POST"])
def dog():
    if request.method == "GET":
        get_id = request.args.get('article_id')
        get_user_id = request.args.get('user_id')
        pic_head = str(get_id) + '_'
        path_dir = os.listdir(os.path.join(os.path.dirname(__file__), 'static'))
        get_data = db.session.query(Article).filter_by(article_id=
                                                       get_id).first()
        get_user_like = db.session.query(UserLike).filter_by\
            (user_id=get_user_id, article_id=get_id).first()

        add_user_history = UserHistory(user_id=get_user_id, article_id=get_id)
        db.session.add(add_user_history)
        db.session.commit()

        add_countcollect = db.session.query(Article).filter_by\
            (article_id=get_id).first()
        if add_countcollect.countcollect:
            add_countcollect.countcollect += 1
        else:
            add_countcollect.countcollect = 1
        db.session.commit()

        contentPictures = []
        pic_list = []
        if get_data:
            for k in path_dir:
                header = os.path.splitext(k)[0]
                if pic_head in header:
                    pic_list.append(k)
            for index,i in enumerate(pic_list):
                name = os.path.splitext(i)
                picture_name = get_id + '_' + str(index+1) + name[1]
                pic_dict = {
                    'article_id': get_id,
                    'column_id': get_data.column_id,
                    'count_like': get_data.countlike,
                    'create_date': str(get_data.create_date),
                    'create_idate': int(str(get_data.create_date.date()
                                            ).replace('-', '')),
                    'isaudit': 1,
                    'order': 1,
                    'picture_id': get_id,
                    'picture_name': picture_name,
                    'title': picture_name,
                    'url': "https://xcx.51babyapp.com/dog/static/"
                           + picture_name
                }

                contentPictures.append(pic_dict)

            if get_user_like:
                is_like = "1"
            else:
                is_like = "0"
            article = {
                'appid': get_data.appid,
                'article_id': get_data.article_id,
                'article_name': get_data.article_name,
                'class_id': get_data.class_id,
                'column_id': get_data.column_id,
                'content': get_data.content,
                'main_events': get_data.main_events,
                'countcollect': get_data.countcollect,
                'countlike': get_data.countlike,
                'create_date': str(get_data.create_date),
                'create_idate': int(str(get_data.create_date.date()
                                        ).replace('-', '')),
                'imageNum': get_data.imageNum,
                'is_audit': get_data.is_audit,
                'is_collect': get_data.is_collect,
                'is_like': is_like,
                'url': get_data.url
            }
            result = {'article': article, 'contentPictures': contentPictures}
            return jsonify(result)
        else:
            return 'article_id错误'


@app.route('/webchat', methods=["GET", "POST"])
def wb():
    if request.method == "GET":
        get_data = db.session.query(Webchat).first()

        if get_data:
            result = {'webchat': get_data.webchat,
                      'conduct': get_data.conduct,
                      'color': get_data.color}
        else:
            result = {}
        return jsonify(result)
    else:
        return '不支持post请求'


@app.route('/search1', methods=["GET", "POST"])
def search1():
    if request.method == "GET":
        get_str = request.args.get('str')
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).filter(
            Article.article_name != '').all()
        search1_list = []
        for data in res_datas:
            if get_str in data.content:
                search1_list.append(data)

        search1_tuple = tuple(search1_list)
        index1 = int(get_page)*6
        index2 = (int(get_page)+1)*6
        article_list = []
        object_list = list(search1_tuple[index1:index2])
        for i in object_list:
            try:
                picture_url = str(i.article_id) + '_1' + os.path.splitext(
                    json.loads(i.url)[0])[1]
            except:
                picture_url = ""
            res__article_object = {
                "article_id": i.article_id,
                "article_name": i.article_name,
                "content": i.content,
                "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                picture_url,
                "liulancount": i.countcollect,
                "shoucangcount": i.countlike
            }
            article_list.append(res__article_object)

        search1_result = {
            "articlelist": article_list
        }
        return jsonify(search1_result)

    else:
        return '不支持POST请求'


# 首页
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).order_by(Article.id.desc()).all()
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        index_object_list = res_datas[index1:index2]

        index_list = []

        for i in index_object_list:

            try:
                picture_url = str(i.article_id) + '_1' + os.path.splitext(
                    json.loads(i.url)[0])[1]
            except:
                picture_url = ""
            res_index_object = {
                "article_id": i.article_id,
                "article_name": i.article_name,
                "content": i.content,
                "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                picture_url,
                "liulancount": i.countcollect,
                "shoucangcount": i.countlike,
                "create_date": str(i.create_date)
            }
            index_list.append(res_index_object)

        index_result = {
            "articlelist": index_list
        }
        return jsonify(index_result)

    else:
        return '不支持POST请求'


# 首页推荐搜索词
@app.route('/show1', methods=["GET", "POST"])
def show1():
    if request.method == "GET":
        res_data = db.session.query(Show1).first()
        if res_data:
            result = {
                "showStr": res_data.search_str
            }
        else:
            result = {}

        return jsonify(result)

    else:
        return '不支持POST请求'


# 首页6个推荐位（已测试）
@app.route('/show6', methods=["GET", "POST"])
def show6():
    if request.method == "GET":
        res_data = db.session.query(Show6).first()

        article_list = []
        if res_data:
            res_show_list = [res_data.show_str1, res_data.show_str2,
                             res_data.show_str3, res_data.show_str4,
                             res_data.show_str5, res_data.show_str6]
            for i in res_show_list:
                res_article_data = db.session.query(Article)\
                    .filter_by(article_name=i).first()
                if res_article_data:
                    article_dict = {
                        "article_id": res_article_data.article_id,
                        "article_name": res_article_data.article_name
                    }
                else:
                    article_dict = {}
                article_list.append(article_dict)
            result = {"articlelist": article_list}

        else:
            result = {}
        return jsonify(result)

    else:
        return '不支持POST请求'


# 首页4个推荐位(已测试)
@app.route('/show4', methods=["GET", "POST"])
def show4():
    if request.method == "GET":
        res_datas = db.session.query(Article).order_by(
            Article.countcollect.desc()).limit(4).all()
        article_list = []
        for i in res_datas:
            article_dict = {
                "article_id": i.article_id,
                "article_name": i.article_name
            }
            article_list.append(article_dict)

        result = {"articlelist": article_list}
        return jsonify(result)

    else:
        return '不支持POST请求'


# 用户收藏(已测试)
@app.route('/like', methods=["GET", "POST"])
def like():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        get_article_id = request.args.get('article_id')
        res_data = db.session.query(UserLike).filter_by(
            user_id=get_user_id,article_id=get_article_id).first()
        if res_data:
            return '该文章已经被收藏了!!!'
        else:
            add_like = UserLike(user_id=get_user_id, article_id=get_article_id)
            db.session.add(add_like)
            db.session.commit()

            res_artictl = db.session.query(Article).filter_by(
                article_id=get_article_id).first()
            if res_artictl.countlike:
                res_artictl.countlike += 1
            else:
                res_artictl.countlike = 1
            db.session.commit()
        return 'ok'

    else:
        return '不支持POST请求'


# 用户取消收藏（已测试）
@app.route('/unlike', methods=["GET", "POST"])
def unlike():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        get_article_id = request.args.get('article_id')
        res_data = db.session.query(UserLike).filter_by(
            user_id=get_user_id, article_id=get_article_id).first()
        if res_data:
            db.session.delete(res_data)
            db.session.commit()
            return '取消收藏成功'

        else:
            return '该文章还未收藏'

    else:
        return '不支持POST请求'


# 返回用户历史列表(已测试)
@app.route('/history', methods=["GET", "POST"])
def history():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        get_page = request.args.get('page')
        res_history = db.session.query(UserHistory).filter_by(
            user_id=get_user_id).order_by(UserHistory.id.desc()).all()
        article_id_list = []
        if res_history:
            for i in res_history:
                article_id_list.append(i.article_id)
            history_list = []
            for k in article_id_list:

                res_article = db.session.query(Article).filter_by(article_id=k)\
                    .first()
                try:
                    picture_url = str(k)+'_1'+os.path.splitext(
                        json.loads(res_article.url)[0])[1]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": res_article.article_id,
                    "article_name": res_article.article_name,
                    "content": res_article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                    picture_url,
                    "liulancount": res_article.countcollect,
                    "shoucangcount": res_article.countlike
                }
                history_list.append(article_dict)

            index1 = int(get_page) * 6
            index2 = (int(get_page) + 1) * 6
            result_list = history_list[index1:index2]
            result = {"articlelist": result_list}
        else:
            result = {}

        return jsonify(result)

    else:
        return '不支持POST请求'


# 返回用户收藏列表（已测试）
@app.route('/like_list', methods=["GET", "POST"])
def like_list():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        get_page = request.args.get('page')
        res_like = db.session.query(UserLike).filter_by(
            user_id=get_user_id).order_by(UserLike.id.desc()).all()
        article_id_list = []
        if res_like:
            for i in res_like:
                article_id_list.append(i.article_id)
            like_list = []
            for k in article_id_list:
                res_article = db.session.query(Article).filter_by(article_id=k)\
                    .first()
                try:
                    picture_url = str(k)+'_1'+os.path.splitext(
                        json.loads(res_article.url)[0])[1]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": res_article.article_id,
                    "article_name": res_article.article_name,
                    "content": res_article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                    picture_url,
                    "liulancount": res_article.countcollect,
                    "shoucangcount": res_article.countlike
                }
                like_list.append(article_dict)

            index1 = int(get_page) * 6
            index2 = (int(get_page) + 1) * 6
            result_list = like_list[index1:index2]
            result = {"articlelist": result_list}

        else:
            result = {}

        return jsonify(result)

    else:
        return '不支持POST请求'


# 返回用户收藏和浏览历史数
@app.route('/UserData', methods=["GET", "POST"])
def userdata():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        res_like = db.session.query(UserLike).filter_by(
            user_id=get_user_id).all()

        res_history = db.session.query(UserHistory).filter_by\
            (user_id=get_user_id).all()
        result = {
            "likes": str(len(res_like)),
            "histories": str(len(res_history))
        }

        return jsonify(result)

    else:
        return '不支持POST请求'


@app.route('/picture', methods=["GET", "POST"])
def picture():
    if request.method == "GET":
        path_dir = os.listdir(os.path.join(os.path.dirname(__file__), 'static'))
        res_articles = db.session.query(Article).all()
        article_ids = []
        for article in res_articles:
            article_ids.append(article.article_id)

        for id in article_ids:
            urls = []
            for k in path_dir:

                header = os.path.splitext(k)[0]
                if str(id) in header:
                    urls.append(k)
                    print(urls)
                    res_article = db.session.query(Article).filter_by \
                        (article_id=id).first()
                    res_article.url = json.dumps(urls)
                    db.session.commit()
                else:
                    pass

        return 'ok'


@app.route('/ad1', methods=["GET", "POST"])
def ad1():
    if request.method == "GET":
        res_ad1 = db.session.query(Ad1).first()
        if res_ad1:
            result = {
                "pictures_url": res_ad1.pic_url,
                "ad1": res_ad1.ad_str
            }
        else:
            result = {}

        return jsonify(result)

    else:
        return '不支持POST请求'


@app.route('/ad2', methods=["GET", "POST"])
def ad2():
    if request.method == "GET":
        res_ad2 = db.session.query(Ad2).first()
        if res_ad2:
            result = {
                "pictures_url": res_ad2.pic_url,
                "head_url": res_ad2.head_url,
                "name": res_ad2.name,
                "Wx": res_ad2.Wx,
                "content": res_ad2.content
            }
        else:
            result ={}

        return jsonify(result)

    else:
        return '不支持POST请求'


if __name__ == '__main__':
    app.run(threaded=True)


