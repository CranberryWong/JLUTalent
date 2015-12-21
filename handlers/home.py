#! /usr/bin/env python
#coding=utf-8

import logging
import time
import os
import json
import tornado.web
import markdown
import random
from models.entity import User, Article, Page, News, Type, Contact, Inform, Meetinfo, Links, Upload
from models.entity import db_session
from handlers.settings import SITESETTINGS
from handlers.admin import nameRewrite
from handlers.util import SignValidateBase
from handlers.generateObject import ArticleListObject, PageListObject, MeetinfoObject, UploadListObject, NewsListObject
from datetime import datetime
from PIL import Image
from cStringIO import StringIO

global lang_encode
lang_encode = 'zh_CN'
tornado.locale.set_default_locale(lang_encode)
#页面通用数据
avatar_path = os.path.join(os.path.abspath('.'), 'static/avatar/')
resume_path = os.path.join(os.path.abspath('.'), 'static/resume/')
homelog_path = os.path.join(os.path.abspath('.'), 'log/')

logging.basicConfig(level=logging.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=homelog_path + 'myapp.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class changeLang(tornado.web.RequestHandler):
    def get(self):
        global lang_encode
        if lang_encode == 'zh_CN':
            lang_encode = 'en_US'
        else:
            lang_encode = 'zh_CN'
        tornado.locale.set_default_locale(lang_encode)
        self.redirect('/')
        
class homeBase(SignValidateBase):
    def init(self):
        self.sitename = SITESETTINGS['site_name']
        self.siteversion = SITESETTINGS['site_version']
        self.session = db_session.getSession
        self.signeduser = SignValidateBase.get_current_user(self)
        global lang_encode
        if lang_encode == 'zh_CN':
            self.lang = 'English'
        else:
            self.lang = '中文版'
        if self.signeduser:
            self.user = self.session.query(User).filter(User.username == self.signeduser).first()
            self.signedid = self.user.uid
            self.signavatar = self.user.uavatar
        else:
            self.signedid = None
            
    def get_user_locale(self):
        #return tornado.locale.set_default_locale('en_US')
        return tornado.locale.get("en_US")

#用于阅读类界面的渲染
class StaticBase(homeBase):
    def init(self):
        homeBase.init(self)
        #所有类型
        self.alltype = self.session.query(Type)
        self.meetinfo = MeetinfoObject(self.session.query(Meetinfo).order_by(Meetinfo.mcettime.desc()).first()) if self.session.query(Meetinfo).order_by(Meetinfo.mcettime.desc()).first() else None
        self.links = self.session.query(Links).all()
        #归档
        articlelist = self.session.query(Article).order_by(Article.apubtime.desc()).all()
        topyear = articlelist[0].apubtime.year
        bottomyear = articlelist[len(articlelist) - 1].apubtime.year
        self.articlebydate = []
        for year in range(bottomyear, topyear + 1):
            for month in range(1, 13):
                nums = len([article for article in articlelist if article.apubtime.year == year and article.apubtime.month ==month])
                if nums != 0:
                    self.articlebydate.insert(0, {'year':year, 'month':month, 'num':nums})

class Pagination(object):
    def __init__(self):
        self.pre = ''
        self.next = ''
        self.pages = []
        self.current = ''
        self.action = ''

def generatePagination(action, bloglist, targetpage):
    targetpage = int(targetpage)
    pagination = Pagination()
    pagination.current = targetpage
    maxpage = len(bloglist)
    pagination.pages = range(1, maxpage/10+2)
    pagination.pre = str(targetpage-1) if targetpage-1 in pagination.pages else str(targetpage)
    pagination.next = str(targetpage+1) if targetpage+1 in pagination.pages else str(targetpage)
    pagination.action = action
    bloglist = bloglist[(targetpage-1) * 10 : targetpage * 10]
    return bloglist, pagination


class Home(homeBase):
    def get(self):
        homeBase.init(self)
        self.title = 'Home'
        informlist = self.session.query(Inform).order_by(Inform.icettime)[:3]
        pagelist = self.session.query(Page).order_by(Page.ppubtime)[:3]
        articlelist = []
        for one in self.session.query(Article).order_by(Article.apubtime)[:7]:
            articlelist.insert(0, ArticleListObject(one))
        self.render('home_index.html', pagelist = pagelist, informlist = informlist, articlelist = articlelist)
        self.session.close()


class ListProjects(StaticBase):
    def get(self):
        #homeBase.init(self)
        StaticBase.init(self)
        self.title = 'Projects'
        targetpage = int(self.get_argument('page',default='1'))
        pagelist = []
        pagelist = list(map(lambda one: PageListObject(one), [one for one in self.session.query(Page).all()]))
        #pagelist.insert(0, PageListObject(one)) for one in self.session.query(Page).all()
        pageList, self.pagination = generatePagination('/projects?page=', pagelist, targetpage)
        self.render('home_plist.html', list = pageList)
        self.session.close()


class ShowProjects(StaticBase):
    def get(self, pid):
        StaticBase.init(self)
        ppage = self.session.query(Page).filter(Page.pid == pid).first()
        page = PageListObject(ppage)
        self.title = page.ptitle
        self.render('home_showpage.html', page = page)
        self.session.close()

class ListNews(StaticBase):
    def get(self):
        #homeBase.init(self)
        StaticBase.init(self)
        self.title = 'News'
        targetpage = int(self.get_argument('page',default='1'))
        newslist = []
        for one in self.session.query(News).all():
            newslist.insert(0, NewsListObject(one))
        newsList, self.pagination = generatePagination('/news?page=', newslist, targetpage)
        self.render('home_plist.html', list = newsList)
        self.session.close()

class ShowNews(StaticBase):
    def get(self, nid):
        StaticBase.init(self)
        nnews = self.session.query(News).filter(News.nid == nid).first()
        news = PageListObject(nnews)
        self.title = news.ptitle
        self.render('home_showpage.html', news = news)
        self.session.close()

class ListMembers(homeBase):
    def get(self):
        homeBase.init(self)
        self.title = 'Members'
        mtype = ['All', 'Master', 'Ph.D', 'Bachelor', 'Professor', 'Guest Prof']
        degree = self.get_argument('degree', default='All')
        if degree == 'All':
            memberlist = self.session.query(User).filter(User.ucheck == True).all()
        else:
            memberlist = self.session.query(User).filter(User.ugrade == degree).filter(User.ucheck == True).all()
        self.render('home_members.html', memberlist = memberlist, mtype = mtype, degree = degree)
        self.session.close()

class ListArticles(StaticBase):
    def get(self):
        StaticBase.init(self)
        self.title = 'Articles'
        targetpage = int(self.get_argument('page',default='1'))
        articlelist = []
        for one in self.session.query(Article).order_by(Article.apubtime).all():
            articlelist.insert(0, ArticleListObject(one))
        alist, self.pagination = generatePagination('/articles?page=', articlelist, targetpage)
        self.render('home_alist.html', list = alist, thisquery=None)
        self.session.close()

class ShowArticles(StaticBase):
    def get(self, id):
        StaticBase.init(self)
        one = self.session.query(Article).filter(Article.aid == id).first()
        self.title = one.atitle
        article = ArticleListObject(one)
        self.render('home_showarticle.html', article = article)
        self.session.close()

class ShowAbout(homeBase):
    def get(self):
        homeBase.init(self)
        self.title = 'About us'
        info_path = os.path.join(self.get_template_path(), 'aboutme.md')
        aboutcontent = markdown.markdown(open(info_path).read().decode('utf8'))
        self.render('home_about.html', aboutcontent = aboutcontent)
        self.session.close()

class ShowContact(homeBase):
    def get(self):
        homeBase.init(self)
        self.title = 'Contact us'
        self.render('home_contact.html')
        self.session.close()

    def post(self):
        homeBase.init(self)
        cname = self.get_argument('cname', default='')
        ccollege = self.get_argument('ccollege', default='')
        ccemail = self.get_argument('ccemail', default='')
        creason = self.get_argument('creason', default='')
        contact = Contact(cname, ccollege, ccemail, creason)
        if 'file' in self.request.files:
            file_dict_list = self.request.files['file']
            for file_dict in file_dict_list:
                filename = nameRewrite(file_dict["filename"]).encode('utf8')
                data = file_dict["body"]
                with open(resume_path + filename, 'w') as f:
                    f.write(data)
                    print filename
            contact.cresume = '/static/resume/' + filename
        self.session.add(contact)
        self.session.commit()
        self.write('<script language="javascript">alert("提交成功");self.location="/";</script>')
        self.session.close()

class ShowMyPage(homeBase):
    def get(self, uid):
        homeBase.init(self)
        user = self.session.query(User).filter(User.uid == uid).first()
        articlelist = []
        for article in user.article:
            articlelist.insert(0, ArticleListObject(article))
        self.title = user.username
        self.render('home_pagehome.html', user = user, articlelist = articlelist)
        self.session.close()

class EditArticle(homeBase):
    @tornado.web.authenticated
    def get(self, uid):
        homeBase.init(self)
        aid = self.get_argument('aid',default=None)
        user = self.session.query(User).filter(User.uid == uid).first()
        self.title = 'Edit Article'
        typelist = self.session.query(Type).all()
        if aid == None:
            article = Article('','','','')
            article.aid = None
        else:
            article = self.session.query(Article).filter(Article.aid == aid).first()
        self.render('home_writepage.html', typelist = typelist, uid = uid, user = user, article = article)
        self.session.close()

    def post(self, uid):
        homeBase.init(self)
        self.title = 'Edit Article'
        atitle = self.get_argument('atitle', default='')
        acontent = self.get_argument('acontent', default='')
        taid = self.get_argument('optionsRadios', default='')
        aid = self.get_argument('aid', default='None')
        if aid == 'None':
            article = Article(atitle, acontent, uid, taid)
            self.session.add(article)
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/members/m/%s"</script>'% str(uid))
        else:
            article = self.session.query(Article).filter(Article.aid == aid).first()
            article.atitle = atitle
            article.acontent = acontent
            article.taid = taid
            article.achgtime = datetime.now()
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/members/m/%s"</script>'% str(uid))
        self.session.close()

class DeleteArticle(homeBase):
    @tornado.web.authenticated
    def get(self, uid):
        homeBase.init(self)
        aid = self.get_argument("aid", default=None)
        self.session.query(Article).filter(Article.aid == aid).delete()
        self.session.commit()
        self.redirect('/members/m/%s' % str(uid))
        self.session.close()

class EditProfile(homeBase):
    @tornado.web.authenticated
    def get(self, id):
        homeBase.init(self)
        user = self.session.query(User).filter(User.uid == id).first()
        self.title = 'Edit Profile'
        self.render('home_profile.html', id = id, user = user)
        self.session.close()

    @tornado.web.authenticated
    def post(self, id):
        homeBase.init(self)
        self.title = 'Edit Profile'
        ucollege = self.get_argument('ucollege', default='')
        ugrade = self.get_argument('ugrade', default='')
        udomain = self.get_argument('udomain', default='')
        ubio = self.get_argument('ubio', default='')
        user = self.session.query(User).filter(User.username == self.signeduser).first()
        user.ucollege = ucollege
        user.ugrade = ugrade
        user.udomain = udomain
        user.ubio = ubio
        print user.uavatar
        print ubio, ugrade, ucollege
        if 'file' in self.request.files:
            file_dict_list = self.request.files['file']
            for file_dict in file_dict_list:
                filename = nameRewrite(file_dict["filename"]).encode('utf8')
                data = file_dict["body"]
                image = Image.open(StringIO(data))
                image.save(avatar_path + filename, quality=150)
                '''
                with open(avatar_path + filename, 'w') as f:
                    f.write(data)
                    print filename'''
            user.uavatar = '/static/avatar/' + filename
        else:
            if user.uavatar == '':
                user.uavatar = '/static/images/' + 'avatar-'+ str(random.randint(1,16)) +'.svg'
                print user.uavatar
        self.session.commit()
        self.write('<script language="javascript">alert("OK,Entering your own homepage!!");self.location="/members/m/%s";</script>' % str(self.signedid))
        self.session.close()

class ListByDate(StaticBase):
    def get(self,year,month):
        StaticBase.init(self)
        targetpage = int(self.get_argument('page',default='1'))
        articlelist = [ArticleListObject(article) for article in self.session.query(Article).all() if article.apubtime.year == int(year) and article.apubtime.month == int(month)]

        list, self.pagination = generatePagination('/q/date/' + year + '/' + month + '?page=', articlelist, targetpage)

        self.title = "归档：" + str(year) + "年" + str(month) + "月"
        self.render("home_alist.html", list = list, thisquery = "归档：" + str(year) + "年" + str(month) + "月" )
        self.session.close()

class ListByType(StaticBase):
    def get(self, typename):
        StaticBase.init(self)
        targetpage = int(self.get_argument('page',default='1'))
        print typename
        tid = self.session.query(Type).filter(Type.typename == str(typename)).first().tid
        print tid
        articlelist = [ArticleListObject(article) for article in self.session.query(Article).filter(Article.taid == tid).all()]

        list, self.pagination = generatePagination('/type/'+typename+'?page=', articlelist, targetpage)

        self.title = "Type：" + str(typename)
        self.render("home_alist.html", list = list, thisquery = "Type：" + str(typename))
        self.session.close()

class ListDownload(StaticBase):
    def get(self):
        StaticBase.init(self)
        self.title = 'Download'
        targetpage = int(self.get_argument('upload',default='1'))
        uploadList = []
        for one in self.session.query(Upload).all():
            uploadList.insert(0, UploadListObject(one))
        uploadList, self.pagination = generatePagination('/download?upload=', uploadList, targetpage)
        self.render('home_download.html', list = uploadList)
        self.session.close()

class ShowSinglePage(StaticBase):
    def get(self, pagename):
        StaticBase.init(self)
        self.title = pagename
        tid = self.session.query(Type).filter(Type.typename == pagename).first().tid
        article = ArticleListObject(self.session.query(Article).filter(Article.taid == tid).first())
        self.render('home_showarticle.html', article = article)