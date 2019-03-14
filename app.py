from flask import Flask, request, jsonify
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
import os
import json
import random

app = Flask(__name__)
db = SQLAlchemy()
app.config['UPLOADED_PATH'] = os.getcwd() + '/upload'

migrate = Migrate()
migrate.init_app(app, db)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    article_name = db.Column(db.String(200))
    way = db.Column(db.String(10))
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
    url = db.Column(db.String(500))
    column_name = db.Column(db.String(255), default='')
    class_name = db.Column(db.String(255), default='')
    bigclass_name = db.Column(db.String(255), default='')


class Webchat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    float_id = db.Column(db.Integer)
    webchat = db.Column(db.String(200))
    conduct = db.Column(db.String(200))
    color = db.Column(db.String(50))


class Expert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expertName = db.Column(db.String(50))
    like = db.Column(db.String(200))
    content = db.Column(db.String(500))
    headrUrl = db.Column(db.String(255))
    consultNum = db.Column(db.String(20))

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


class User_dg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    use_id = db.Column(db.String(200))
    isHaveDog = db.Column(db.String(10))
    dogType = db.Column(db.String(50))
    dogSex = db.Column(db.String(10))
    dog_Age = db.Column(db.String(10))


class User_question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200))
    questions = db.Column(db.TEXT)


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
    remark = db.Column(db.String(200))


class Article_view(ModelView):
    form_columns = ('article_id', 'article_name', 'content','main_events',
                    'create_date', 'countcollect', 'countlike', 'column_name',
                    'bigclass_name', 'class_name', 'way')
    column_list = ('article_id', 'article_name', 'content', 'main_events',
                   'create_date', 'countcollect', 'countlike', 'column_name',
                   'bigclass_name', 'class_name', 'way'
                   )
    column_labels = dict(
        article_id=u'文章ID',
        article_name=u'文章名',
        content=u'文章内容',
        main_events=u'注意事项',
        create_date=u'文章创建日期',
        countcollect=u'文章浏览数',
        countlike=u'文章收藏数',
        column_name=u'栏目',
        bigclass_name=u'大分类',
        class_name=u'分类名',
        way=u'来源'

    )
    column_searchable_list = ['article_id', 'article_name']
    create_modal = True
    edit_modal = True
    can_export = True
    column_formatters = dict(content=lambda v, c, m, p: m.content[0:50]+'***',
                             main_events=lambda v, c, m, p:
                             m.main_events[:20]+'***')


class Zj(ModelView):
    column_labels = dict(
        expertName=u'专家名',
        like=u'专家简介',
        content='专家介绍',
        headrUrl=u'专家头像地址',
        consultNum=u'咨询量'
    )


class Upload(BaseView):
    @expose('/')
    def upload(self):
        return self.render('index.html')


admin = Admin(name='Admin', endpoint='admin', template_mode='bootstrap3')


file_path = os.path.join(os.path.dirname(__file__), 'static')
# admin.add_view(Upload(name='up', endpoint='upload'))
# admin.add_view(Userview(Sdk,db.session,name='sdk_f'))
admin.add_view(FileAdmin(file_path, '/static/', name='upload'))
admin.add_view(Article_view(Article, db.session, name='article'))
admin.add_view(ModelView(Webchat, db.session, name='webchat'))
admin.add_view(ModelView(Show1, db.session, name='搜索推荐'))
admin.add_view(ModelView(Show6, db.session, name='首页6推荐位'))
admin.add_view(ModelView(Ad1, db.session, name='信息流1'))
admin.add_view(ModelView(Ad2, db.session, name='信息流2'))
admin.add_view(Zj(Expert, db.session, name='专家页'))

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
        get_data = db.session.query(Article).filter_by(article_id=
                                                       get_id).first()
        get_user_like = db.session.query(UserLike).\
            filter_by(user_id=get_user_id, article_id=get_id).first()

        if get_user_id != "null":
            add_user_history = UserHistory(user_id=get_user_id,
                                           article_id=get_id)
            db.session.add(add_user_history)
            db.session.commit()
        else:
            pass

        add_countcollect = db.session.query(Article).filter_by\
            (article_id=get_id).first()
        if add_countcollect.countcollect:
            add_countcollect.countcollect += 1
        else:
            add_countcollect.countcollect = 1
        db.session.commit()

        contentPictures = []
        if get_data:
            if get_data.url:
                pic_list = sorted(json.loads(get_data.url))
                for picture_name in pic_list:
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

            if get_user_like and get_user_id != "null":
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
        get_id = request.args.get("id")
        get_data = db.session.query(Webchat).filter_by(float_id=get_id).first()

        if get_data:
            result = {'webchat': get_data.webchat,
                      'conduct': get_data.conduct,
                      'color': get_data.color}
        else:
            result = {}
        return jsonify(result)
    else:
        return '不支持post请求'


