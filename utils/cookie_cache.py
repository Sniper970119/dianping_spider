# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""

import schedule


class CookieCache():
    def __init__(self):
        self.all_cookie = []
        self.valid_cookie = []
        self.invalid_cookie = []

    def init_cookie(self):
        """
        初始化cookie，读取文件中cookie信息，添加review、detail标记
        """
        with open('cookies.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            # cookie detail_valid_tag   review_valid_tag
            self.all_cookie.append([line, 0, 0])

    def check_cookie(self):
        """
        检查cookie，定时任务，恢复&去掉 review、detail标记
        """
        review_test_url = 'http://www.dianping.com/shop/F8oeMhRBwBa99Z70/review_all/p34'
        detail_test_url = 'http://www.dianping.com/shop/G1PUPaOlLNpU8Z1h'
        for cookie in self.all_cookie:
            pass

    def timing_check(self):
        """
        定时任务，用于定时启动check_cookie
        :return:
        """
        schedule.every().minute.at('00:00').do(self.check_cookie)
        while True:
            schedule.run_pending()

    def get_cookie(self, mission_type):
        """
        获取cookie
        :param mission_type: 获取cookie所用于的任务
        :return:
        """
        assert mission_type in ['review', 'detail']

    def change_state(self, cookie, mission_type):
        """
        修改cookie状态
        :param cookie:
        :param mission_type:
        :return:
        """
        pass


cookie_cache = CookieCache()
