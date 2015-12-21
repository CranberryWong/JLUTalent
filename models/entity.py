#! /usr/bin/env python
#coding:utf-8

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from settings import DBSETTINGS
from datetime import datetime

Base = declarative_base()

class User(Base):
   __tablename__ = 'users'

   uid = Column(Integer, primary_key=True)
   username = Column(String(35))
   password = Column(String(35))
   uemail = Column(String(30))
   ubio = Column(Text)
   ucheck = Column(Boolean)
   ucollege = Column(String(30))
   ugrade = Column(String(10))
   udomain = Column(Text)
   uavatar = Column(String(100))
   luid = Column(Integer, ForeignKey('limits.lid'))

   ulevel = relationship('Limits', backref='user')

   def __init__(self, username, password, uemail):
      self.username = username
      self.password = password
      self.uemail = uemail
      self.ubio = ''
      self.ucheck = False
      self.ucollege = ''
      self.ugrade = ''
      self.udomain = ''
      self.uavatar = ''
      self.luid = 1

   def __repr__(self):
      return "<User('%s')>" % (self.username)

class Article(Base):
    __tablename__ = 'articles'

    aid = Column(Integer, primary_key=True)
    atitle = Column(String(60), nullable=False)
    acontent = Column(Text)
    apubtime = Column(DateTime, nullable=False)
    achgtime = Column(DateTime, nullable=False)
    uaid = Column(Integer, ForeignKey('users.uid'))
    taid = Column(Integer, ForeignKey('types.tid'))

    auser = relationship('User', backref='article')
    atype = relationship('Type', backref='article')

    def __init__(self, atitle, acontent, uaid, taid):
        self.atitle = atitle
        self.acontent = acontent
        self.apubtime = datetime.now()
        self.achgtime = datetime.now()
        self.uaid = uaid
        self.taid = taid

    def __repr__(self):
        return "<Article('%s')>" % (self.atitle)

class Type(Base):
    __tablename__ = 'types'

    tid = Column(Integer, primary_key=True)
    typename = Column(String(10), nullable=False)

    typeofa = relationship('Article')

    def __init__(self, typename):
        self.typename = typename

    def __repr__(self):
        return "<Type('%s')>" % (self.typename)

class Page(Base):
    __tablename__ = 'pages'

    pid = Column(Integer, primary_key=True)
    ptitle = Column(String(60), nullable=False)
    pcontent = Column(Text)
    ppubtime = Column(DateTime, nullable=False)
    pchgtime = Column(DateTime, nullable=False)
    ppic = Column(String(100))

    def __init__(self, ptitle, pcontent):
        self.ptitle = ptitle
        self.pcontent = pcontent
        self.ppubtime = datetime.now()
        self.pchgtime = datetime.now()

    def __repr__(self):
        return "<Page('%s')>" % (self.ptitle)

class News(Base):
    __tablename__ = 'news'

    nid = Column(Integer, primary_key=True)
    ntitle = Column(String(60), nullable=False)
    ncontent = Column(Text)
    npubtime = Column(DateTime, nullable=False)
    nchgtime = Column(DateTime, nullable=False)

    def __init__(self, ntitle, ncontent):
        self.ntitle = ntitle
        self.ncontent = ncontent
        self.npubtime = datetime.now()
        self.nchgtime = datetime.now()

    def __repr__(self):
        return "<News('%s')>" % (self.ntitle)

class Contact(Base):
    __tablename__ = 'contacts'

    cid = Column(Integer, primary_key=True)
    cname = Column(String(35), nullable=False)
    ccollege = Column(String(30), nullable=False)
    ccemail = Column(String(30), nullable=False)
    creason = Column(Text)
    cresume = Column(String(100))

    def __init__(self, cname, ccollege, ccemail, creason):
        self.cname = cname
        self.ccollege = ccollege
        self.ccemail = ccemail
        self.creason = creason
        self.cresume = ''

    def __repr__(self):
        return "<Contact('%s')>" % (self.cname)

class Inform(Base):
    __tablename__ = 'inform'

    iid = Column(Integer, primary_key=True)
    ititle = Column(String(60), nullable=False)
    iabstract = Column(String(200), nullable=False)
    iurl = Column(String(100))
    ipic = Column(String(100))
    icettime = Column(DateTime, nullable=False)
    ibtnview = Column(String(25))

    def __init__(self, ititle, iabstract):
        self.ititle = ititle
        self.iabstract = iabstract
        self.iurl = ''
        self.ipic = ''
        self.icettime = datetime.now()
        self.ibtnview = 'View Detail'

    def __repr__(self):
        return "<Inform('%s')>" % (self.ititle)

class Upload(Base):
    __tablename__ = 'upload'

    fileid = Column(Integer, primary_key=True)
    filename = Column(String(50), nullable=False)
    cettime = Column(DateTime, nullable=False)
    fileurl = Column(String(100), nullable=False)

    def __init__(self, filename, fileurl):
        self.filename = filename
        self.cettime = datetime.now()
        self.fileurl = fileurl

    def __repr__(self):
        return "<Upload('%s')>" % (self.filename)

class Limits(Base):
    __tablename__ = 'limits'

    lid = Column(Integer, primary_key=True)
    lname = Column(String(20), nullable=False)
    lsuper = Column(Boolean, nullable=False)
    ladmin = Column(Boolean, nullable=False)

    def __init__(self, lname, lsuper, ladmin):
        self.lname = lname
        self.lsuper = lsuper
        self.ladmin = ladmin

    def __repr__(self):
        return "<Limits('%s')>" % (self.lname)

class Links(Base):
    __tablename__ = 'links'

    lkid = Column(Integer, primary_key=True)
    lkname = Column(String(30), nullable=False)
    lkurl = Column(String(100), nullable=False)
    lkdescribe = Column(Text)

    def __init__(self, lkname, lkurl):
        self.lkname = lkname
        self.lkurl = lkurl
        self.lkdescribe = ''

    def __repr__(self):
        return "<Links('%s')>" % (self.lkname)

class Meetinfo(Base):
    __tablename__ = 'meetinfo'

    mid = Column(Integer, primary_key=True)
    mtitle = Column(String(30), nullable=False)
    mcontent = Column(Text)
    mcettime = Column(DateTime)

    def __init__(self, mtitle, mcontent):
        self.mtitle = mtitle
        self.mcontent = mcontent
        self.mcettime = datetime.now()

    def __repr__(self):
        return "<MeetingInfo('%s')>" % (self.mtitle)

def getDBURL():
   return 'postgresql+psycopg2://%s:%s@%s:%d/%s' % (DBSETTINGS['db_user'], DBSETTINGS['db_password'], DBSETTINGS['db_host'], DBSETTINGS['db_port'], DBSETTINGS['db_name'])

class DB_Session(object):
    def __init__(self):
        engine = create_engine(getDBURL())
        self.Session = sessionmaker(bind=engine)

    @property
    def getSession(self):
        return self.Session()

db_session = DB_Session()
