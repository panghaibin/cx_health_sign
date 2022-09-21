# -*- coding: utf8 -*-
from config import _Report


class SDPUHealthReport(_Report):
    """
    SDPU Health Report
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)
        self._form_id = '211393'
        self._enc = '4e585485d0b21ac1b15b6701b7c01f49'
        self._reporter_name = 'SDPU打卡'

        self._day_id = 52
        self._report_time_id = -1
        self._temperature_ids = [5, 22, 23]
        self._options_ids = [62, 64, 65, 32, 6, 29, 16, 66, 67, 68]
        self._hasAuthority_ids = [38, 52, 34, 5, 22, 23, 35, 36, 49, 37, 54, 57, 59, 39, 14, 19, 56, 58, 61, 60]
        self._isShow_ids = [33, 28, 27, 31, 16, 67, 69, 68, 70]

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._day_id:
                # 打卡日期
                today = self._t.today
                if f['fields'][0]['values'][0]['val'] == today:
                    # 如果获取到上次的打卡时间是今天的，则不需要再次填报
                    self._result = '%s今日%s已填报过%s' % (self._username_masked, today, self._reporter_name)
                    raise Exception(self._result)
                else:
                    f['fields'][0]['values'][0]['val'] = today
            elif f['id'] == self._report_time_id:
                # 打卡时间
                today = self._t.today
                report_time = self._t.report_time
                if f['fields'][0]['values'][0]['val'].startswith(today):
                    # 同上
                    self._result = '%s今日%s已填报过%s' % (self._username_masked, today, self._reporter_name)
                    raise Exception(self._result)
                else:
                    f['fields'][0]['values'][0]['val'] = report_time
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
