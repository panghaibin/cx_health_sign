# -*- coding: utf8 -*-
from config import _Report


class XNECHealthReport4(_Report):
    """
    XNEC Health Report
    """

    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '100989'
        self._enc = 'd854f35d6eb6ee0a700243ac1a4db86b'
        self._reporter_name = 'XNEC午检'

        self._day_id = 21
        self._report_time_id = 35
        self._temperature_ids = [15]
        self._options_ids = []
        self._hasAuthority_ids = [38, 8, 9, 10, 25, 28, 32, 29, 39, 41, 42]
        self._isShow_ids = []

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] in self._temperature_ids:
                temperature = self._random_temperature()
                f['fields'][0]['values'][0]['val'] = temperature
            elif f['id'] == self._day_id:
                f['fields'][0]['values'][0]['val'] = self._t.today
            elif f['id'] == self._report_time_id:
                report_time = self._t.report_time
                f['fields'][0]['values'][0]['val'] = report_time
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False

        self._today_form_data = form_data
        return form_data
