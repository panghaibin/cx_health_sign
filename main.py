# -*- coding: utf8 -*-
import json
import random
import requests
from setting import Setting
from config import Time
from config.default import DefaultHealthReport
from config.nnnu import NNNUHealthReport
from config.test import TestReport


class MainHandle(object):
    """
    主函数
    """

    def __init__(self):
        setting = Setting()
        self._reporters = {
            'test': TestReport,
            'default': DefaultHealthReport,
            'nnnu': NNNUHealthReport,
        }
        self._users = setting.get_users(post_type=None)
        self._global_api = setting.global_api
        # 健康报告结果，多用户存储在一个数组
        self.report_results: list = []
        # 消息发送结果
        self.send_results: list = []

        self.report_all()

        # 全局消息发送结果
        self.global_send_result: str = ''
        self.global_send()

    def report_all(self):
        for user in self._users:
            try:
                post_type = user['post_type']
                r = self._reporters[post_type](user['username'], user['password'], user['school_id'])
                t = r.report()
                self.report_results.append(t)
            except Exception as e:
                self.report_results.append(str(e))
            if user['api_type'] not in ['', 0]:
                send = SendMsg(user, result=self.report_results[-1])
                self.send_results.append(send.send_result)
            else:
                self.send_results.append('')

    def global_send(self) -> str:
        api = {
            'api_type': self._global_api.get('api_type', ''),
            'api_key': self._global_api.get('api_key', '')
        }
        if api['api_type'] not in ['', 0]:
            send = SendMsg(api, result_list=self.report_results)
            self.global_send_result = send.send_result
        else:
            self.global_send_result = '未指定全局消息推送'
        return self.global_send_result


class SendMsg(object):
    """
    消息发送函数
    """

    def __init__(self, user_api, result: str = None, result_list: list = None):
        if result is None and result_list is None:
            raise Exception('必须传入 result 或 result_list')

        self._api_types = ('未设置', '方糖气球', '推送加')
        self.api_type = user_api['api_type']
        self.api_key = user_api['api_key']
        if self.api_type not in range(1, len(self._api_types)):
            raise Exception('未正确配置消息发送类型')
        self.api_type_name = self._api_types[self.api_type]
        self.send_result: dict = {}
        self.send_result_bool: bool = False

        self.result_list = result_list
        self.title = result if result is not None else result_list[0]
        self.desp: str = Time().now_time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
        self.desp += result if result is not None else "\n\n".join(result_list)
        # 添加随机字符以确保提交成功
        self.desp += "\n\n" + str(random.randint(0, 100000))

        # 这里要写在最后，确保 title resp 已初始化
        self._send_api = (None, self.server_chan(), self.push_plus())

        self.send_msg()

    def server_chan(self) -> bool:
        url = "http://sctapi.ftqq.com/%s.send" % self.api_key
        data = {
            'text': self.title,
            'desp': self.desp
        }
        text = requests.post(url, data=data).text
        send_result = json.loads(text)
        self.send_result = send_result
        if send_result['code'] == 0:
            return True
        else:
            return False

    def push_plus(self) -> bool:
        url = "http://www.pushplus.plus/send"
        data = {
            'token': self.api_key,
            'title': self.title,
            'content': self.desp,
            'template': 'markdown'
        }
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data).encode(encoding='utf-8')
        text = requests.post(url, data=body, headers=headers).text
        send_result = json.loads(text)
        self.send_result = send_result
        if send_result['code'] == 200:
            return True
        else:
            return False

    def send_msg(self) -> bool:
        result_bool = self._send_api[self.api_type]
        self.send_result_bool = result_bool
        return self.send_result_bool


if __name__ == '__main__':
    main = MainHandle()
    # 打印每个用户健康报告填报结果
    print(main.report_results)
    # 打印每个用户的消息发送结果
    print(main.send_results)
    # 打印全局消息发送结果
    print(main.global_send_result)
