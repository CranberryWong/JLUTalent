#! /usr/bin/env python
#coding:utf-8

from email.mime.text import MIMEText
from settings import MAILSETTINGS

import tornado.web
from handlers.admin import StaticData
import smtplib

def sendmail(contact_list, content):
    msg = MIMEText(content, MAILSETTINGS['mail_subtype'], MAILSETTINGS['mail_encode'])
    from_addr = MAILSETTINGS['mail_host_addr']
    password = MAILSETTINGS['mail_host_psw']
    to_addr = contact_list

    server = smtplib.SMTP(MAILSETTINGS['mail_smtp_host'], MAILSETTINGS['mail_smtp_port'])
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

    return "success"

class MailSending(StaticData):
    @tornado.web.authenticated
    def get(self):
        StaticData.init(self)
        self.title = "Mail Sending"
        self.render('admin_mail.html')
        self.session.close()

    def post(self):
        StaticData.init(self)
        self.title = "Mail Sending"
        contact_list = self.get_argument('contact', default='').split(',')
        content = self.get_argument('content', default='')
        sendmail(contact_list, content)
        self.write('<script language="javascript">alert("发送成功");self.location="/admin";</script>')
        self.session.close()
