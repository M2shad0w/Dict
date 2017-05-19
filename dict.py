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

appid = '20151113000005349'
secretKey = 'osubCEzlGjzvw8qdQc41'

class DictBaiDu(object):
    """
    baidu dict
    """

    def __init__(self, argv):
        if len(argv) > 1:
            q = ' '.join(argv[1:])
            httpClient = None
            myurl = '/api/trans/vip/translate'
            fromLang = 'en'
            toLang = 'zh'
            self.content = None
            salt = random.randint(32768, 65536)

            sign = appid + q + str(salt) + secretKey
            m1 = md5()
            m1.update(sign.encode('utf-8'))
            sign = m1.hexdigest()
            self.myurl = myurl+'?appid='+appid+'&q='+quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
            self.translate()
        else:
            print('Error! Plese Input Your Content.')

    def translate(self):
        """
        翻译
        """
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', self.myurl)
        response = httpClient.getresponse()
        res = response.read()
        # print type(response.read())
        self.content = json.loads(res)
        self.parse()

    def parse(self):
        """
        解析响应内容
        """
        try:
            trans_result = self.content['trans_result']
            # print trans_result
        except KeyError:
            code = self.content['error_code']
            if code == 52001:
                print("①TIMEOUT：超时（52001）【请调整文本字符长度】")
            elif code == 52002:
                print('②SYSTEM ERROR：翻译系统错误（52002）')
            elif code == 52003:
                print("③UNAUTHORIZED USER：未授权的用户（52003）【请检查是否将api key输入错误")
            else:
                print('③msg:PARAM_FROM_TO_OR_Q_EMPTY：必填参数为空（5004）【from 或 to 或query 三个必填参数，请检查是否相关参数未填写完整】')
            return
        print('\033[1;31m################################### \033[0m')

        if trans_result != 'None':
            for i in range(0, len(trans_result)):
                print('\033[1;31m# \033[0m %s %s' % ((trans_result[i]['src']), (trans_result[i]['dst'])))
        else:
            print('\033[1;31m# \033[0m Explains None')
        print('\033[1;31m################################### \033[0m')
if __name__ == '__main__':
    DictBaiDu(sys.argv)
