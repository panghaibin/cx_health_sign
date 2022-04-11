# -*- coding: utf8 -*-
import json


class Compare:
    def __init__(self, get_file_path='', post_file_path=''):
        self.get_file_path = get_file_path
        self.post_file_path = post_file_path

        # self.get_form = self.get_get_form()
        self.post_form = self.get_post_form()

    @staticmethod
    def get_json(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_get_form(self):
        json_data = self.get_json(self.get_file_path)
        form_data = json_data['data']['formsUser']['formData']
        return form_data

    def get_post_form(self):
        form_data = self.get_json(self.post_file_path)
        return form_data

    def compare_form(self):
        isShow_ids = []
        hasAuthority_ids = []
        options_ids = []
        temperature_ids = []
        day_id = -1
        report_time_id = -1

        for p_item in self.post_form:
            if not p_item['isShow']:
                isShow_ids.append(p_item['id'])
            if not p_item['hasAuthority']:
                hasAuthority_ids.append(p_item['id'])
            try:
                if len(p_item['fields'][0]['options']) != 0:
                    options_ids.append(p_item['id'])
            except KeyError:
                pass
            try:
                if '体温' in p_item['fields'][0]['label']:
                    temperature_ids.append(p_item['id'])
            except KeyError:
                pass
            try:
                if 'yyyy-MM-dd' == p_item['fields'][0]['fieldType']['format']:
                    day_id = p_item['id']
            except KeyError:
                pass
            try:
                if 'yyyy-MM-dd HH:mm' == p_item['fields'][0]['fieldType']['format']:
                    report_time_id = p_item['id']
            except KeyError:
                pass

        print('# 变量值为 -1 或者 [] 的表示没有找到对应的id，若确认表单中没有这些变量，则不影响使用')
        print('self._day_id =', day_id)
        print('self._report_time_id =', report_time_id)
        print('self._temperature_ids =', temperature_ids)
        print('self._options_ids =', options_ids)
        print('self._hasAuthority_ids =', hasAuthority_ids)
        print('self._isShow_ids =', isShow_ids)


class Run:
    def __init__(self):
        # self.get_file_path = input('请输入get.json文件路径：')
        # self.get_file_path = 'get.json' if self.get_file_path == '' else self.get_file_path
        self.get_file_path = ''
        self.post_file_path = input('请输入文件路径，留空则使用运行目录下的post.json文件：')
        self.post_file_path = 'post.json' if self.post_file_path == '' else self.post_file_path
        if self.post_file_path.startswith('"') and self.post_file_path.endswith('"'):
            self.post_file_path = self.post_file_path[1:-1]

        self.compare = Compare(self.get_file_path, self.post_file_path)
        self.compare.compare_form()


if __name__ == '__main__':
    run = Run()
