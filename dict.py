#! /usr/bin/env python
# -*- coding: utf-8 -*-
_author_ = 'm2shad0w'
_Time_ = '2015-09-26'
_version_ = '1.00'

import json
import urllib
import urllib2
import sys


class DictBaiDu:
    _from = 'auto'
    _to = 'auto'
    _client_id = '5PRuCGTvkkmEkT3mYiGTGOn8'
    api = "http://openapi.baidu.com/public/2.0/bmt/translate"
    get_param = "?from="+_from+"&to="+_to+"&client_id="+_client_id+"&q="
    content = None
    post_body = {'from': _from,
                 'to': _to,
                 'client_id': _client_id,
                 'q': ''
                 }

    def __init__(self, argv):
        if len(argv) > 1:
            # self.post_body['q'] = argv[1:]
            self.api += self.get_param
            for i in range(1, len(argv)):
                self.api += argv[i]+' '
            print self.api
            self.translate()
        else:
            print 'Error! Plese Input Your Content.'

    def translate(self):

        # print urllib.urlencode(self.post_body)
        # self.content = urllib2.urlopen(self.api, urllib.urlencode(self.post_body)).read()
        self.content = urllib2.urlopen(self.api).read()
        self.content = json.loads(self.content)
        self.parse()
        # print self.content

    def parse(self):
        try:
            trans_result = self.content['trans_result']
            # print trans_result
        except KeyError:
            code = self.content['error_code']
            if code == 52001:
                print "①TIMEOUT：超时（52001）【请调整文本字符长度】"
            elif code == 52002:
                print '②SYSTEM ERROR：翻译系统错误（52002）'
            elif code == 52003:
                print "③UNAUTHORIZED USER：未授权的用户（52003）【请检查是否将api key输入错误"
            else:
                print '③msg:PARAM_FROM_TO_OR_Q_EMPTY：必填参数为空（5004）【from 或 to 或query 三个必填参数，请检查是否相关参数未填写完整】'
            return
        print '\033[1;31m################################### \033[0m'

        if trans_result != 'None':
            for i in range(0, len(trans_result)):
                print '\033[1;31m# \033[0m', (trans_result[i]['src']), (trans_result[i]['dst'])
        else:
            print '\033[1;31m# \033[0m Explains None'
        print '\033[1;31m################################### \033[0m'
if __name__ == '__main__':
    DictBaiDu(sys.argv)
