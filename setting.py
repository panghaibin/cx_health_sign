# -*- coding: utf8 -*-
import os
import yaml


class Setting(object):
    def __init__(self):
        self._abs_path = os.path.split(os.path.realpath(__file__))[0]
        self.setting_path = self._abs_path + "/setting.yaml"
        self.setting: dict = {}
        self._load_setting()
        self._users: dict = {}
        self._check_users()
        self.user_list: list = []
        self.global_api: dict = self.setting.get('global_send', {})

    def _load_setting(self):
        if not os.path.exists(self.setting_path):
            print('未找到配置文件')
            print('请创建 setting.yaml 文件')
            print('格式参考 setting.bak.yaml')
            raise Exception('配置文件不存在')
        with open(self.setting_path, 'r', encoding='utf-8') as f:
            setting = yaml.load(f, Loader=yaml.FullLoader)
        self.setting = setting

    def _save_setting(self) -> bool:
        with open(self.setting_path, 'w') as f:
            yaml.dump(self.setting, f)
            return True

    def _check_users(self):
        users = self.setting.get('users', {})
        save_requite = False
        for user in list(users.keys()):
            if 'username_' in user:
                users.pop(user)
                save_requite = True
        self._users: dict = users
        if save_requite:
            self.setting['users'] = users
            self._save_setting()

    def get_users(self, post_type=None) -> list:
        self._check_users()
        users = self._users
        user_list = []
        for username in list(users.keys()):
            if users[username]['post_type'] == post_type or post_type is None:
                user = {
                    'username': username,
                    'password': users[username]['password'],
                    'post_type': users[username]['post_type'],
                    'school_id': users[username].get('school_id', ''),
                    'api_type': users[username].get('api_type', ''),
                    'api_key': users[username].get('api_key', '')
                }
                user_list.append(user)
        self.user_list = user_list
        return self.user_list

    def add_user(self, username, password, post_type, school_id='', api_type='', api_key='') -> bool:
        user_info = dict(
            password=password, post_type=post_type, school_id=school_id,
            api_type=api_type, api_key=api_key
        )
        user = {username: user_info}
        self._users.update(user)
        self.setting['users'] = self._users
        return self._save_setting()
