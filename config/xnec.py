# -*- coding: utf8 -*-
from config import _Report
from config import Time


class XNECHealthReport(_Report):
    """
    XNEC Health Report
    """

    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '100992'
        self._enc = 'bd1883314d3b5f4b36c91dc1907b5c74'
        self._reporter_name = 'XNEC健康打卡'
        self._t = Time()

        self._day_id = 21
        self._report_time_id = 29
        self._temperature_id = 32
        self._options_ids = []
        self._hasAuthority_ids = [34, 30, 31, 8, 9, 10, 29, 24, 26, 27, 28, 35, 38, 39]
        self._isShow_ids = []

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._temperature_id:
                temperature = self._random_temperature()
                f['fields'][0]['values'][0]['val'] = temperature
            elif f['id'] == self._day_id:
                today = self._t.today
                if f['fields'][0]['values'][0]['val'].startswith(today):
                    self._result = '%s今日%s已填报过%s' % (self._username_masked, today, self._reporter_name)
                    raise Exception(self._result)
                else:
                    f['fields'][0]['values'][0]['val'] = today
            elif f['id'] == self._report_time_id:
                report_time = self._t.report_time
                f['fields'][0]['values'][0]['val'] = report_time
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False

        self._today_form_data = form_data
        return form_data
