# -*- coding: utf8 -*-
from config import _Report


class DefaultHealthReport(_Report):
    """
    学习通默认健康上报表单
    _clean_form_data 参考自 GitHub
        https://github.com/mkdir700/chaoxing_auto_sign/blob/bf2255ed59cdbdf0e810e31d07ef6198810fdbe5/heath/main.py
    未验证可用性
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)
        self._form_id = '99783'
        self._enc = 'cb9894ce56b7e222cb3eab72d0fed834'
        self._reporter_name = '学习通健康表单'

    def _clean_form_data(self):
        form_data = self._last_form_data
        not_show = [x for x in range(9, 36) if x % 2 != 0]
        not_show.extend([38, 39, 41, 42])
        for f in form_data:
            if f['id'] == 5:
                f['fields'][0]['tip']['text'] = r"<p+style=\"text-align:+center;\"><span+style=\"font-size:+large" \
                                                r";+font-weight:+bold;\">基本信息</span></p> "
            elif f['id'] == 6:
                f['fields'][0]['tip']['text'] = r"<p+style=\"text-align:+center;\"><span+style=\"font-size:+large" \
                                                r";+font-weight:+bold;\">健康状况</span></p> "
            elif f['id'] == 36:
                f['fields'][0]['tip']['text'] = r"<p+style=\"text-align:+center;\"><span+style=\"font-size:+large" \
                                                r";+font-weight:+bold;\">出行情况</span></p> "
            elif f['id'] == 8:
                f['fields'][0]['values'][0]['val'] = "健康 "
                f['fields'][0]['options'][0]['title'] = "健康 "

            if f['id'] in not_show:
                f['isShow'] = False
            else:
                f['isShow'] = True
        self._today_form_data = form_data
        return form_data
