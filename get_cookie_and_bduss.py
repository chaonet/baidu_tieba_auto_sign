#!/usr/bin/env python
# coding: utf-8

import os, sys

import json
import urllib
import urllib2
import cookielib
import ConfigParser

import re
from bs4 import BeautifulSoup

defaultencoding = 'utf-8'

if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

user = ""
password = ""
BDUSS = ""

if os.path.exists('conf.ini'):
    cf = ConfigParser.ConfigParser()
    cf.read('conf.ini')
    user = cf.get('main', 'username')
    password = cf.get('main', 'password')
else:
    user = os.environ.get("username")
    password = os.environ.get("password")

data = urllib.urlopen("http://www.baidu.com").read()
soup = BeautifulSoup(data, 'html.parser')

TOKEN = ""
TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3"
INDEX_URL = "http://www.baidu.com/"
LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

loginHeaders = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
    "Host":"passport.baidu.com",
    'Upgrade-Insecure-Requests':'1',
    "Origin":"http://www.baidu.com",
    "Referer":"http://www.baidu.com/",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"
}

bdData = {
    "staticpage":"https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
    "token":"",
    "tpl":"pp",
    "username":user,
    "password":password,
    "loginmerge":"true",
    "mem_pass":"on",
    "logintype":"basicLogin",
    "logLoginType":"pc_loginBasic",
}
"""
signData = {
    "ie":"utf-8",
    "kw":"",
    "tbs":""
}
"""
def get_cookie_and_bduss():
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    try:
        opener.open(INDEX_URL) # 打开百度主页
    except:
        print("网络出现问题,正在退出...")
        return

    #get TOKEN
    print("Loading...正在获取token:")
    try:
        data = opener.open(TOKEN_URL).read()
        TOKEN = re.compile("\"token\"\s+:\s+\"(\w+)\"").findall(str(data))[0]
        bdData["token"] = TOKEN
        print("token获取成功:" + TOKEN)
    except:
        print("网络问题 无法为您获取token,正在退出...")
        return
    #login
    request = urllib2.Request(LOGIN_URL, headers=loginHeaders, data=urllib.urlencode(bdData).encode('utf-8'))
    print "正在为 %s 进行登录操作" % user
    try:
        result = opener.open(request).read()
        # result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
        result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("ISO-8859-1"))

    except:
        print("遇到问题,无法登录,正在退出...")
        return
    # result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
    result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("ISO-8859-1"))

    if result["no"] == 0:
        print(user + "登录成功!")
        # print cookie
        for ck in cookie:
            if ck.name == 'BDUSS':
                BDUSS = ck.value 
                # print BDUSS
    return cookie,BDUSS

if __name__ == "__main__":
    ck,bdu = get_cookie_and_bduss()
    print ck
    print bdu