@app.route('/expert', methods=["GET","POST"])
def expert():
    if request.method == "GET":
        get_data = db.session.query(Expert).all()

        expertlist = []
        if get_data:
            for data in get_data:
                result = {
                    "name": data.expertName,
                    "introduce": data.like,
                    "more": data.content,
                    "headerUrl": data.headrUrl,
                    "consultNum": data.consultNum
                }
                expertlist.append(result)

            result = {"expertlist": expertlist}

            return jsonify(result)
        else:
            return "没有专家"

    else:
        return "不支持POST请求"


@app.route('/search1', methods=["GET", "POST"])
def search1():
    if request.method == "GET":
        get_str = request.args.get('str')
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).filter(
            Article.article_name != '').all()
        search1_list = []
        for data in res_datas:
            if get_str in data.article_name:
                search1_list.append(data)

        search1_tuple = tuple(search1_list)
        index1 = int(get_page)*6
        index2 = (int(get_page)+1)*6
        article_list = []
        object_list = list(search1_tuple[index1:index2])
        for i in object_list:
            try:
                picture_url = sorted(json.loads(i.url))[0]
            except:
                picture_url = ""
            res__article_object = {
                "article_id": i.article_id,
                "article_name": i.article_name,
                "content": i.content,
                "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                picture_url,
                "liulancount": i.countcollect,
                "shoucangcount": i.countlike,
                "create_date": str(i.create_date),
                "lanmu": i.column_name
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
        res_datas = db.session.query(Article).order_by(Article.id.desc()).\
            filter_by(way="手").all()
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        index_object_list = res_datas[index1:index2]

        index_list = []

        for i in index_object_list:

            try:
                picture_url = sorted(json.loads(i.url))[0]
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


@app.route('/index2', methods=["GET", "POST"])
def index2():
    if request.method == "GET":
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).order_by(Article.id.desc()).\
            filter_by(way="爬").all()
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        index_object_list = res_datas[index1:index2]

        index_list = []

        for i in index_object_list:

            try:
                picture_url = sorted(json.loads(i.url))[0]

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
        res_datas = db.session.query(Article).all()
        rand_datas = random.sample(res_datas, 4)
        article_list = []
        for i in rand_datas:
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
                print(k, type(k))

                res_article = db.session.query(Article).filter_by(article_id=k)\
                    .first()
                print(res_article)
                try:
                    picture_url = sorted(json.loads(res_article.url))[0]

                except:
                    picture_url = ""
                article_dict = {
                    "article_id": res_article.article_id,
                    "article_name": res_article.article_name,
                    "content": res_article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                    picture_url,
                    "liulancount": res_article.countcollect,
                    "shoucangcount": res_article.countlike,
                    "create_date": str(res_article.create_date)
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
                    picture_url = sorted(json.loads(res_article.url))[0]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": res_article.article_id,
                    "article_name": res_article.article_name,
                    "content": res_article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                    picture_url,
                    "liulancount": res_article.countcollect,
                    "shoucangcount": res_article.countlike,
                    "create_date": str(res_article.create_date)
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
        get_data_id = request.args.get("aid")
        path_dir = os.listdir(os.path.join(os.path.dirname(__file__), 'static'))
        res_articles = db.session.query(Article).\
            filter(Article.id > get_data_id).all()
        # article_ids = []
        # for article in res_articles:
        #     article_ids.append(article.article_id)

        for article in res_articles:
            urls = []
            for k in path_dir:
                xiabiao = k.index("_")
                if str(article.article_id) == k[:xiabiao]:
                    urls.append(k)
                    res_article = db.session.query(Article).\
                        filter_by(article_id=article.article_id).first()
                    res_article.url = json.dumps(urls)
                else:
                    pass
            db.session.commit()

        return 'ok'


@app.route('/ad1', methods=["GET", "POST"])
def ad1():
    if request.method == "GET":
        res_ad1 = db.session.query(Ad1).all()

        ad1s = []
        for i in res_ad1:
            ad1_dic = {
                "pictures_url": i.pic_url,
                "str": i.ad_str
            }
            ad1s.append(ad1_dic)

        result = {
            "ad1": ad1s
        }
        return jsonify(result)

    else:
        return '不支持POST请求'


@app.route('/ad2', methods=["GET", "POST"])
def ad2():
    if request.method == "GET":
        res_ad2 = db.session.query(Ad2).all()
        urls = []
        for i in res_ad2:
            urls.append(i.pic_url)
            result = {
                "pictures_url": urls,
                "head_url": i.head_url,
                "name": i.name,
                "Wx": i.Wx,
                "content": i.content
            }

        return jsonify(result)

    else:
        return '不支持POST请求'


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         for f in request.files.getlist('file'):
#             f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
#     return render_template('index.html')


# 推荐栏目待定
# @app.route('/recommend', methods=["GET", "POST"])
# def recommend():
#     if request.method == "GET":
#         res_datas = db.session.query(Article).all()
#         data_count = len(res_datas)
#
#         recommend_datas = db.session.query(Article).


# 头条栏目待定
# @app.route('/headline', methods=["GET", "POST"])
# def headline():
#     if request.method == "GET":
#         pass


# 健康栏目
@app.route('/health', methods=["GET", "POST"])
def health():
    if request.method == "GET":
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).order_by(Article.id.desc()).all()

        article_list = []
        for article in res_datas:
            if "健康" in article.column_name:
                try:
                    picture_url = sorted(json.loads(article.url))[0]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "content": article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                        picture_url,
                    "liulancount": article.countcollect,
                    "shoucangcount": article.countlike,
                    "create_date": str(article.create_date),
                    "lanmu": "健康"
                }
                article_list.append(article_dict)
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        result_list = article_list[index1:index2]
        result = {"articlelist": result_list}

        return jsonify(result)

    else:
        return "不支持POST请求"


