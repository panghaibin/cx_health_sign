# -*- coding: utf8 -*-
from setting import Setting
from config.default import DefaultHealthReport
from config.nnnu import NNNUHealthReport
from config.test import TestReport


if __name__ == '__main__':
    default_user = Setting().get_users(config='default')
    nnnu_user = Setting().get_users(config='nnnu')
    test_user = Setting().get_users(config='test')
    results = []
    for user in default_user:
        try:
            r = DefaultHealthReport(user['username'], user['password'])
            t = r.report()
            results.append(t)
        except Exception as e:
            results.append(e)
    for user in nnnu_user:
        try:
            r = NNNUHealthReport(user['username'], user['password'])
            t = r.report()
            results.append(t)
        except Exception as e:
            results.append(e)
    for user in test_user:
        try:
            r = TestReport(user['username'], user['password'])
            t = r.report()
            results.append(t)
        except Exception as e:
            results.append(e)

    # TODO: 实现消息推送
    print(results)
