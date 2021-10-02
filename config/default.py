# -*- coding: utf8 -*-
from config import _Report


class DefaultHealthReport(_Report):
    """
    学习通默认健康上报表单
    form_id 及 enc 来自 GitHub
        https://github.com/mkdir700/chaoxing_auto_sign/blob/bf2255ed59cdbdf0e810e31d07ef6198810fdbe5/heath/main.py
    已修改适配
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '7185'
        self._enc = 'f837c93e0de9d9ad82db707b2c27241e'
        self._reporter_name = '学习通健康表单'

        self._options_ids = [7, 8, 43, 46, 52, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34]
        self._isShow = [9, 45, 48, 49, 47, 53, 54, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
        self._hasAuthority_ids = [5, 6]

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] in self._options_ids:
                # 下拉项选择改写为 true
                for option in f['fields'][0]['options']:
                    if f['fields'][0]['values'][0]['val'] == option['title']:
                        option['checked'] = True
            elif f['id'] in self._isShow:
                f['isShow'] = False
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False

        self._today_form_data = form_data
        return form_data
