#! /usr/bin/env python
#coding=utf-8

from urls import homeurls, SETTINGS

import tornado.web

app = tornado.web.Application(
   handlers = homeurls,
   **SETTINGS
)
