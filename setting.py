# -*- coding: utf8 -*-
import os
import yaml


class Setting(object):
    def __init__(self):
        self._abs_path = os.path.split(os.path.realpath(__file__))[0]
        self.setting_path = self._abs_path + "/setting.yaml"
        self._check_setting()
        self._check_users()
        self.user_list = []
        self.global_api = self.setting.get('global_send')

    def _check_setting(self):
        if not os.path.exists(self.setting_path):
            print('未找到配置文件')
            print('请创建 setting.yaml 文件')
            print('格式参考 setting.bak.yaml')
            raise Exception('配置文件不存在')
        with open(self.setting_path, 'r', encoding='utf-8') as f:
            setting = yaml.load(f, Loader=yaml.FullLoader)
        self.setting = setting

    def _check_users(self):
        users = self.setting.get('users', [])
        for user in list(users.keys()):
            if 'username_' in user:
                users.pop(user)
        self._users = users
        return self._users

    def get_users(self, post_type=None):
        self._check_users()
        users = self._users
        user_list = []
        for username in list(users.keys()):
            if users[username]['post_type'] == post_type or post_type is None:
                user = {
                    'username': username,
                    'password': users[username]['password'],
                    'school_id': users[username].get('school_id', ''),
                    'post_type': users[username]['post_type'],
                    'api_type': users[username]['api_type'],
                    'api_key': users[username]['api_key']
                }
                user_list.append(user)
        self.user_list = user_list
        return self.user_list

    def add_user(self):
        # TODO
        pass
