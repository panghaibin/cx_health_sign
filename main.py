# -*- coding: utf8 -*-
import os
import sys
import json
import random
import traceback
import requests
import logging
from time import sleep
from setting import Setting
from setting import GitHub
from config import Time
from config.default import DefaultHealthReport
from config.nnnu import NNNUHealthReport
from config.hnucc import HNUCCHealthReport
from config.swut import SWUTHealthReport
from config.hnisc import HNISCHealthReport
from config.test import TestReport


class MainHandle(object):
    """
    主函数
    """

    def __init__(self):
        self._users: list = []
        self.users_num: int = 0
        self._global_api: dict = {}
        self._reporters = {
            'test': TestReport,
            'default': DefaultHealthReport,
            'nnnu': NNNUHealthReport,
            'hnucc': HNUCCHealthReport,
            'swut': SWUTHealthReport,
            'hnisc': HNISCHealthReport,
        }

        # 健康上报结果，多用户存储在一个数组
        self.report_results: list = []
        # 消息发送结果
        self.send_results: list = []
        # 全局消息发送结果
        self.global_send_result: str = ''

    @staticmethod
    def _sleep():
        """
        休眠函数，多个用户填报时，防止被封
        通过设置环境变量控制，默认 5s
        """
        os_sleep = os.getenv('sleep_time', '5')
        if os_sleep == 'random':
            sleep(random.randint(30, 360))
        else:
            sleep(int(os_sleep))

    def main(self):
        setting = Setting()
        self._users = setting.get_users(post_type=None)
        self.users_num = len(self._users)
        self._global_api = setting.global_api

        if self.users_num == 0:
            print('用户数量为0，开始添加用户')
            self.add_user()
            print('可执行 `python main.py add` 或修改 setting.yaml 文件继续添加')
        # 填报全部用户
        self.report_all()
        # 发送全局消息
        self.global_send()

        # 打印每个用户健康报告填报结果
        print(self.report_results)
        # 打印每个用户的消息发送结果
        print(self.send_results)
        # 打印全局消息发送结果
        print(self.global_send_result)

    def report_all(self):
        for user in self._users:
            self._sleep()
            try:
                post_type = user['post_type']
                r = self._reporters[post_type](user['username'], user['password'], user.get('school_id', ''))
                t = r.report()
                self.report_results.append(t)
            except Exception as e:
                logging.exception(e)
                msg = traceback.format_exc()
                self.report_results.append(str(msg))
            if user.get('api_type', 0) != 0:
                send = SendMsg(user, result=self.report_results[-1])
                self.send_results.append(send.send_result)
            else:
                self.send_results.append('用户未指定消息推送服务')

    def global_send(self) -> str:
        api = {
            'api_type': self._global_api.get('api_type', 0),
            'api_key': self._global_api.get('api_key', '')
        }
        if api['api_type'] != 0:
            send = SendMsg(api, result_list=self.report_results)
            self.global_send_result = send.send_result
        else:
            self.global_send_result = '未指定全局消息推送'
        return self.global_send_result

    @staticmethod
    def _input(message: str, is_require=True, message_list=None):
        """
        封装的输入函数，判断是否必填项，支持对一个列表的选择（返回该列表的下标 (int) ），进行了错误处理
        """
        if message_list is not None:
            for i in range(len(message_list)):
                print("%s: %s" % (i + 1, message_list[i]))

        while True:
            data = input(message)
            if data == '' and not is_require:
                break
            elif data != '' and message_list is None:
                break
            elif data != '' and message_list is not None:
                try:
                    data = int(data) - 1
                    if 0 <= data <= len(message_list) - 1:
                        print('已选择: %s' % message_list[data])
                        break
                except Exception as e:
                    print(e)
        return data

    def add_user(self) -> bool:
        setting = Setting()

        print('输入用户名')
        print('手机号/邮箱/学号均可，必填')
        username = self._input('请输入: ')

        print('输入密码，必填')
        password = self._input('请输入: ')

        print('输入需要打卡的配置类型，必填')
        report_types = list(self._reporters.keys())
        post_type = self._input('请选择: ', message_list=report_types)
        post_type = report_types[post_type]

        print('输入学校id，选填 若使用学号登录则必填')
        school_id = self._input('请输入: ', is_require=False)

        print('选择消息推送服务，选填')
        send = SendMsg
        send_types = [send.api_types_name[i] + ' ' + send.api_types_url[i] for i in range(len(send.api_types_name))]
        api_type = self._input('请选择: ', is_require=False, message_list=send_types[1:])
        api_type = 0 if api_type == '' else api_type + 1

        api_key = ''
        if api_type != 0:
            print('输入消息推送 key')
            api_key = self._input('请输入: ')

        add_result = setting.add_user(username, password, post_type, school_id, api_type, api_key)
        if add_result:
            print('用户添加成功')
            self._users = setting.get_users(post_type=None)
        else:
            print('用户添加失败')
        return add_result

    def set_global_send(self) -> bool:
        setting = Setting()
        print('设置全局推送服务')

        print('选择消息推送服务')
        send = SendMsg
        send_types = [send.api_types_name[i] + ' ' + send.api_types_url[i] for i in range(len(send.api_types_name))]
        api_type = self._input('请选择: ', is_require=True, message_list=send_types[1:])
        api_type = 0 if api_type == '' else api_type + 1

        print('输入消息推送 key')
        api_key = self._input('请输入: ')
        add_result = setting.set_global_send(api_type, api_key)
        if add_result:
            print('全局推送设置成功')
            self._global_api = setting.global_api
        else:
            print('全局推送设置失败')
        return add_result


