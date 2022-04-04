# -*- coding: utf8 -*-
from config import _Report
from config import Time


class _NNNU0HealthReport(_Report):
    """
    NNNU 表单处理总入口
    早午晚检的不同字段 id 在子类中重写，以实现对 form data 的处理
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._t = Time()

        self._day_id = -1
        self._temperature_id = -1
        self._options_ids = []
        self._hasAuthority_ids = []

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == self._day_id:
                today = self._t.today
                # 防止重复填报
                if f['fields'][0]['values'][0]['val'] == today:
                    self._result = '%s今日%s已填报过%s' % (self._username_masked, today, self._reporter_name)
                    raise Exception(self._result)
                else:
                    f['fields'][0]['values'][0]['val'] = today
            elif f['id'] == self._temperature_id:
                temperature = self._random_temperature()
                f['fields'][0]['values'][0]['val'] = temperature
            elif f['id'] in self._options_ids:
                # 下拉项选择改写为 true
                for option in f['fields'][0]['options']:
                    if f['fields'][0]['values'][0]['val'] == option['title']:
                        option['checked'] = True
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False
        self._today_form_data = form_data
        return form_data


class NNNU1HealthReport(_NNNU0HealthReport):
    """
    NNNU 早检
    """
    def __init__(self, username, password, school_id=''):
        _NNNU0HealthReport.__init__(self, username, password, school_id)
        self._form_id = '99778'
        # noinspection SpellCheckingInspection
        self._enc = '5affca1a747445b8d3ec9de92612ecae'
        self._reporter_name = 'NNNU早检表单'

        self._day_id = 21
        self._temperature_id = 15
        self._options_ids = [22, 23, 13]
        self._hasAuthority_ids = [8, 9, 10, 26, 27]


class NNNU2HealthReport(_NNNU0HealthReport):
    """
    NNNU 午检（已废弃）
    """
    def __init__(self, username, password, school_id=''):
        _NNNU0HealthReport.__init__(self, username, password, school_id)
        self._form_id = '99781'
        # noinspection SpellCheckingInspection
        self._enc = 'e4041a9c358a738a1dd8780e8dfeccb6'
        self._reporter_name = 'NNNU午检表单'

        self._day_id = 21
        self._temperature_id = 15
        self._options_ids = [13, 22, 24]
        self._hasAuthority_ids = [8, 9, 10, 25, 28, 32, 29]


class NNNU3HealthReport(_NNNU0HealthReport):
    """
    NNNU 午检（原晚检）
    """
    def __init__(self, username, password, school_id=''):
        _NNNU0HealthReport.__init__(self, username, password, school_id)
        self._form_id = '99783'
        # noinspection SpellCheckingInspection
        self._enc = 'cb9894ce56b7e222cb3eab72d0fed834'
        self._reporter_name = 'NNNU午检表单'

        self._day_id = 21
        self._temperature_id = 29
        self._options_ids = [13, 22, 23]
        self._hasAuthority_ids = [8, 9, 10, 24, 26, 27, 28]


"""
不同时间继承不同的类，实现不同的上报
"""
t = Time()
hour = t.int_hour
minute = t.int_minute
if 7 <= hour <= 11:
    class NNNUHealthReport(NNNU1HealthReport):
        def __init__(self, username, password, school_id=''):
            super().__init__(username, password, school_id)
# elif 11 <= hour <= 14 or hour == 15 and 0 <= minute <= 30:
#     class NNNUHealthReport(NNNU2HealthReport):
#         def __init__(self, username, password, school_id=''):
#             super().__init__(username, password, school_id)
# elif 18 <= hour <= 22 or hour == 23 and 0 <= minute <= 59:
#     class NNNUHealthReport(NNNU3HealthReport):
#         def __init__(self, username, password, school_id=''):
#             super().__init__(username, password, school_id)
elif 14 <= hour <= 18:
    class NNNUHealthReport(NNNU3HealthReport):
        def __init__(self, username, password, school_id=''):
            super().__init__(username, password, school_id)
else:
    class NNNUHealthReport(_NNNU0HealthReport):
        def __init__(self, username, password, school_id=''):
            super().__init__(username, password, school_id)
            self._result = '%s填报%s不在填报时间' % (self._username_masked, self._reporter_name)

        def report(self):
            return self._result
