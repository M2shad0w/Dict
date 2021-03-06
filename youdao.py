#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import time
from sys import version_info


YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '69c37883a7a8a5b7'
APP_SECRET = 'your key'
# 文档地址
# https://ai.youdao.com/DOCSIRMA/html/自然语言翻译/API文档/文本翻译服务/文本翻译服务-API文档.html


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    if version_info.major == 3:
        pass
    else:
        q = q.decode("utf-8")
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(query_world):
    # q = "english"
    q = ' '.join(query_world)
    data = {}
    data['from'] = 'auto'
    data['to'] = 'auto'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        # print(response.content)
        try:
            import json
            req = json.loads(response.content)
            print('\033[1;31m{} \033[0m'.format('###' * 10))
            print('\033[1;31m# trans: \033[0m %s' % (req["translation"][0]))
            # print(req["translation"][0])
            if "web" in req.keys():
                print('\033[1;31m# %s 联想 : %s\033[0m' % ('---' * 4, '---' * 4))
                if version_info.major == 3:
                    print('\033[1;31m# web key: \033[0m %s' % (req["web"][0]["key"]))
                else:
                    print('\033[1;31m# web key: \033[0m %s' % (req["web"][0]["key"]).encode("utf-8"))
                print('\033[1;31m# web value: \033[0m %s' % (', '.join(req["web"][0]["value"])))
            # print(', '.join(req["web"][0]["value"]))
            print('\033[1;31m{} \033[0m'.format('###' * 10))
        except Exception as e:
            print(e)
            print('\033[1;31m{} \033[0m'.format(req))


if __name__ == '__main__':
    q = sys.argv[1:]
    if len(q) > 0:
        connect(q)
    else:
        print("请输入你的翻译字符")
