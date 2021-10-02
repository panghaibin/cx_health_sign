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
        global_api: dict = self.setting.get('global_send', {})
        self.global_api: dict = {} if global_api is None else global_api

    def _load_setting(self):
        if not os.path.exists(self.setting_path):
            with open(self.setting_path, 'w') as f:
                config = dict(global_send={}, users={})
                yaml.dump(config, f)
        with open(self.setting_path, 'r', encoding='utf-8') as f:
            setting = yaml.load(f, Loader=yaml.FullLoader)
        self.setting = setting

    def _save_setting(self) -> bool:
        with open(self.setting_path, 'w') as f:
            yaml.dump(self.setting, f)
            return True

    def _check_users(self):
        users = self.setting.get('users')
        users = {} if users is None else users
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
                    'api_type': users[username].get('api_type', 0),
                    'api_key': users[username].get('api_key', '')
                }
                user_list.append(user)
        self.user_list = user_list
        return self.user_list

    def add_user(self, username, password, post_type, school_id='', api_type=0, api_key='') -> bool:
        user_info = dict(
            password=password, post_type=post_type, school_id=school_id,
            api_type=api_type, api_key=api_key
        )
        user = {username: user_info}
        self._users.update(user)
        self.setting['users'] = self._users
        save_result = self._save_setting()
        if save_result:
            self._load_setting()
            self._check_users()
        return save_result

    def set_global_send(self, api_type, api_key):
        global_api = dict(api_type=api_type, api_key=api_key)
        global_send = {
            'global_send': global_api
        }
        self.setting.update(global_send)
        save_result = self._save_setting()
        if save_result:
            self._load_setting()
            self.global_api: dict = self.setting['global_send']
        return save_result


class GitHub(object):
    """
    用于 GitHub Actions
    """

    def __init__(self):
        self._users_raw = os.environ['users'].split(';')
        self._global_api_raw = os.environ.get('send', '').split(',')

        self._users: list = []
        self._check_users()
        self.user_list: list = []

        self.global_api: dict = {}
        self._check_global_api()

    def _check_users(self):
        _users = []
        for user_info_raw in self._users_raw:
            user_info = user_info_raw.split(',')
            if len(user_info) == 3:
                user = dict(username=user_info[0], password=user_info[1], post_type=user_info[2],
                            school_id='', api_type=0, api_key='')
            elif len(user_info) == 4:
                user = dict(username=user_info[0], password=user_info[1], post_type=user_info[2],
                            school_id=user_info[3], api_type=0, api_key='')
            elif len(user_info) == 5:
                user = dict(username=user_info[0], password=user_info[1], post_type=user_info[2],
                            school_id='', api_type=int(user_info[3]), api_key=user_info[4])
            elif len(user_info) == 6:
                user = dict(username=user_info[0], password=user_info[1], post_type=user_info[2],
                            school_id=user_info[3], api_type=int(user_info[4]), api_key=user_info[5])
            else:
                continue
            _users.append(user)
        self._users = _users

    def get_users(self, post_type=None) -> list:
        if not post_type:
            self.user_list = self._users
        else:
            user_list = []
            for user in self._users:
                if user['post_type'] == post_type:
                    user_list.append(user)
            self.user_list = user_list
        return self.user_list

    def _check_global_api(self):
        if len(self._global_api_raw) == 2:
            self.global_api = dict(
                api_type=int(self._global_api_raw[0]),
                api_key=self._global_api_raw[1]
            )
        else:
            self.global_api = dict(api_type=0, api_key='')
