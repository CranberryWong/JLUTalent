#! /usr/bin/env python
#coding:utf-8

import tornado.web
import time
import os
import markdown
from models.entity import User, Article, Type, Page, Contact, Upload, Inform, Limits, Links, Meetinfo
from models.entity import db_session
from handlers.settings import SITESETTINGS
from handlers.generateObject import ArticleListObject, PageListObject, MeetinfoObject, InformObject, UploadListObject
import hashlib
import json
import random
from datetime import datetime
from PIL import Image
from handlers.util import adminLimit
from handlers.util import SignValidateBase
from cStringIO import StringIO

page_path = os.path.join(os.path.abspath('.'), 'static/page/')
inform_path = os.path.join(os.path.abspath('.'), 'static/inform/')
addon_path = os.path.join(os.path.abspath('.'), 'static/addon/')

def nameRewrite(filename):
    file_timestamp = int(time.time())
    name_split = filename.split('.')
    if len(name_split) == 1:
        filename = filename + str(file_timestamp)
    else:
        filename = name_split[0] + str(file_timestamp) + '.' + name_split[1]
    return filename

class StaticData(SignValidateBase):
   @adminLimit
   def init(self):
      self.sitename = SITESETTINGS['site_name']
      self.siteversion = SITESETTINGS['site_version']
      if self.signeduser:
            self.user = self.session.query(User).filter(User.username == self.signeduser).first()
            self.signedid = self.user.uid
            self.signavatar = self.user.uavatar
      else: 
            self.signedid = None

      

class Signin(SignValidateBase):
   def get(self):
      self.title = 'Sign in'
      self.render('signin.html')

   def post(self):
      self.session = db_session.getSession
      username = self.get_argument('username', default='')
      password = self.get_argument('password', default='')
      md5_psw = hashlib.md5(password).hexdigest()
      user = self.session.query(User).filter(User.username==username).one()
      uname = user.username
      psw = user.password
      if username == uname and md5_psw == psw:
          if user.ucheck == True:
              self.set_secure_cookie('username', username)
              self.redirect('/admin')
          else:
              self.write('<script language="javascript">alert("对不起，账户需管理员确认后方能生效");self.location="/signin";</script>')
      else:
         self.write('<script language="javascript">alert("用户名或密码错误");self.location="/signin";</script>')
      self.session.close()

class Signout(SignValidateBase):
   def get(self):
      self.clear_cookie('username')
      self.redirect('/')

class Signup(SignValidateBase):
   def get(self):
      self.title = 'Sign Up'
      self.render('signup.html')

   def post(self):
      self.session = db_session.getSession
      username = self.get_argument('username', default='')
      password = self.get_argument('password', default='')
      passvali = self.get_argument('passvali', default='')
      uemail = self.get_argument('email', default='')
      if password == passvali:
          uname = self.session.query(User).filter(User.username==username).first()
          if uname != None:
              self.write('<script language="javascript">alert("用户名已被占用");self.location="/signup";</script>')
          else:
              psw = hashlib.md5(password).hexdigest()
              newuser = User(username,psw,uemail)
              self.session.add(newuser)
              newuser.uavatar = '/static/images/' + 'avatar-'+ str(random.randint(1,16)) +'.svg'
              self.session.commit()
              self.set_secure_cookie('username', username)
              self.write('<script language="javascript">alert("注册成功");self.location="/signin";</script>')
      else:
          self.write('<script language="javascript">alert("密码不匹配");self.location="/signup";</script>')
      self.session.close()

