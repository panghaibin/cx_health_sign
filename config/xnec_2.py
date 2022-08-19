# -*- coding: utf8 -*-
from config import _Report


class XNECHealthReport2(_Report):
    """
    XNEC健康打卡2
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)
        self._form_id = '100244'
        self._enc = 'c30d59556090a358fc0fb4992dd65cc1'
        self._reporter_name = 'XNEC健康打卡2'

        self._day_id = 59
        self._report_time_id = -1
        self._temperature_ids = [58]
        self._options_ids = [60, 8, 45, 11, 13, 15, 56, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 38]
        self._hasAuthority_ids = [1, 49, 51, 52, 53, 46, 7, 37]
        self._isShow_ids = [10, 12, 14, 56, 57, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 39, 41, 42, 43]

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._day_id:
                # 打卡日期
                today = self._t.today
                f['fields'][0]['values'][0]['val'] = today
            elif f['id'] in self._temperature_ids:
                # 体温
                temperature = self._random_temperature()
                f['fields'][0]['values'][0]['val'] = temperature
            elif f['id'] in self._options_ids and f['id'] not in self._isShow_ids:
                # 下拉项选择改写为 true
                for option in f['fields'][0]['options']:
                    if f['fields'][0]['values'][0]['val'] == option['title']:
                        option['checked'] = True
            elif f['id'] in self._hasAuthority_ids:
                # 内部使用的id
                f['hasAuthority'] = False
            elif f['id'] in self._isShow_ids:
                # 内部使用的id
                f['isShow'] = False

        self._today_form_data = form_data
        return form_data
