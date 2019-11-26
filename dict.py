#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from hashlib import md5
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
import sys
try:
    import httplib
    import sys  
    reload(sys)  
    sys.setdefaultencoding('utf8')
except ImportError:
    import http.client as httplib
import random

appid = 'your appid'
secretKey = 'your secret'
is_dict = '0'


class DictBaiDu(object):
    """
    baidu dict
    """

    def __init__(self, argv):
        if len(argv) > 1:
            q = ' '.join(argv[1:])
            print(q)
            is_chinese = is_contains_chinese(q)
            if is_chinese:
                # 添加判断是否中文
                fromLang = 'zh'
                toLang = 'en'
            else:
                # 添加判断是否中文
                fromLang = 'en'
                toLang = 'zh'

            httpClient = None
            myurl = '/api/trans/vip/translate'

            self.content = None
            salt = random.randint(32768, 65536)

            sign = appid + q + str(salt) + secretKey
            m1 = md5()
            m1.update(sign.encode('utf-8'))
            sign = m1.hexdigest()
            self.myurl = myurl+'?appid='+appid+'&q='+quote(q)+'&from='+fromLang+'&to='+\
                         toLang+'&salt='+str(salt)+'&sign='+sign+'&dict=' + is_dict
            print(self.myurl)
            self.translate()
        else:
            print('Error! Plese Input Your Content.')

    def translate(self):
        """
        翻译
        """
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        # print(self.myurl)
        httpClient.request('GET', self.myurl)
        response = httpClient.getresponse()
        res = response.read()
        # print type(response.read())
        # print(res)
        self.content = json.loads(res)
        self.parse()

    def parse(self):
        """
        解析响应内容
        """
        try:
            print(self.content)
            trans_result = self.content['trans_result']
            # print trans_result
            dict_content = self.content["dict"]
            print(dict_content)
        except KeyError:
            code = self.content['error_code']
            if code == 52001:
                print("① TIMEOUT：超时（52001）【请调整文本字符长度】")
            elif code == 52002:
                print('② SYSTEM ERROR：翻译系统错误（52002）')
            elif code == 52003:
                print("③ UNAUTHORIZED USER：未授权的用户（52003）【请检查是否将api key输入错误")
            else:
                print('code: {} 账户余额不足'.format(code))
            return

        if trans_result != 'None':
            print('\033[1;31m{} \033[0m'.format('#'*3*len((trans_result[0]['src']).encode('UTF-8'))))
            for i in range(0, len(trans_result)):
                print('\033[1;31m# \033[0m %s %s' % ((trans_result[i]['src']), (trans_result[i]['dst'])))
            print('\033[1;31m{} \033[0m'.format('#'*3*len(trans_result[0]['src'].encode('UTF-8'))))
        else:
            print('\033[1;31m# \033[0m Explains None')


def is_contains_chinese(x):
    import re
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    x = x.decode()
    return zh_pattern.search(x)


if __name__ == '__main__':
    DictBaiDu(sys.argv)
