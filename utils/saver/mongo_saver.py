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
        assert data_type in ['search', 'detail', 'review']
        if data_type == 'search':
            self.save_search_list(data)
        elif data_type == 'detail':
            self.save_detail_list(data)
        elif data_type == 'review':
            self.save_review_list(data)
        else:
            raise Exception

    def save_search_list(self, data):
        """
        保存搜索结果
        :param data:
        :return:
        """
        data_list = []
        for each in data:
            data_dict = {
                '店铺id': each[0],
                '店铺名称': each[1],
                '店铺评分': each[2],
                '评论数量': each[3],
                '平均价格': each[4],
                '标签1': each[5],
                '标签2': each[6],
                '地址': each[7],
                '推荐': each[8],
                '评分': each[9],
                '图片链接': each[10],
                '详情链接': each[11],

            }
            data_list.append(data_dict)
        col = self.database['info']
        for each in data_list:
            col.delete_many({'店铺id': each['店铺id']})
        col.insert(data_list)
        pass

    def save_detail_list(self, data):
        """
        保存详细结果
        :param data:
        :return:
        """
        data_list = []
        for each in data:
            data_dict = {
                '店铺id': each[0],
                '店铺名称': each[1],
                '评论数量': each[2],
                '平均价格': each[3],
                '评分': each[4],
                '地址': each[5],
                '电话': each[6],
                '其他信息': each[7],

            }
            data_list.append(data_dict)
        col = self.database['info_detail']

        for each in data_list:
            col.delete_many({'店铺id': each['店铺id']})
        col.insert(data_list)

    def save_review_list(self, data):
        """
        保存评论数据
        :param data:
        :return:
        """
        data_list = []
        for each in data:
            data_dict = {
                '评论id': each[0],
                '店铺id': each[1],
                '用户名': each[2],
                '打分': each[3],
                '评论': each[4],
                '喜欢': each[5],
                '发布时间': each[6],

            }
            data_list.append(data_dict)
        col = self.database['review']
        for each in data_list:
            col.delete_many({'评论id': each['评论id']})
        col.insert(data_list)
