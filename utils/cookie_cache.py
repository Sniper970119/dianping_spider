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


class CookieCache():
    def __init__(self):
        self.all_cookie = []
        self.valid_cookie = []
        self.invalid_cookie = []

    def init_cookie(self):
        """
        初始化cookie，读取文件中cookie信息，添加review、detail标记
        """
        pass

    def check_cookie(self):
        """
        检查cookie，定时任务，恢复&去掉 review、detail标记
        """
        review_test_url = 'http://www.dianping.com/shop/F8oeMhRBwBa99Z70/review_all/p34'

        detail_test_url = 'http://www.dianping.com/shop/G1PUPaOlLNpU8Z1h'

    def get_cookie(self, mission_type):
        """
        获取cookie
        :param mission_type: 获取cookie所用于的任务
        :return:
        """
        assert mission_type in ['review', 'detail']


cookie_cache = CookieCache()
