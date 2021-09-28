# -*- coding: utf8 -*-
import re
import json
import requests


class Report(object):
    """
    通用填报模板
    需要继承该类，重写 _form_id, _enc, _clean_form_data() 后使用
    """
    def __init__(self, username, password, school_id=''):
        """
        :params username: 手机号、邮箱或学号
        :params password: 密码
        :params school_id: 学校代码，使用学号登录才需填写
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.125 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self._username = username
        self._password = password
        self._school_id = school_id
        self._session = requests.session()
        self._session.headers = headers

        self._form_id = ''
        self._enc = ''
        self._reporter_name = '通用模板'
        self._result = ''
        self._last_form_data = {}
        self._today_form_data = {}
        self._check_code = ''
        self._today_report_result = {}

    def _login(self):
        """
        登录: 支持手机和邮箱登录
        """
        login_api = "https://passport2.chaoxing.com/api/login"
        params = {
            "name": self._username,
            "pwd": self._password,
            "verify": "0",
            "schoolid": self._school_id if self._school_id else ""
        }
        resp = self._session.get(login_api, params=params)

        if resp.status_code == 403:
            raise Exception("403，登录请求被拒绝")

        data = json.loads(resp.text)
        if not data['result']:
            self._result = '登录失败'
            raise Exception(self._result)
        return data

    def _get_last_form_data(self) -> dict:
        """
        获取上次提交的健康信息
        """
        params = {
            "cpage": "1",
            "formId": self._form_id,
            "enc": self._enc,
            "formAppId": ""
        }
        # api = 'http://office.chaoxing.com/data/apps/forms/fore/user/list'
        api = 'http://office.chaoxing.com/data/apps/forms/fore/forms/user/last/info'
        resp = self._session.get(api, params=params)
        raw_data = json.loads(resp.text)
        if not raw_data['data']:
            self._result = '获取上次提交数据为空，可能为今日已提交'
            raise Exception(self._result)
        form_data = raw_data['data']['formsUser']['formData']
        d = {
            "inDetailGroupIndex": -1,
            "fromDetail": False,
            "isShow": True,
            "hasAuthority": True
        }
        for f in form_data:
            f.update(d)
        self._last_form_data = form_data
        return self._last_form_data

    def _clean_form_data(self):
        """
        子类继承后重写该函数，用于提交数据的修改
        例如修改提交日期为当日，随机体温等
        """
        self._today_form_data = self._last_form_data

    def _get_check_code(self):
        """
        访问表单页面，并获取 check code
        """
        params = {
            'id': self._form_id,
            'enc': self._enc
        }
        form_url = "http://office.chaoxing.com/front/web/apps/forms/fore/apply"
        resp = self._session.get(form_url, params=params)
        code = re.findall(r"checkCode.*'(.*)'", resp.text)
        if code:
            self._check_code = code[0]
            return self._check_code
        else:
            self._result = "校验码获取失败"
            raise Exception(self._result)

    def _today_report(self):
        """
        上报今日信息
        """
        save_api = "http://office.chaoxing.com/data/apps/forms/fore/user/save?lookuid=127973604"
        form_data = json.dumps(self._today_form_data)
        data = {
            "gatherId": "0",
            "formId": self._form_id,
            "formAppId": "",
            "version": "5",
            "checkCode": self._check_code,
            "enc": self._enc,
            "formData": form_data
        }
        resp = self._session.post(save_api, data=data)
        self._today_report_result = json.loads(resp.text)
        return self._today_report_result

    def report(self):
        self._login()
        self._get_last_form_data()
        self._clean_form_data()
        self._get_check_code()
        report_result = self._today_report()
        if report_result['success']:
            self._result = '%s填报%s(id=%s)成功' % (self._username, self._reporter_name, self._form_id)
        return self._result
