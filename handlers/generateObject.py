#! /usr/bin/env python
#coding=utf-8

class ArticleListObject(object):
    def __init__(self, article):
        self.id = article.aid
        self.title = article.atitle
        self.subcontent = article.acontent[:300]
        self.content = article.acontent
        self.type = article.atype.typename
        self.typelink = '/type/'+self.type
        self.pubtime = article.apubtime.date()
        self.chgtime = article.achgtime.date()
        self.user = article.auser.username
        self.useravatar = article.auser.uavatar
        self.userlink = '/members/m/' + str(article.auser.uid)

class PageListObject(object):
    def __init__(self, page):
        self.pid = page.pid
        self.ptitle = page.ptitle
        self.pcontent = page.pcontent
        self.ppubtime = page.ppubtime.date()
        self.pchgtime = page.pchgtime.date()
        self.ppic = page.ppic

class NewsListObject(object):
    def __init__(self, news):
        self.nid = news.nid
        self.ntitle = news.ntitle
        self.ncontent = news.ncontent
        self.npubtime = news.npubtime.date()
        self.nchgtime = news.nchgtime.date()

class UploadListObject(object):
    def __init__(self, upload):
        self.fileid = upload.fileid
        self.filename = upload.filename
        self.cettime = upload.cettime.date()
        self.fileurl = upload.fileurl

class MeetinfoObject(object):
    def __init__(self, meetinfo):
        self.mid = meetinfo.mid
        self.mtitle = meetinfo.mtitle
        self.mcontent = meetinfo.mcontent
        self.mcettime = meetinfo.mcettime.date()

class InformObject(object):
    def __init__(self, inform):
        self.iid = inform.iid
        self.ititle = inform.ititle
        self.iabstract = inform.iabstract
        self.iurl = inform.iurl
        self.ipic = inform.ipic
        self.icettime = inform.icettime.date()
        self.ibtnview = inform.ibtnview