# 饮食栏目
@app.route('/food', methods=["GET", "POST"])
def food():
    if request.method == "GET":
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).order_by(Article.id.desc()).all()

        article_list = []
        for article in res_datas:
            if "饮食" in article.column_name:
                try:
                    picture_url = sorted(json.loads(article.url))[0]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "content": article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                        picture_url,
                    "liulancount": article.countcollect,
                    "shoucangcount": article.countlike,
                    "create_date": str(article.create_date),
                    "lanmu": "饮食"
                }
                article_list.append(article_dict)
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        result_list = article_list[index1:index2]
        result = {"articlelist": result_list}

        return jsonify(result)

    else:
        return "不支持POST请求"


# 训练栏目
@app.route('/fitness', methods=["GET", "POST"])
def fitness():
    if request.method == "GET":
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).order_by(Article.id.desc()).all()

        article_list = []
        for article in res_datas:
            if "训练" in article.column_name:
                try:
                    picture_url = sorted(json.loads(article.url))[0]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "content": article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                        picture_url,
                    "liulancount": article.countcollect,
                    "shoucangcount": article.countlike,
                    "create_date": str(article.create_date),
                    "lanmu": "训练"
                }
                article_list.append(article_dict)
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        result_list = article_list[index1:index2]
        result = {"articlelist": result_list}

        return jsonify(result)

    else:
        return "不支持POST请求"


# 美容栏目
@app.route('/beauty', methods=["GET", "POST"])
def beauty():
    if request.method == "GET":
        get_page = request.args.get('page')
        res_datas = db.session.query(Article).order_by(Article.id.desc()).all()

        article_list = []
        for article in res_datas:
            if "美容" in article.column_name:
                try:
                    picture_url = sorted(json.loads(article.url))[0]
                except:
                    picture_url = ""
                article_dict = {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "content": article.content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                        picture_url,
                    "liulancount": article.countcollect,
                    "shoucangcount": article.countlike,
                    "create_date": str(article.create_date),
                    "lanmu": "美容"
                }
                article_list.append(article_dict)
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        result_list = article_list[index1:index2]
        result = {"articlelist": result_list}

        return jsonify(result)

    else:
        return "不支持POST请求"


# 百科
@app.route('/bike', methods=["GET","POST"])
def bike():
    if request.method == "GET":
        get_key = request.args.get('key')
        get_page = request.args.get('page')
        get_datas = db.session.query(Article).order_by(Article.id.desc())\
            .filter_by(class_name=get_key).all()
        print(get_key)
        if get_datas:
            article_list = []
            for article in get_datas:
                try:
                    picture_url = sorted(json.loads(article.url))[0]
                except:
                    picture_url = ""

                article_dict = {
                    "article_id": article.article_id,
                    "article_name": article.article_name,
                    "content": article.content,
                    "picture_url": "https://xcx.51babyapp.com/dog/static/" +
                                   picture_url,
                    "liulancount": article.countcollect,
                    "shoucangcount": article.countlike,
                    "create_date": str(article.create_date)
                }
                article_list.append(article_dict)
            index1 = int(get_page) * 6
            index2 = (int(get_page) + 1) * 6
            result_list = article_list[index1:index2]
            result = {"artilcelist": result_list}

            return jsonify(result)
        else:
            return '该类目暂时没有内容'
    else:
        return "不支持POST请求"


