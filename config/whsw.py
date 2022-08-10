# -*- coding: utf8 -*-
from config import _Report


class WHSWHealthReport(_Report):
    """
    此为示例报表，请勿直接使用
    以下的变量都需要适配修改，可能需要根据实际情况增加或只需要部分变量，
    请前往 https://hbte.ch/1968.html 查看如何适配，并自行修改
    修改后可在 GitHub 上提 Pull Request
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)
        '''↓↓↓↓↓↓↓↓↓↓修改此处的form id、enc以及打卡名称↓↓↓↓↓↓↓↓↓↓↓'''
        self._form_id = '174267'
        self._enc = '2ea539d84f23c7852a021ed77008df9f'
        self._reporter_name = '20软件三班小郭健康打卡示例'
        '''↑↑↑↑↑↑↑↑↑↑修改此处的form id、enc以及打卡名称↑↑↑↑↑↑↑↑↑↑↑'''

        '''↓↓↓↓↓↓↓↓↓↓粘贴修改以下内容↓↓↓↓↓↓↓↓↓↓↓'''
        self._day_id = 62
        self._report_time_id = -1
        self._temperature_ids = [8]
        self._options_ids = [8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 38, 50, 55]
        self._hasAuthority_ids = [1, 7, 37, 49]
        self._isShow_ids = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 39, 41, 42, 43, 54]
        '''↑↑↑↑↑↑↑↑↑↑粘贴修改以上内容↑↑↑↑↑↑↑↑↑↑↑'''

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
