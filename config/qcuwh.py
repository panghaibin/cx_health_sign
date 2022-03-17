# -*- coding: utf8 -*-
from config import _Report


class QCUWHHealthReport(_Report):
    """
    QCUWH Health Report
    该脚本由他人贡献，本人未充分测试，不保证其可用性
    """
    def __init__(self, username, password, school_id=''):
        _Report.__init__(self, username, password, school_id)

        self._form_id = '7185'
        self._enc = 'f837c93e0de9d9ad82db707b2c27241e'
        self._reporter_name = 'QCUWH健康表单'

        self._options_ids = [7, 8, 43, 46, 52, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 56, 57, 58]
        self._isShow = [9, 48, 49, 47, 53, 54, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]  # 不显示
        self._hasAuthority_ids = [5, 6]
        self._edittext_area = [45]
        """
        56:三针是否龙泉卫生院接种
        57:两针
        58:一针
        同时只出现在一个，val可能不存在
        45选项为未接种原因，当有57或58时候才会显示
        """

    def _clean_form_data(self):
        form_data = self._last_form_data
        for f in form_data:
            if f['id'] in self._options_ids:
                if not f['fields'][0]['values']:  # 没数据，不显示,处理56,57,58
                    f['isShow'] = False
                else:
                    # 下拉项选择改写为 true
                    for option in f['fields'][0]['options']:
                        if f['fields'][0]['values'][0]['val'] == option['title']:
                            option['checked'] = True
            elif f['id'] in self._isShow:
                f['isShow'] = False
            elif f['id'] in self._hasAuthority_ids:
                f['hasAuthority'] = False
            # 这个是文本填写,处理45
            elif f['id'] in self._edittext_area:
                if not f['fields'][0]['values']:  # 没数据，不显示
                    f['isShow'] = False

        self._today_form_data = form_data
        return form_data