class AdminHome(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Dashboard'
        articlelist = []
        pagelist = []
        userlist = self.session.query(User).all()
        aarticlelist = self.session.query(Article).all()
        for one in aarticlelist:
            articlelist.insert(0, ArticleListObject(one))
        ppagelist = self.session.query(Page).all()
        for one in ppagelist:
            pagelist.insert(0, PageListObject(one))
        typelist = self.session.query(Type).all()
        tid = self.get_argument('tid', default=None)
        if tid == None:
            typeobj = Type('')
            typeobj.tid = None
        else:
            typeobj = self.session.query(Type).filter(Type.tid == tid).first()
        self.render('admin_overview.html', userlist = userlist, articlelist = articlelist, pagelist = pagelist, typelist = typelist, typeobj = typeobj)
        self.session.close()

    def post(self):
        StaticData.init(self)
        tid = self.get_argument('tid', default='None')
        typename = self.get_argument('typename', default='')
        if tid == 'None':
            typeobj = Type(typename)
            self.session.add(typeobj)
            self.session.commit()
        else:
            typeobj = self.session.query(Type).filter(Type.tid == tid).first()
            typeobj.typename = typename
            self.session.commit()
        self.redirect('/admin#dropdown2-tab')
        self.session.close()

##################  删除用户  ##################

class DelUser(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        uid = self.get_argument('uid', default=None)
        print uid, type(uid)
        self.session.query(Article).filter(Article.uaid == uid).delete()
        self.session.query(User).filter(User.uid == uid).delete()
        self.session.commit()
        self.redirect('/admin#home')
        self.session.close()
            
###############################################

class EditPage(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Dashboard Page Edit'
        pid = self.get_argument('pid', default=None)
        if pid == None:
            page = Page('','')
            page.pid = None
        else:
            page = self.session.query(Page).filter(Page.pid == pid).first()
        self.render('admin_editpage.html', active2 = 'class="active"', page = page)
        self.session.close()

    def post(self):
        self.title = 'Dashboard Page Edit'
        StaticData.init(self)
        pid = self.get_argument('pid', default='None')
        print pid, type(pid)
        ptitle = self.get_argument('ptitle', default='')
        pcontent = self.get_argument('pcontent', default='')
        if pid == 'None':
            page = Page(ptitle, pcontent)
            if 'file' in self.request.files:
                file_dict_list = self.request.files['file']
                for file_dict in file_dict_list:
                    filename = nameRewrite(file_dict["filename"]).encode('utf8')
                    data = file_dict["body"]
                    image = Image.open(StringIO(data))
                    image.save(page_path + filename, quality=150)
                    '''
                    with open(page_path + filename, 'w') as f:
                        f.write(data)
                        print filename'''
                    page.ppic = '/static/page/' + filename
            self.session.add(page)
            self.session.commit()
        else:
            page = self.session.query(Page).filter(Page.pid == pid).first()
            page.ptitle = ptitle
            page.pcontent = pcontent
            if 'file' in self.request.files:
                file_dict_list = self.request.files['file']
                for file_dict in file_dict_list:
                    filename = nameRewrite(file_dict["filename"]).encode('utf8')
                    if page.ppic[:len(filename)-10] != '/static/page/' + filename[:len(filename)-10]:
                        print page.ppic[:len(filename)-10],'/static/page/' + filename[:len(filename)-10]
                        data = file_dict["body"]
                        image = Image.open(StringIO(data))
                        image.save(avatar_path + filename, quality=150)
                        page.ppic = '/static/page/' + filename
            page.pchgtime = datetime.now()
            self.session.commit()
        self.write('<script language="javascript">alert("提交成功");self.location="/admin/editpage"</script>')
        self.session.close()

class DelPage(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        pid = self.get_argument('pid', default=None)
        self.session.query(Page).filter(Page.pid == pid).delete()
        self.session.commit()
        self.redirect('/admin')
        self.session.close()
        
class EditArticle(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Dashboard Article Edit'
        aid = self.get_argument('aid',default=None)
        typelist = self.session.query(Type).all()
        specialtype = self.session.query(Type).filter(Type.typename == 'Group' or Type.typename == 'Policy').all()
        if aid == None:
            article = Article('','','','')
            article.aid = None
        else:
            article = self.session.query(Article).filter(Article.aid == aid).first()
        self.render('admin_editarticle.html', active9 = 'class="active"', typelist = typelist, uid = self.signedid, user = self.user, article = article)
        self.session.close()

    def post(self):
        self.title = 'Dashboard Article Edit'
        StaticData.init(self)
        atitle = self.get_argument('atitle', default='')
        acontent = self.get_argument('acontent', default='')
        taid = self.get_argument('atype', default='')
        aid = self.get_argument('aid', default='None')
        if aid == 'None':
            article = Article(atitle, acontent, self.signedid, taid)
            self.session.add(article)
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/admin/editarticle"</script>')
        else:
            article = self.session.query(Article).filter(Article.aid == aid).first()
            article.atitle = atitle
            article.acontent = acontent
            article.taid = taid
            article.achgtime = datetime.now()
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/members/m/%s"</script>'% str(uid))
        self.session.close()

class DelArticle(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        aid = self.get_argument("aid", default=None)
        self.session.query(Article).filter(Article.aid == aid).delete()
        self.session.commit()
        self.redirect('/admin')
        self.session.close()

class EditLimits(StaticData):
    @tornado.web.authenticated
    def get(self):
        self.title = 'Dashboard Limits'
        StaticData.init(self)
        limitlist = self.session.query(Limits).all()
        userlist = self.session.query(User).order_by(User.uid.desc()).all()
        self.render('admin_limits.html', userlist = userlist, limitlist = limitlist)
        self.session.close()

class ChangeChecked(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        uid = self.get_argument('uid')
        uchecked = self.get_argument('ucheck')
        print uid, uchecked, type(uchecked)
        if uchecked == 'False':
            uchecked = False
        else:
            uchecked = True
        user = self.session.query(User).filter(User.uid == uid).first()
        print user.username
        user.ucheck = not uchecked
        print user.ucheck
        self.session.commit()
        self.redirect('/admin/limits')
        self.session.close()

class ChangeLimit(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        uid = self.get_argument('uid', default=None)
        luid = self.get_argument('lid', default=None)
        user = self.session.query(User).filter(User.uid == uid).first()
        if self.session.query(User).filter(User.username == self.signeduser).first().luid == 3:
            user.luid = luid
            self.session.commit()
            self.redirect('/admin/limits')
        else:
            self.write('<script language="javascript">alert("你并没有权限");self.location="/admin/limits"</script>')
        self.session.close()

class ListReports(StaticData):
    @tornado.web.authenticated
    def get(self):
        self.title = 'Dashboard Reports'
        StaticData.init(self)
        contactlist = self.session.query(Contact).all()
        self.render('admin_reports.html', contactlist = contactlist)
        self.session.close()

class DelReports(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        cid = self.get_argument('cid',default=None)
        self.session.query(Contact).filter(Contact.cid == cid).delete()
        self.session.commit()
        self.redirect('/admin/reports')
        self.session.close()


class SlideOption(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Slide Option'
        iid = self.get_argument('iid', default=None)
        informs = []
        inform = self.session.query(Inform).all()
        for one in inform:
            informs.insert(0, InformObject(one))
        if iid == None:
            informobj = Inform('','')
            informobj.iid = None
        else:
            informobj = self.session.query(Inform).filter(Inform.iid == iid).first()
        self.render("admin_slide.html", informs = informs, informobj = informobj)
        self.session.close()

    def post(self):
        StaticData.init(self)
        self.title = 'Slide Option'
        iid = self.get_argument('iid', default='None')
        ititle = self.get_argument('ititle', default='')
        iabstract = self.get_argument('iabstract', default='')
        iurl = self.get_argument('iurl', default='')
        ibtnview = self.get_argument('ibtnview', default='View Detail')
        if iid == 'None':
            inform = Inform(ititle, iabstract)
            inform.iurl = iurl
            inform.itynview = ibtnview
            if 'file' in self.request.files:
                file_dict_list = self.request.files['file']
                for file_dict in file_dict_list:
                    filename = nameRewrite(file_dict["filename"]).encode('utf8')
                    data = file_dict["body"]
                    image = Image.open(StringIO(data))
                    image.save(inform_path + filename, quality=150)
                    '''
                    with open(inform_path + filename, 'w') as f:
                        f.write(data)
                        print filename'''
                    inform.ipic = '/static/inform/' + filename
            self.session.add(inform)
            self.session.commit()
        else:
            slide = self.session.query(Inform).filter(Inform.iid == iid).first()
            slide.ititle = ititle
            slide.iabstract = iabstract
            slide.iurl = iurl
            slide.ibtnview = ibtnview
            if 'file' in self.request.files:
                file_dict_list = self.request.files['file']
                for file_dict in file_dict_list:
                    filename = nameRewrite(file_dict["filename"]).encode('utf8')
                    if slide.iurl[:len(filename)-10] != '/static/inform/' + filename[:len(filename)-10]:
                        print inform.iurl[:len(filename)-10], '/static/inform/' + filename[:len(filename)-10]
                        data = file_dict["body"]
                        image = Image.open(StringIO(data))
                        image.save(inform_path + filename, quality=150)
                        '''
                        with open(inform_path + filename, 'w') as f:
                            f.write(data)
                            print filename'''
                        slide.iurl = '/static/inform/' + filename
            self.session.commit()
        self.write('<script language="javascript">alert("提交成功");self.location="/admin";</script>')
        self.session.close()

class DelSlide(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        iid = self.get_argument('iid', default=None)
        self.session.query(Inform).filter(Inform.iid == iid).delete()
        self.session.commit()
        self.redirect('/admin/slide')

class LinkOption(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Link Option'
        lkid = self.get_argument('lkid', default=None)
        links = self.session.query(Links).all()
        if lkid == None:
            linkobj = Links('','')
            linkobj.lkid = None
        else:
            linkobj = self.session.query(Links).filter(Links.lkid == lkid).first()
        self.render('admin_link.html', links = links, linkobj = linkobj)
        self.session.close()

    def post(self):
        StaticData.init(self)
        self.title = 'Link Option'
        lkid = self.get_argument('lkid', default='None')
        lkname = self.get_argument('lkname', default='')
        lkurl = self.get_argument('lkurl', default='')
        lkdescribe = self.get_argument('lkdescribe', default='')
        if lkid == 'None':
            link = Links(lkname, lkurl)
            link.lkdescribe = lkdescribe
            self.session.add(link)
            self.session.commit()
        else:
            link = self.session.query(Links).filter(Links.lkid == lkid).first()
            link.lkname = lkname
            link.lkurl = lkurl
            link.lkdescribe = lkdescribe
            self.session.commit()
        self.write('<script language="javascript">alert("提交成功");self.location="/admin/link";</script>')
        self.session.close()

class DelLink(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        lkid = self.get_argument('lkid', default=None)
        self.session.query(Links).filter(Links.lkid == lkid).delete()
        self.session.commit()
        self.redirect('/admin/link')
        self.session.close()

class MeetinfoOption(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Meetinfo Option'
        meetinfos =[]
        meetinfo = self.session.query(Meetinfo).all()
        for one in meetinfo:
            meetinfos.insert(0, MeetinfoObject(one))
        mid = self.get_argument('mid', default=None)
        if mid == None:
            meetinfoobj = Meetinfo('','')
            meetinfoobj.mid = None
        else:
            meetinfoobj = self.session.query(Meetinfo).filter(Meetinfo.mid == mid).first()
        self.render('admin_meetinfo.html', meetinfos = meetinfos, meetinfoobj = meetinfoobj)
        self.session.close()

    def post(self):
        StaticData.init(self)
        self.title = 'Meetinfo Option'
        mtitle = self.get_argument('mtitle', default='')
        mcontent = self.get_argument('mcontent', default='')
        mid = self.get_argument('mid', default='None')
        if mid == 'None':
            meetinfo = Meetinfo(mtitle, mcontent)
            self.session.add(meetinfo)
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/admin/meetinfo";</script>')
        else:
            meetinfo = self.session.query(Meetinfo).filter(Meetinfo.mid == mid).first()
            meetinfo.mtitle = mtitle
            meetinfo.mcontent = mcontent
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/admin/meetinfo";</script>')
        self.session.close()

class DelMeetinfo(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        mid = self.get_argument('mid', default=None)
        self.session.query(Meetinfo).filter(Meetinfo.mid == mid).delete()
        self.session.commit()
        self.redirect('/admin/meetinfo')
        self.session.close()

class DelType(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        tid = self.get_argument('tid', default=None)
        self.session.query(Type).filter(Type.tid == tid).delete()
        self.session.commit()
        self.redirect('/admin#nav-type')
        self.session.close()

class AdminStatistic():
    pass

class SettingsOption(StaticData):
    @tornado.web.authenticated
    def get(self):
        self.title = 'Settings'
        StaticData.init(self)
        info_path = os.path.join(self.get_template_path(), 'aboutme.md')
        aboutcontent = open(info_path).read().decode('utf8')
        self.render('admin_settings.html', aboutcontent = aboutcontent)
        self.session.close()

    def post(self):
        sitename = self.get_argument('sitename', default='')
        siteversion = self.get_argument('siteversion', default='')
        SITESETTINGS['site_name'] = sitename
        SITESETTINGS['site_version'] = siteversion
        info_path = os.path.join(self.get_template_path(), 'aboutme.md')
        aboutcontent = self.get_argument('siteabout', default='')
        with open(info_path, 'w') as f:
            f.write(aboutcontent.encode('utf8'))
        self.write('<script language="javascript">alert("提交成功");self.location="/admin";</script>')

class DownloadOption(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = 'Download Option'
        uploadList = []
        for one in self.session.query(Upload).all():
            uploadList.insert(0, UploadListObject(one))
        self.render('admin_download.html', list = uploadList)
        self.session.close()

    def post(self):
        StaticData.init(self)
        #upload_path = os.path.join(os.path.dirname(__file__),"static"),
        if 'file' in self.request.files:
            file_dict_list = self.request.files['file']
            for file_dict in file_dict_list:
                filename = file_dict["filename"].encode('utf8')
                data = file_dict["body"]
                with open(addon_path + filename, 'w') as f:
                    f.write(data)
            self.session.add(Upload(filename, '/static/addon/'+filename))
            self.session.commit()
            self.write('<script language="javascript">alert("提交成功");self.location="/admin/download"</script>')
            self.session.close()

class DelDownload(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        fileid = self.get_argument('fileid', default=None)
        self.session.query(Upload).filter(Upload.fileid == fileid).delete()
        self.session.commit()
        self.redirect('/admin/download')
        self.session.close()

##################  翻译模块  ##################

class TranslateOption(StaticData):
    translate_path = os.path.join(os.path.join(os.path.abspath('.'), 'csv_translations/zh_CN.csv'))
    @tornado.web.authenticated
    def get(self):
        self.title = 'Translate'
        StaticData.init(self)
        translateCSV = open(self.translate_path).read().decode('utf8')
        self.render('admin_translate.html', translateCSV = translateCSV)
        self.session.close()

    def post(self):
        translateCSV = self.get_argument('translate', default='')
        with open(self.translate_path, 'w') as f:
            f.write(translateCSV.encode('utf8'))
        self.write('<script language="javascript">alert("提交成功");self.location="/admin/translate";</script>')
        
###############################################