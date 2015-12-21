#! /usr/bin/env python
#coding=utf-8

import functools
import tornado.web
from models.entity import User
from models.entity import db_session

class SignValidateBase(tornado.web.RequestHandler):
   def get_current_user(self):
      return self.get_secure_cookie('username')

def adminLimit(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.session = db_session.getSession
        self.signeduser = SignValidateBase.get_current_user(self)
        if self.session.query(User).filter(User.username == self.signeduser).first().luid == 1:
            self.write('<script language="javascript">alert("你不适合这里！！");self.location="/signin";</script>')
        return method(self, *args, **kwargs)
    return wrapper