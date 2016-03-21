#!/usr/bin/env python
# coding: utf-8

import os, sys

import urllib
import urllib2
import cookielib
import re
import hashlib
import json
import threading
import platform

import ConfigParser

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






def _setup_cookie(cookie):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    """
    # Install an OpenerDirector instance as the default global opener. 
    # install it globally so it can be used with urlopen.

    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    urllib2.urlopen('http://www.example.com/login.html')
    """
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
 
    """
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'),
                         ('Cookie', my_cookie), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
    """

def _fetch_like_tieba_list():
    print u'获取喜欢的贴吧ing...' if system_env else '获取喜欢的贴吧ing...'
    page_count = 1
    find_like_tieba = []
    while True:
        like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
        req = urllib2.Request(like_tieba_url)
        resp = urllib2.urlopen(req).read()
        resp = resp.decode('gbk').encode('utf8')
        re_like_tieba = '<a href="\/f\?kw=.*?" title="(.*?)">.+?<\/a>'
        temp_like_tieba = re.findall(re_like_tieba, resp)
        if not temp_like_tieba:
            break
        if not find_like_tieba:
            find_like_tieba = temp_like_tieba
        else:
            find_like_tieba += temp_like_tieba
        page_count += 1

    return find_like_tieba


def _fetch_tieba_info(tieba):
    tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba
    wap_resp = urllib2.urlopen(tieba_wap_url).read()

    if not wap_resp:
        return
    re_already_sign = '<td style="text-align:right;"><span[ ]>(.*?)<\/span><\/td><\/tr>'
    already_sign = re.findall(re_already_sign, wap_resp)

    re_fid = '<input type="hidden" name="fid" value="(.+?)"\/>'
    _fid = re.findall(re_fid, wap_resp)
    fid = _fid and _fid[0] or None

    re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'
    _tbs = re.findall(re_tbs, wap_resp)

    tbs = _tbs and _tbs[0] or None
    return already_sign, fid, tbs


def _decode_uri_post(postData):
    SIGN_KEY = "tiebaclient!!!"
    s = ""
    keys = postData.keys()
    keys.sort()
    for i in keys:
        s += i + '=' + postData[i]
    sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()
    postData.update({'sign': str(sign)})
    return postData


def _make_sign_request(tieba, fid, tbs, BDUSS):
    sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
    sign_request = {"BDUSS": BDUSS, "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36", "_client_type":
                    "4", "_client_version": "1.2.1.17", "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6", "fid": fid, "kw": tieba, "net_type": "3", 'tbs': tbs}

    sign_request = _decode_uri_post(sign_request)
    sign_request = urllib.urlencode(sign_request)

    sign_request = urllib2.Request(sign_url, sign_request)
    sign_request.add_header(
        "Content-Type", "application/x-www-form-urlencoded")
    return sign_request


def _handle_response(sign_resp):
    sign_resp = json.load(sign_resp)
    error_code = sign_resp['error_code']
    sign_bonus_point = 0
    try:
        # Don't know why but sometimes this will trigger key error.
        sign_bonus_point = int(sign_resp['user_info']['sign_bonus_point'])
    except KeyError:
        pass
    if error_code == '0':
        print u"签到成功,经验+%d" % sign_bonus_point if system_env else "签到成功,经验+%d" % sign_bonus_point
    else:
        error_msg = sign_resp['error_msg']
        if error_msg == u'亲，你之前已经签过了':
            print u'之前已签到' if system_env else '之前已签到'
        else:
            print u'签到失败' if system_env else '签到失败'
            print "Error:" + unicode(error_code) + " " + unicode(error_msg)


def _sign_tieba(tieba, BDUSS):
    already_sign, fid, tbs = _fetch_tieba_info(tieba)
    if not already_sign:
        print tieba.decode('utf-8') + u'......正在尝试签到' if system_env else tieba + '......正在尝试签到'
    else:
        if already_sign[0] == "已签到":
            print tieba.decode('utf-8') + u"......之前已签到" if system_env else tieba + "......之前已签到"
            return

    if not fid or not tbs:
        print u"签到失败，原因未知" if system_env else "签到失败，原因未知"
        return

    sign_request = _make_sign_request(tieba, fid, tbs, BDUSS)
    sign_resp = urllib2.urlopen(sign_request, timeout=5)
    _handle_response(sign_resp)


def sign(cookie, BDUSS):
    _setup_cookie(cookie)
    _like_tieba_list = _fetch_like_tieba_list()
    if len(_like_tieba_list) == 0:
        print u"获取喜欢的贴吧失败，请检查Cookie和BDUSS是否正确" if system_env else "获取喜欢的贴吧失败，请检查Cookie和BDUSS是否正确"
        return
    thread_list = []
    for tieba in _like_tieba_list:
        t = threading.Thread(target=_sign_tieba, args=(tieba, BDUSS))
        thread_list.append(t)
        t.start()
        
    for t in thread_list:
        t.join(2)


def main():
    ck,bdu = get_cookie_and_bduss()
    sign(ck, bdu)

if __name__ == "__main__":
    system_env = True
    main()
    # os.system("date /T >> tieba_log.log") if system_env else os.system("date >> tieba_log.log")
