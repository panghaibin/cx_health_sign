# -*- coding: utf8 -*-
from config import _Report


class TestReport(_Report):
    """
    这个表单是在网上随便找的，不限填报次数、时间
    拿来用作测试用
    随时可能失效
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)
        self._form_id = '13243'
        self._enc = '3a9416c86432c5f667f2b23a88a0123a'
        self._reporter_name = '测试用填报表单'

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] == 15:
                f['hasAuthority'] = False
            elif f['id'] == 12:
                # 此处可修改填报的值
                f['fields'][0]['values'][0]['val'] = '.'
        self._today_form_data = form_data
        return form_data