# 保存用户狗的信息
@app.route('/saveDog', methods=["GET", "POST"])
def savedog():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        get_isHaveDog = request.args.get('haveDog')
        get_dogType = request.args.get('dogType')
        get_dogSex = request.args.get('dogSex')
        get_dogAget = request.args.get('dogAge')

        add_dog = User_dg(use_id=get_user_id, isHaveDog=get_isHaveDog,
                          dogType=get_dogType, dogSex=get_dogSex,
                          dog_Age=get_dogAget)
        db.session.add(add_dog)
        db.session.commit()

        return '保存成功'


# 保存用户关系问题信息
@app.route('/questions', methods=["GET", "POST"])
def question():
    if request.method == "POST":
        get_data = request.data
        dict_data = json.loads(get_data)
        len_data = len(dict_data)
        for n in range(1, len_data):
            print(n)
            add_question = User_question(user_id=dict_data['user_id'],
                                         questions=dict_data['str%s'%(n)])
            db.session.add(add_question)
            db.session.commit()
        return 'ok'

    else:
        return '请用GET请求'


# 文章打标签
@app.route('/mark', methods=["GET", "POST"])
def mark():
    if request.method == "GET":
        test_data = db.session.query(Article).all()
        get_datas = db.session.query(Article).filter_by(class_name='[]').all()
        health_list = ['眼珠脱垂', '干眼证', '白内障', '眼膜炎', '眼睑炎', '视神经炎',
                       '角膜炎', '眼虫病', '青光眼', '卡他性口炎', '真菌性口炎',
                       '牙周炎', '咽炎', '咽麻痹', '食管炎', '食惯梗阻', '急性胃卡他',
                       '慢新胃卡他', '胃扩张', '胃出血', '幽门狭窄', '溃疡性口炎',
                       '肠胃炎', '体内驱虫', '体外驱虫', '皮肤过敏', '疥癣',
                       '嗜舔性皮肤炎', '皮肤肿瘤', '急性湿性皮炎', '免疫功能絮乱',
                       '细菌', '真菌', '细小', '狗瘟', '翻肠', '骨折']

        for class_name in health_list:
            for data in get_datas:
                if class_name in data.content:
                    class_list = json.loads(data.class_name)
                    column_list = json.loads(data.column_name)
                    class_list.append(class_name)
                    column_list.append('健康')
                    column_list = list(set(column_list))
                    data.column_name = json.dumps(column_list,
                                                  ensure_ascii=False)
                    data.class_name = json.dumps(class_list, ensure_ascii=False)
                    db.session.commit()

        return 'ok'


@app.route('/bigclass', methods=["GET", "POST"])
def bigclass():
    if request.method == "GET":
        get_datas = db.session.query(Article).filter(
            Article.class_name != '[]').all()
        for i in get_datas:
            i.bigclass_name = json.dumps([], ensure_ascii=False)
            db.session.commit()
        eyes_list = ['眼珠脱垂','干眼证','白内障','眼膜炎','眼睑炎','视神经炎',
                     '角膜炎','眼虫病','青光眼']
        neike_list= ['卡他性口炎','真菌性口炎','牙周炎','咽炎','咽麻痹','食管炎',
                     '食惯梗阻','急性胃卡他','慢新胃卡他','胃扩张','胃出血',
                     '幽门狭窄','溃疡性口炎','肠胃炎','体内驱虫']
        pifu_list = ['体外驱虫','皮肤过敏','疥癣','嗜舔性皮肤炎','皮肤肿瘤',
                     '急性湿性皮炎','免疫功能絮乱','细菌','真菌']
        others_list = ['细小','狗瘟','翻肠','骨折']

        for data in get_datas:
            for get_class in json.loads(data.class_name):
                get_bigclass = json.loads(data.bigclass_name)
                if get_class in eyes_list:
                    get_bigclass.append('眼睛')
                elif get_class in neike_list:
                    get_bigclass.append('内科')
                elif get_class in pifu_list:
                    get_bigclass.append('皮肤病')
                elif get_class in others_list:
                    get_bigclass.append('其他')
                lastclass_name = list(set(get_bigclass))
                data.bigclass_name = json.dumps(lastclass_name,
                                                ensure_ascii=False)
                db.session.commit()

        return 'ok'


if __name__ == '__main__':
    app.run(threaded=True)


