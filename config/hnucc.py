# -*- coding: utf8 -*-
from config import _Report


class HNUCCHealthReport(_Report):
    """
    HNUCC 健康打卡
    """
    def __init__(self, username, password, school_id=''):
        super().__init__(username, password, school_id)
        self._form_id = '86243'
        self._enc = 'de7939f413267efd9a0fd882dca9140b'
        self._reporter_name = 'HNUCC健康打卡'

        self._options_ids = [15, 21, 4, 6, 7, 8, 26, 27]
        self._college_id = 15
        self._classes_ids = [21, 25, 23, 22, 24, 28]

    def _clean_form_data(self):
        """
        表单的<所在班级>存在多个，其可见性 isShow 根据<所在系部>决定
        _college_id 为系部的id，确定其系部对应的班级后将其余班级的 isShow 设置为 False
        """
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] in self._options_ids:
                # 下拉项选择改写为 true
                for option in f['fields'][0]['options']:
                    if f['fields'][0]['values'][0]['val'] == option['title']:
                        option['checked'] = True

        for f in form_data:
            if f['id'] == self._college_id:
                fields_value = f['fields'][0]['values'][0]['val']
                for fields in f['fields'][0]['options']:
                    if fields['title'] == fields_value:
                        self._classes_ids.remove(fields['idArr'][0])

        for f in form_data:
            if f['id'] in self._classes_ids:
                f['isShow'] = False

        self._today_form_data = form_data
        return form_data
