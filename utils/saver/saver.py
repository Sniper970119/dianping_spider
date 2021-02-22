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
from utils.config import global_config


class Saver():
    """
    存储器
    """

    def __init__(self):
        save_mode = global_config.get('config', 'save_mode')
        self.saver_list = []
        # 构造每个存储方法的存储器
        if 'csv' in save_mode:
            from utils.saver.csv_saver import CSV
            csv_saver = CSV()
            self.saver_list.append(csv_saver)
            pass
        if 'mongo' in save_mode:
            from utils.saver.mongo_saver import MongoSaver
            mongo_saver = MongoSaver()
            self.saver_list.append(mongo_saver)

    def save_data(self, data, data_type):
        """
        保存数据
        :param data:
        :param data_type:
        :return:
        """
        assert data_type in ['search', 'detail', 'review']
        for each in self.saver_list:
            each.save_data(data, data_type)
