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
import sys

from utils.config import global_config
from utils.logger import logger


class MongoSaver():
    def __init__(self):
        mongo_url = global_config.get('config', 'mongo_path')
        try:
            import pymongo
            client = pymongo.MongoClient(mongo_url)
            self.database = client['dianping']
        except:
            logger.warning(
                u'系统中可能没有安装或启动MongoDB数据库，请先根据系统环境安装或启动MongoDB，再运行程序')
            sys.exit()

    def save_data(self, data, data_type):
        """
        保存数据
        :param data:
        :param data_type:
        :return:
        """
        assert data_type in ['search', 'detail', 'comment']
        if data_type == 'search':
            self.save_search_list(data)
        elif data_type == 'detail':
            self.save_detail_list(data)
        elif data_type == 'comment':
            self.save_comment_list(data)
        else:
            raise Exception

    def save_search_list(self, data):
        """
        保存搜索结果
        :param data:
        :return:
        """
        # Todo 判断重复，存数据
        col = self.database['info']
        col.find({'id': data})
        pass

    def save_detail_list(self, data):
        """
        保存详细结果
        :param data:
        :return:
        """
        # Todo 判断重复，存数据
        col = self.database['info_detail']
        pass

    def save_comment_list(self, data):
        """
        保存评论数据
        :param data:
        :return:
        """
        # Todo 判断重复，存数据
        col = self.database['comment']
        pass
