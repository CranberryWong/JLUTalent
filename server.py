#! /usr/bin/env python
#coding=utf-8

import tornado.ioloop
import sys
import os

from application import app

PORT = 8080

if __name__ == '__main__':
   #if len(sys.argv) > 1:
   #   PORT = sys.argv[1]
   tornado.locale.load_translations(os.path.join(os.path.dirname(__file__), "csv_translations"))
   
   app.listen(PORT)
   print 'Development server is running at http://127.0.0.1:%s/' % PORT
   print 'Quit the server with Ctrl-C'
   tornado.ioloop.IOLoop.instance().start()
