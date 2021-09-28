# -*- coding: utf8 -*-
import os
import yaml


class Setting(object):
    def __init__(self):
        self._abs_path = os.path.split(os.path.realpath(__file__))[0]
        self.setting_path = self._abs_path + "/setting.yaml"
        self.users = {}
        self.user_list = []

    def check_setting(self):
        if not os.path.exists(self.setting_path):
            print('未找到配置文件')
            print('请创建 setting.yaml 文件')
            print('格式参考 setting.bak.yaml')
            raise Exception('配置文件不存在')
        with open(self.setting_path, 'r', encoding='utf-8') as f:
            users = yaml.load(f, Loader=yaml.FullLoader)['users']
        for user in list(users.keys()):
            if 'username_here' in user:
                users.pop(user)
        self.users = users
        return self.users

    def get_users(self, config=None):
        self.check_setting()
        users = self.users
        user_list = []
        for username in list(users.keys()):
            if users[username][1] == config or config is None:
                user = {
                    'username': username,
                    'password': users[username][0]
                }
                user_list.append(user)
        self.user_list = user_list
        return self.user_list

    def add_user(self):
        # TODO
        pass
