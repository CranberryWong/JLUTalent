#! /usr/bin/env python
#coding=utf-8

import os
import tornado.web
from handlers import admin, home, upload, exception, mail, search

SETTINGS = dict(
   debug = True,
   template_path = os.path.join(os.path.dirname(__file__),"templates"),
   static_path = os.path.join(os.path.dirname(__file__),"static"),
   cookie_secret = "dEr2Viz6TrqsoQVbQCRdxUmzKB5q40U0jYtp+fnsAOY=",
   login_url = "/signin",
   autoescape = None,
)

homeurls = [

   #前台
   (r"/",home.Home),
   (r"/changelang",home.changeLang),
   (r"/news",home.ListNews),
   (r"/projects",home.ListProjects),
   (r"/articles",home.ListArticles),
   (r"/members",home.ListMembers),
   (r"/download",home.ListDownload),
   (r"/about",home.ShowAbout),
   (r"/contact",home.ShowContact),
   (r"/upload?",upload.ImageUpload),
   (r"/news/n/([0-9]+)",home.ShowNews),
   (r"/projects/p/([0-9]+)",home.ShowProjects),
   (r"/articles/a/([0-9]+)",home.ShowArticles),
   (r"/members/m/([0-9]+)",home.ShowMyPage),
   (r'/q/date/([0-9]+)/([0-9]+)',home.ListByDate),
   (r'/type/([0-9a-zA-Z]*)', home.ListByType),
   (r'/search', search.ListSearch),
   (r'/single/([0-9a-zA-Z]*)', home.ShowSinglePage),
   #(r"/type/([0-9a-zA-Z]*)",home.ShowAbout),

   (r"/members/m/([0-9]+)/write",home.EditArticle),
   (r"/members/m/([0-9]+)/delete",home.DeleteArticle),
   (r"/members/m/([0-9]+)/profile",home.EditProfile),
   #(r"/members/m/([0-9]+)/setting/",admin.EditProfile),

   #后台
   (r"/signin",admin.Signin),
   (r"/signup",admin.Signup),
   (r"/signout",admin.Signout),
   (r"/admin",admin.AdminHome),
   (r"/admin/deluser",admin.DelUser),
   (r"/admin/deltype",admin.DelType),
   (r"/admin/editpage",admin.EditPage),
   (r"/admin/delpage",admin.DelPage),
   (r"/admin/editarticle",admin.EditArticle),
   (r"/admin/delarticle",admin.DelArticle),
   (r"/admin/limits",admin.EditLimits),
   (r"/admin/reports",admin.ListReports),
   (r"/admin/delreports",admin.DelReports),
   (r"/admin/slide",admin.SlideOption),
   (r"/admin/delslide",admin.DelSlide),
   (r"/admin/link",admin.LinkOption),
   (r"/admin/dellink",admin.DelLink),
   (r"/admin/meetinfo",admin.MeetinfoOption),
   (r"/admin/delmeetinfo",admin.DelMeetinfo),
   (r"/admin/changechecked",admin.ChangeChecked),
   (r"/admin/changelimit",admin.ChangeLimit),
   (r"/admin/download",admin.DownloadOption),
   (r"/admin/deldownload",admin.DelDownload),

   (r"/admin/settings",admin.SettingsOption),

   (r"/admin/translate",admin.TranslateOption),
   
   (r"/admin/mail",mail.MailSending),


   #cache
   (r"/(favicon\.ico)", tornado.web.StaticFileHandler, dict(path=SETTINGS['static_path'])),

   #exception
   (r".*", exception.ErrorHandler)
]
