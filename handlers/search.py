#! /usr/bin/env python
#coding:utf-8

from handlers.home import StaticBase, generatePagination
from handlers.generateObject import ArticleListObject
from models.entity import Article
import tornado.web

class ListSearch(StaticBase):
    def get(self):
        StaticBase.init(self)
        targetpage = int(self.get_argument('page',default='1'))
        keyword = self.get_argument('keyword',default='')
        articles = []
        for article in self.session.query(Article).all():
            if keyword in article.atitle or keyword in article.acontent:
                articles.insert(0, article)

        articlelist = [ArticleListObject(article) for article in articles]

        list, self.pagination = generatePagination('/search?keyword=' + keyword + '&page=', articlelist, targetpage)

        self.title = "搜索：" + keyword.encode('utf8')
        self.render("home_alist.html", list = list, thisquery = "搜索：" + keyword.encode('utf8') )
