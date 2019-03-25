import os
import json
import random
import time
from collections import Counter

from flask import Flask, request, jsonify, render_template
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
import jieba


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
    class_name = db.Column(db.String(20))


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
    user_headImg = db.Column(db.String(200))
    user_sign = db.Column(db.String(200))


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


class Recommend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keys = db.Column(db.String(500))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200), comment="提问用户id")
    user_name = db.Column(db.String(50), comment="提问用户名")
    isAnonymous = db.Column(db.String(10), comment="是否匿名")
    user_headImg = db.Column(db.String(200), comment="提问用户头像地址")
    question_id = db.Column(db.String(200), comment="问题id")
    question_name = db.Column(db.String(200), comment="问题标题")
    question_content = db.Column(db.String(500), comment="问题描述")
    question_pictures = db.Column(db.String(500), comment="问题上传图片地址")
    collect_count = db.Column(db.Integer, comment="问题浏览量")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(200), comment="评论id")
    user_id = db.Column(db.String(200), comment="评论人id")
    question_id = db.Column(db.String(200), comment="问题id")
    user_name = db.Column(db.String(50), comment="评论人名")
    isAnonymous = db.Column(db.String(10), comment="是否匿名")
    comment_content = db.Column(db.String(500), comment="评论内容")
    up_count = db.Column(db.Integer, comment="点赞数")
    user_headImag = db.Column(db.String(200), comment="评论人头像地址")
    comment_pictures = db.Column(db.String(500), comment="评论人上传图片地址")


class UserUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(200), comment="评论id")
    user_id = db.Column(db.String(200), comment="用户id")
    up_count = db.Column(db.Integer, comment="评论点赞数")


