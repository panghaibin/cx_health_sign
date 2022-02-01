# -*- coding: utf8 -*-
from config import _Report


class HNISCHealthReport(_Report):
    def __init__(self, username, password, school_id=''):
        super().__init__(username, password, school_id)

        self._form_id = '158324'
        self._enc = 'b08ae0de35d833ebc04ad7c5604f1b43'
        self._reporter_name = 'HNISC健康打卡'

        self._temperature_id = 7
        self._options_ids = [33, 6, 25, 26, 8, 9]
        self._hasAuthority_ids = [1, 23, 24, 32, 36]
        self._isShow_ids = [14, 29, 30]

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._temperature_id:
                temperature = self._random_temperature()
                f['fields'][0]['values'][0]['val'] = temperature
            elif f['id'] in self._options_ids:
                # 下拉项选择改写为 true
                for option in f['fields'][0]['options']:
                    if f['fields'][0]['values'][0]['val'] == option['title']:
                        option['checked'] = True
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False
            elif f['id'] in self._isShow_ids:
                f['isShow'] = False

        self._today_form_data = form_data
        return form_data
