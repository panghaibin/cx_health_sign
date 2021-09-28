# -*- coding: utf8 -*-
import os
import pickle
import requests


class Session(object):
    def __init__(self, username, session=None):
        self._abs_path = os.path.split(os.path.realpath(__file__))[0]
        self.sess_path = self._abs_path + '/%s.sess' % username
        self.session = session

    def load_session(self, use_new=False):
        if os.path.exists(self.sess_path) and not use_new:
            with open(self.sess_path, 'rb') as f:
                self.session = pickle.load(f)
                return self.session
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/84.0.4147.125 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
            }
            self.session = requests.session()
            self.session.headers = headers
            return self.session

    def save_session(self):
        with open(self.sess_path, 'wb') as f:
            pickle.dump(self.session, f)
            return True