class Article_view(ModelView):
    form_columns = ('article_id', 'article_name', 'content', 'main_events',
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
    column_formatters = dict(content=lambda v, c, m, p: m.content[0:50] + '***',
                             main_events=lambda v, c, m, p:
                             m.main_events[:20] + '***')


class Zj(ModelView):
    column_labels = dict(
        expertName=u'专家名',
        like=u'专家简介',
        content='专家介绍',
        headrUrl=u'专家头像地址',
        consultNum=u'咨询量',
        class_name=u'专家标签'
    )


class Upload(BaseView):

    @expose('/')
    def upload(self):
        return self.render('index.html')


admin = Admin(name='Admin', endpoint='admin', template_mode='bootstrap3')


file_path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(Upload(name='up', endpoint='upload'))
# admin.add_view(Userview(Sdk,db.session,name='sdk_f'))
admin.add_view(FileAdmin(file_path, '/static/', name='upload'))
admin.add_view(Article_view(Article, db.session, name='article'))
admin.add_view(ModelView(Webchat, db.session, name='webchat'))
admin.add_view(ModelView(Show1, db.session, name='搜索推荐'))
admin.add_view(ModelView(Show6, db.session, name='首页6推荐位'))
admin.add_view(ModelView(Ad1, db.session, name='信息流1'))
admin.add_view(ModelView(Ad2, db.session, name='信息流2'))
admin.add_view(Zj(Expert, db.session, name='专家页'))
admin.add_view(ModelView(Recommend, db.session, name='推荐词'))

app.config.from_object('config')
db.init_app(app)
db.create_all(app=app)
admin.init_app(app)
app.secret_key = 'qw123098'
app.config['JSON_AS_ASCII'] = False


@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')


# 返回文章数据(已测试)
@app.route('/dog', methods=["GET", "POST"])
def dog():
    if request.method == "GET":
        get_id = request.args.get('article_id')
        get_user_id = request.args.get('user_id')
        get_data = db.session.query(Article).filter_by(
            article_id=get_id).first()
        get_user_like = db.session.query(UserLike).\
            filter_by(user_id=get_user_id, article_id=get_id).first()

        if get_user_id != "null":
            res_history = db.session.query(UserHistory).\
                filter_by(user_id=get_user_id, article_id=get_id).first()
            if res_history:
                db.session.delete(res_history)
                db.session.commit()
            add_user_history = UserHistory(user_id=get_user_id,
                                           article_id=get_id)
            db.session.add(add_user_history)
            db.session.commit()
        else:
            pass

        add_countcollect = db.session.query(Article)\
            .filter_by(article_id=get_id).first()
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


@app.route('/expert', methods=["GET", "POST"])
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
                    "consultNum": data.consultNum,
                    "class_name": data.class_name
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
    """
    搜索功能实现，借助jieba库实现字符串分词，将分词进行数据库文章名匹配
    同时搜索方法实现了，关键词完整匹配，关键词按数据库出现的数量由小到大排列
    同时给前段返回精确的匹配关键词key
    """

    if request.method == "GET":
        get_str = request.args.get("str")
        get_page = request.args.get("page")
        seg_list = jieba.lcut_for_search(get_str)
        all_datas = db.session.query(Article).all()

        object_list = []
        part_list = []
        for data1 in all_datas:
            if get_str in data1.article_name:
                object_list.append((get_str, data1))
            else:
                pass

        object_data_list = [data[1] for data in object_list]
        for data2 in all_datas:
            for searchStr in seg_list:
                part_data_list = [data1[1] for data1 in part_list]
                if searchStr in data2.article_name and data2 not in \
                        object_data_list and data2 not in part_data_list:
                    part_list.append((searchStr, data2))
                else:
                    pass
        # object_list += sorted(part_list)
        list_key = [key[0] for key in part_list]
        list_key_sort = sorted(Counter(list_key))

        part_finish_list = []
        for key in list_key_sort:
            for tuple_part in part_list:
                if tuple_part[0] == key:
                    part_finish_list.append(tuple_part)
                else:
                    pass

        object_list += part_finish_list
        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6
        articleList = []

        if object_list:
            for i in object_list[index1:index2]:
                try:
                    picture_url = sorted(json.loads(i[1].url))[0]
                except:
                    picture_url = ''
                result = {
                    "article_id": i[1].article_id,
                    "article_name": i[1].article_name,
                    "content": i[1].content,
                    "pictures_url": "https://xcx.51babyapp.com/dog/static/" +
                                    picture_url,
                    "liulancount": i[1].countcollect,
                    "shoucangcount": i[1].countlike,
                    "create_date": str(i[1].create_date),
                    "lanmu": i[1].column_name,
                    "key": i[0]
                }
                articleList.append(result)
        else:
            pass

        results = {"articlelist": articleList}

        return jsonify(results)


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


@app.route('/SaveUser', methods=["GET", "POST"])
def saveuser():
    if request.method == "POST":
        get_data = request.get_data()
        data_dic = json.loads(get_data)
        user_id = data_dic["user_id"]
        res_data = db.session.query(User).filter_by(user_id=user_id).first()
        if res_data:
            pass
        else:
            add_data = User(user_id=user_id, user_name=data_dic["user_name"],
                            user_headImg=data_dic["user_headImg"],
                            user_sign=data_dic["user_sign"])
            db.session.add(add_data)
            db.session.commit()

        return "ok"
    else:
        return "不支持GET请求"


# 用户收藏(已测试)
@app.route('/like', methods=["GET", "POST"])
def like():
    if request.method == "GET":
        get_user_id = request.args.get('user_id')
        get_article_id = request.args.get('article_id')
        res_data = db.session.query(UserLike).filter_by(
            user_id=get_user_id, article_id=get_article_id).first()
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

        res_history = db.session.query(UserHistory)\
            .filter_by(user_id=get_user_id).all()
        result = {
            "likes": str(len(res_like)),
            "histories": str(len(res_history))
        }

        return jsonify(result)

    else:
        return '不支持POST请求'


@app.route('/picture', methods=["GET", "POST"])
def picture():
    """
    图片自动添加脚本路由，aid 理论应为数据库中没有url数据的起始id,
    由于录入的数据没有录入图片的具体网址，该路由完成的功能是，将本地
    图片名称，以json格式追加到数据库对应的url中，(不用手动录入图片
    地址，也千万不要录入，)否则会出现图片无法识别的情况
    """

    if request.method == "GET":
        get_data_id = request.args.get("aid")
        path_dir = os.listdir(os.path.join(
            os.path.dirname(__file__), 'static'))
        res_articles = db.session.query(Article).\
            filter(Article.id > get_data_id).all()

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
    """
    信息流1路由，本路由下自定义信息流的图
    片路径和文本信息，有多少条信息返回多少条信息
    """

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
    """
    信息流数据2，当录入多条信息流数据时，要保证最后录入的一条信息是完全的
    ，这样就可以保证以数组形式提供数据，否则的话，会造成异常数据
    """

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


# 推荐栏目
@app.route('/recommend', methods=["GET", "POST"])
def recommend():
    if request.method == "GET":
        res_data = db.session.query(Recommend).first()

        if res_data:
            keys = res_data.keys.split(',')

        result = {"keys": keys}
        return jsonify(result)


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
@app.route('/bike', methods=["GET", "POST"])
def bike():
    if request.method == "GET":
        get_key = request.args.get('key')
        get_page = request.args.get('page')
        get_datas = db.session.query(Article).order_by(Article.id.desc())\
            .filter_by(class_name=get_key).all()
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
            add_question = User_question(user_id=dict_data['user_id'],
                                         questions=dict_data['str%s' % (n)])
            db.session.add(add_question)
            db.session.commit()
        return 'ok'

    else:
        return '请用GET请求'


# 文章打标签
@app.route('/mark', methods=["GET", "POST"])
def mark():
    """
    对文章分类信息进行检索匹配，对于包含自定义字符串的文章，
    加入标签标记，本路由将完成，一级标签和三级标签的匹配
    """

    if request.method == "GET":
        get_datas = db.session.query(Article).\
            filter(Article.class_name.contains('[]')).all()
        health_list = ['眼珠脱垂', '干眼证', '白内障', '眼膜炎', '眼睑炎', '视神经炎',
                       '角膜炎', '眼虫病', '青光眼', '卡他性口炎', '真菌性口炎',
                       '牙周炎', '咽炎', '咽麻痹', '食管炎', '食惯梗阻', '急性胃卡他',
                       '慢新胃卡他', '胃扩张', '胃出血', '幽门狭窄', '溃疡性口炎',
                       '肠胃炎', '体内驱虫', '体外驱虫', '皮肤过敏', '疥癣',
                       '嗜舔性皮肤炎', '皮肤肿瘤', '急性湿性皮炎', '免疫功能絮乱',
                       '细菌', '真菌', '细小', '狗瘟', '翻肠', '骨折']
        food_list = ['羊奶', '狗粮', '益生菌', '小零食', '驱虫药', '磨牙棒', '营养膏',
                     '钙片']
        fitness_list = ['定时作息', '定时入笼', '定时饮食', '定点排便', '乱咬乱斯',
                        '翻垃圾桶', '乱拾食物', '咬人']
        beauty_list = ['剪毛', '染毛', '剪耳朵', '清耳朵', '断尾']

        for class_name in health_list:
            for data in get_datas:
                if class_name in data.content:
                    print(class_name)
                    class_list = json.loads(data.class_name)
                    column_list = json.loads(data.column_name)
                    class_list.append(class_name)
                    column_list.append('健康')
                    column_list = list(set(column_list))
                    data.column_name = json.dumps(column_list,
                                                  ensure_ascii=False)
                    data.class_name = json.dumps(
                        class_list, ensure_ascii=False)
                    db.session.commit()
                else:
                    pass

        for class_name in food_list:
            for data in get_datas:
                if class_name in data.content:
                    class_list = json.loads(data.class_name)
                    column_list = json.loads(data.column_name)
                    class_list.append(class_name)
                    column_list.append('饮食')
                    column_list = list(set(column_list))
                    data.column_name = json.dumps(column_list,
                                                  ensure_ascii=False)
                    data.class_name = json.dumps(
                        class_list, ensure_ascii=False)
                    db.session.commit()
                else:
                    pass

        for class_name in fitness_list:
            for data in get_datas:
                if class_name in data.content:
                    class_list = json.loads(data.class_name)
                    column_list = json.loads(data.column_name)
                    class_list.append(class_name)
                    column_list.append('训练')
                    column_list = list(set(column_list))
                    data.column_name = json.dumps(column_list,
                                                  ensure_ascii=False)
                    data.class_name = json.dumps(
                        class_list, ensure_ascii=False)
                    db.session.commit()
                else:
                    pass

        for class_name in beauty_list:
            for data in get_datas:
                if class_name in data.content:
                    class_list = json.loads(data.class_name)
                    column_list = json.loads(data.column_name)
                    class_list.append(class_name)
                    column_list.append('美容')
                    column_list = list(set(column_list))
                    data.column_name = json.dumps(column_list,
                                                  ensure_ascii=False)
                    data.class_name = json.dumps(
                        class_list, ensure_ascii=False)
                    db.session.commit()
                else:
                    pass

        return 'ok'


@app.route('/bigclass', methods=["GET", "POST"])
def bigclass():
    """
    对于加入一级标签和三级标签的数据，本路由将完成加二级标签的功能
    """

    if request.method == "GET":
        get_datas = db.session.query(Article).filter(
            Article.class_name != '[]').all()
        for i in get_datas:
            i.bigclass_name = json.dumps([], ensure_ascii=False)
            db.session.commit()
        eyes_list = ['眼珠脱垂', '干眼证', '白内障', '眼膜炎', '眼睑炎', '视神经炎',
                     '角膜炎', '眼虫病', '青光眼']
        neike_list = ['卡他性口炎', '真菌性口炎', '牙周炎', '咽炎', '咽麻痹', '食管炎',
                      '食惯梗阻', '急性胃卡他', '慢新胃卡他', '胃扩张', '胃出血',
                      '幽门狭窄', '溃疡性口炎', '肠胃炎', '体内驱虫']
        pifu_list = ['体外驱虫', '皮肤过敏', '疥癣', '嗜舔性皮肤炎', '皮肤肿瘤',
                     '急性湿性皮炎', '免疫功能絮乱', '细菌', '真菌']
        others_list = ['细小', '狗瘟', '翻肠', '骨折']

        daily_list = ['羊奶', '狗粮', '益生菌', '小零食']
        special_list = ['驱虫药', '磨牙棒', '营养膏', '钙片']

        xgyc_list = ['定时作息', '定时入笼', '定时饮食', '定点排便']
        mbjz_list = ['乱咬乱斯', '翻垃圾桶', '乱拾食物', '咬人']

        hair_list = ['剪毛', '染毛']
        operation_list = ['剪耳朵', '清耳朵', '断尾']

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

        for data1 in get_datas:
            for get_class in json.loads(data1.class_name):
                get_bigclass = json.loads(data1.bigclass_name)
                if get_class in daily_list:
                    get_bigclass.append('日常')
                elif get_class in special_list:
                    get_bigclass.append('特殊')
                lastclass_name = list(set(get_bigclass))
                data1.bigclass_name = json.dumps(lastclass_name,
                                                 ensure_ascii=False)
                db.session.commit()

        for data2 in get_datas:
            for get_class in json.loads(data2.class_name):
                get_bigclass = json.loads(data2.bigclass_name)
                if get_class in xgyc_list:
                    get_bigclass.append('习惯养成')
                elif get_class in mbjz_list:
                    get_bigclass.append('毛病纠正')
                lastclass_name = list(set(get_bigclass))
                data2.bigclass_name = json.dumps(lastclass_name,
                                                 ensure_ascii=False)
                db.session.commit()

        for data3 in get_datas:
            for get_class in json.loads(data3.class_name):
                get_bigclass = json.loads(data3.bigclass_name)
                if get_class in hair_list:
                    get_bigclass.append('毛发')
                elif get_class in operation_list:
                    get_bigclass.append('手术')
                lastclass_name = list(set(get_bigclass))
                data3.bigclass_name = json.dumps(lastclass_name,
                                                 ensure_ascii=False)
                db.session.commit()

        return 'ok'


@app.route('/del', methods=["GET", "POST"])
def delkey():
    res_data = db.session.query(Article).all()

    for data in res_data:
        if 'douchai144' in data.content:
            data.content = data.content.replace('douchai144', 'XQ113143')
            db.session.commit()
            print(data.article_id)
        else:
            pass
    return 'ok'


@app.route('/cat', methods=["GET", "POST"])
def cat():
    res_data = db.session.query(Article).filter(
        Article.article_id > 10121).all()
    for i in res_data:
        if '\t' in i.content:
            i.content = i.content.replace('\t', '\r\t')
            db.session.commit()
        else:
            pass
    return "ok"


@app.route('/find', methods=["GET", "POST"])
def find():
    res_datas = db.session.query(Article).all()
    for i in res_datas:
        if 'img' not in i.content:
            print(i.article_id)

    return "ok"


@app.route('/ask', methods=["GET", "POST"])
def ask():
    """
    提问模块，用户输入问题，和问题描述以及图片,问题和问题描述不可以为空值，图片可以不添加
    将用户信息全部存入数据库question,包括用户名，用户id,用户头像地址，问题和问题描述
    """

    if request.method == "POST":
        get_data = request.get_data()

        get_name = request.headers.get("picname")
        get_id = request.headers.get("questionid")
        res_data = db.session.query(Question).filter_by(
            question_id=get_id).first()

        if get_name:
            path = os.path.dirname(os.path.abspath(__file__))\
                + "/static/question/"
            pic_name = path + get_name
            with open(pic_name, "wb") as f:
                f.write(get_data)
            pathdir = os.listdir(path)
            pictures = []
            for i in pathdir:
                if get_id in i:
                    pictures.append(i)

            pictures = list(set(pictures))
            res_data.question_pictures = json.dumps(pictures)
            db.session.commit()

        else:
            path_time = str(time.time()).replace('.', '')
            data_dic = json.loads(get_data)
            question_id = path_time
            path_head = "https://xcx.51babyapp.com/dog/static/head/"
            get_pichead = data_dic["user_headImg"]
            user_headImg = path_head + \
                get_pichead if get_pichead != "0" else "0"
            add_questions = Question(user_id=data_dic["user_id"],
                                     user_name=data_dic["user_name"],
                                     user_headImg=user_headImg,
                                     question_id=question_id,
                                     question_name=data_dic["question_name"],
                                     question_content=data_dic[
                                         "question_content"],
                                     isAnonymous=data_dic["isAnonymous"]
                                     )
            db.session.add(add_questions)
            db.session.commit()
            return question_id

        return "ok"
    else:
        return "不支持GET请求"


@app.route('/comment', methods=["GET", "POST"])
def comment():
    """
    用户评论信息，用户输入评论的问题id,用户名，用户id,评论内容，评论图片可添加也可不添加,储存
    用户的评论信息
    """

    if request.method == "POST":
        get_data = request.get_data()
        get_name = request.headers.get("picname")
        get_pcid = request.headers.get("pcid")

        res_data = db.session.query(Comment).filter_by(
            comment_id=get_pcid).first()

        if get_name:
            path = os.path.dirname(os.path.abspath(__file__)) \
                + "/static/comment/"
            pic_name = path + get_name
            with open(pic_name, "wb") as f:
                f.write(get_data)
            pathdir = os.listdir(path)
            pictures = []
            for i in pathdir:
                if get_pcid in i:
                    pictures.append(i)
            pictures = list(set(pictures))
            res_data.comment_pictures = json.dumps(pictures)
            db.session.commit()

        else:
            data_dic = json.loads(get_data)
            path_head = "https://xcx.51babyapp.com/dog/static/head/"
            get_pichead = data_dic["user_headImg"]
            user_headImg = path_head + \
                get_pichead if get_pichead != "0" else "0"
            add_comment = Comment(user_id=data_dic["user_id"],
                                  comment_id=data_dic["commentid"],
                                  user_name=data_dic["user_name"],
                                  question_id=data_dic["question_id"],
                                  user_headImag=user_headImg,
                                  comment_content=data_dic["comment_content"],
                                  isAnonymous=data_dic["isAnonymous"]
                                  )
            db.session.add(add_comment)
            db.session.commit()
        return "ok"
    else:
        return "不支持GET请求"


@app.route('/userComment', methods=["GET", "POST"])
def detailask():
    """
    输入qid用户问题id,和page分页，实现用户问题和用户评论信息同时加载，同时评论信息支持分页
    """
    if request.method == "GET":
        get_id = request.args.get("questionid")
        get_cid = request.args.get("commentid")
        get_page = request.args.get("page")

        res_data = db.session.query(Question).\
            filter_by(question_id=get_id).first()
        try:
            res_data.collect_count += 1
        except:
            res_data.collect_count = 1
        db.session.commit()

        res_comments = db.session.query(Comment).\
            filter_by(question_id=get_id).all()
        res_userup = db.session.query(
            UserUp).filter_by(comment_id=get_cid).all()

        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6

        comments = res_comments[index1:index2]

        try:
            question_pictures = [
                "https://xcx.51babyapp.com/dog/static/question/"
                + k for k in sorted(json.loads(res_data.question_pictures))]
        except:
            question_pictures = []

        first_dic = {
            "user_name": res_data.user_name,
            "user_headImg": res_data.user_headImg,
            "question_name": res_data.question_name,
            "question_content": res_data.question_content,
            "question_pictures": question_pictures,
            "answer_count": str(len(res_comments))
        }
        comment_list = []

        for data in comments:
            try:
                comment_pictures = [
                    "https://xcx.51babyapp.com/dog/static/comment/"
                    + k for k in sorted(json.loads(data.comment_pictures))]
            except:
                comment_pictures = []
            user_headImg = data.user_headImag if data.user_headImag != "0" else "0"
            second_dic = {
                "user_name": data.user_name,
                "user_headImg": user_headImg,
                "comment": data.comment_content,
                "isAnonymous": data.isAnonymous,
                "up_count": str(len(res_userup)),
                "comment_pictures": comment_pictures
            }
            comment_list.append(second_dic)

        result = {
            "question": first_dic,
            "comments": comment_list
        }

        return jsonify(result)
    else:
        return "不支持POST请求"


@app.route("/getAsk", methods=["GET", "POST"])
def getask():
    if request.method == "GET":
        get_page = request.args.get("page")
        res_datas = db.session.query(
            Question).order_by(Question.id.desc()).all()

        index1 = int(get_page) * 6
        index2 = (int(get_page) + 1) * 6

        question_list = []
        for data in res_datas[index1:index2]:
            question_id = data.question_id

            res_comment = db.session.query(
                Comment).filter_by(question_id=question_id).all()
            try:
                pic_url = sorted(json.loads(data.question_pictures))[0]
            except:
                pic_url = ''
            user_headImg = data.user_headImg if data.user_headImg != "0" else "0"

            question_dic = {
                "user_name": data.user_name,
                "question_id": data.question_id,
                "user_headImg": user_headImg,
                "isAnonymous": data.isAnonymous,
                "question_name": data.question_name,
                "question_content": data.question_content,
                "collectCount": data.collect_count,
                "answerCount": str(len(res_comment)),
                "pic_url": "https://xcx.51babyapp.com/dog/static/question/"
                           + pic_url
            }
            question_list.append(question_dic)
        result = {"asklist": question_list}

        return jsonify(result)
    else:
        return "不支持POST请求"


@app.route('/addup', methods=["GET", "POST"])
def addup():
    if request.method == "GET":
        get_id = request.args.get("commentid")
        get_uid = request.args.get("userid")
        res_userup = db.session.query(UserUp).filter_by(comment_id=get_id,
                                                        user_id=get_uid).first()
        if res_userup:
            return "nook"
        else:
            add_userup = UserUp(comment_id=get_id, user_id=get_uid, up_count=1)
            db.session.add(add_userup)
            db.session.commit()
        return "ok"


@app.route('/editUser', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        get_data = request.get_data()
        get_picname = request.headers.get("picname")

        if get_picname:

            path = os.path.dirname(os.path.abspath(__file__))
            name = path + "/static/head/" + get_picname
            with open(name, "wb") as f:
                f.write(get_data)
        else:
            data_dic = json.loads(get_data)
            get_uid = data_dic["user_id"]
            res_data = db.session.query(
                User).filter_by(user_id=get_uid).first()
            res_questions = db.session.query(Question).\
                filter_by(user_id=get_uid).all()
            res_comments = db.session.query(Comment).\
                filter_by(user_id=get_uid).all()
            pic_path = "https://xcx.51babyapp.com/dog/static/head/"
            if res_data:
                res_data.user_name = data_dic["user_name"]
                res_data.user_headImg = pic_path + data_dic["picname"]
                res_data.sign = data_dic["sign"]
                db.session.commit()
            else:
                add_user = User(user_id=data_dic["user_id"],
                                user_headImg=pic_path + data_dic["picname"],
                                user_name=data_dic["user_name"],
                                user_sign=data_dic["sign"])
                db.session.add(add_user)
                db.session.commit()
            for data1 in res_questions:
                data1.user_headImg = pic_path + data_dic["picname"]
                db.session.commit()
            for data2 in res_comments:
                data2.user_headImag = pic_path + data_dic["picname"]
                db.session.commit()

        return "ok"
    else:
        return "不支持GET请求"


if __name__ == '__main__':
    app.run(threaded=True)
