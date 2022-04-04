# -*- coding: utf8 -*-
from config import _Report


class SWUTHealthReportNoon(_Report):
    """
    SWUT 午检打卡
    """

    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '175235'
        self._enc = 'fb50b811a71a357bbb3a87424f7c074c'
        self._reporter_name = 'SWUT午检打卡'

        self._temperature_id = 6
        self._options_ids = [10, 12, 13, 19, 14]
        self._day_id = 20

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
            elif f['id'] == self._day_id:
                today = self._t.today
                f['fields'][0]['values'][0]['val'] = today

        self._today_form_data = form_data
        return form_data
