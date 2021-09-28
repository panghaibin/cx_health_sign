# -*- coding: utf8 -*-
import json
import requests
from setting import Setting
from config.default import DefaultHealthReport
from config.nnnu import NNNUHealthReport
from config.test import TestReport


class MainHandle(object):
    """
    主函数
    """

    def __init__(self):
        setting = Setting()
        self._default_user = setting.get_users(config='default')
        self._nnnu_user = setting.get_users(config='nnnu')
        self._test_user = setting.get_users(config='test')
        self.results = []

        for user in self._default_user:
            try:
                r = DefaultHealthReport(user['username'], user['password'])
                t = r.report()
                self.results.append(t)
            except Exception as e:
                self.results.append(str(e))
        for user in self._nnnu_user:
            try:
                r = NNNUHealthReport(user['username'], user['password'])
                t = r.report()
                self.results.append(t)
            except Exception as e:
                self.results.append(str(e))
        for user in self._test_user:
            try:
                r = TestReport(user['username'], user['password'])
                t = r.report()
                self.results.append(t)
            except Exception as e:
                self.results.append(str(e))


class SendMsg(object):
    """
    消息发送函数
    """

    def __init__(self, results):
        if not results:
            raise Exception('消息内容不能为空')
        self.results = results
        self._api_types = ['未设置', '方糖气球', '推送加']
        setting = Setting()
        self.api_type = setting.api_type
        self.api_key = setting.api_key
        if self.api_type not in range(1, len(self._api_types)) or self.api_key == '':
            raise Exception('未配置消息发送类型及 key')
        self.api_type_name = self._api_types[self.api_type]
        self.send_result = {}
        self.send_result_bool = None
        self.desp = ''
        for i in self.results:
            self.desp += i + "\n\n"

    def server_chan(self):
        url = "http://sctapi.ftqq.com/%s.send" % self.api_key
        data = {
            'text': self.results[0],
            'desp': self.desp
        }
        text = requests.post(url, data=data).text
        result = json.loads(text)
        self.send_result = result
        if result['data']['error'] == 'SUCCESS':
            return True
        else:
            return False

    def push_plus(self):
        url = "http://www.pushplus.plus/send"
        data = {
            'token': self.api_key,
            'title': self.results[0],
            'content': self.desp,
            'template': 'markdown'
        }
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data).encode(encoding='utf-8')
        text = requests.post(url, data=body, headers=headers).text
        result = json.loads(text)
        self.send_result = result
        if result['code'] == 200:
            return True
        else:
            return False

    def send_msg(self):
        result_bool = False
        if self.api_type == 1:
            result_bool = self.server_chan()
        elif self.api_type == 2:
            result_bool = self.push_plus()
        self.send_result_bool = result_bool
        return self.send_result_bool


if __name__ == '__main__':
    main = MainHandle()
    print(main.results)
    send = SendMsg(main.results)
    send.send_msg()
    print(send.send_result)
