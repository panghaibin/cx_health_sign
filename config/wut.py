# -*- coding: utf8 -*-
from config import _Report


class WUTHealthReport(_Report):
    """
    WUT Health Report
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)
        self._form_id = '89398'
        self._enc = '75244f75384287c902e57b080c4d1c6d'
        self._reporter_name = 'WUT健康打卡'

        self._day_id = 38
        self._report_time_id = -1
        self._temperature_ids = []
        self._options_ids = [12, 13, 14, 15, 16, 17, 19, 20, 22, 24, 26, 28, 30, 33, 36]
        self._hasAuthority_ids = [38]
        self._isShow_ids = [21, 23, 25, 27, 32, 29, 34, 35, 36, 37, 17, 18]

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._day_id:
                # 打卡日期
                today = self._t.today
                f['fields'][0]['values'][0]['val'] = today
            elif f['id'] in self._temperature_ids and f['id'] not in self._options_ids:
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