class GitHubHandle(MainHandle):

    def __init__(self):
        super().__init__()

    def main(self):
        setting = GitHub()
        self._users = setting.get_users(post_type=None)
        self.users_num = len(self._users)
        self._global_api = setting.global_api

        if self.users_num == 0:
            raise Exception('GitHub Actions Secrets 未设置')
        # 填报全部用户
        self.report_all()
        # 发送全局消息
        self.global_send()

        # 打印每个用户健康报告填报结果
        print(self.report_results)
        # 打印每个用户的消息发送结果
        print(self.send_results)
        # 打印全局消息发送结果
        print(self.global_send_result)

    def add_user(self) -> bool:
        return False

    def set_global_send(self) -> bool:
        return False


class SendMsg(object):
    """
    消息发送类
    """

    api_types_name = [
        '未设置',
        'Server酱',
        '推送加',
        '推送加(hxtrip域下)'
    ]

    api_types_url = [
        '',
        'https://sct.ftqq.com/',
        'https://www.pushplus.plus/',
        'https://pushplus.hxtrip.com/'
    ]

    def __init__(self, user_api: dict, result: str = None, result_list: list = None):
        """
        result: 仅发送单条消息
        result_list: 发送多条消息，合并在消息的详情发送
        两个二选一， result 优先
        """
        if not result and not result_list:
            raise Exception('必须传入 result 或 result_list')

        self.api_type = user_api.get('api_type', 0)
        self.api_key = user_api.get('api_key', '')
        if self.api_type not in range(1, len(self.api_types_name)):
            raise Exception('未正确配置消息发送类型')
        self.api_type_name = self.api_types_name[self.api_type]
        self.api_type_url = self.api_types_url[self.api_type]
        self.send_result: dict = {}
        self.send_result_bool: bool = False

        self.result_list = result_list
        self.title = result_list[0] if not result else result
        self.title = self.title.replace("\n", '<br>')[:99]
        self.desp: str = Time().now_time.strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
        self.desp += "\n\n".join(result_list) if not result else result
        # 添加随机字符以确保提交成功
        self.desp += "\n\n" + str(random.randint(0, 100000))

        # 这里要写在最后，确保 title resp 已初始化
        self._send_api = (None, self.server_chan, self.push_plus, self.push_plus_hxtrip)

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

    def push_plus_hxtrip(self) -> bool:
        url = 'http://pushplus.hxtrip.com/send'
        data = {
            "token": self.api_key,
            "title": self.title,
            "content": self.desp.replace("\n\n", "<br>")
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json',
                   'accept': 'application/json'}
        text = requests.post(url, data=body, headers=headers).text
        result = json.loads(text)
        if result['code'] == 200:
            return True
        else:
            return False

    def send_msg(self) -> bool:
        result_bool = self._send_api[self.api_type]()
        self.send_result_bool = result_bool
        return self.send_result_bool


if __name__ == '__main__':
    if len(sys.argv) == 1:
        MainHandle().main()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'add':
            MainHandle().add_user()
        elif sys.argv[1] == 'send':
            MainHandle().set_global_send()
        elif sys.argv[1] == 'gh':
            GitHubHandle().main()
