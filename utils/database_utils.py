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

from utils.logger import logger
from utils.spider_config import spider_config


class DataBaseUtils():
    def __init__(self):
        mongo_url = spider_config.MONGO_PATH
        try:
            import pymongo
            client = pymongo.MongoClient(mongo_url)
            self.database = client['dianping']
            self.col = self.database['info']

        except:
            logger.warning(
                u'系统中可能没有安装或启动MongoDB数据库，请先根据系统环境安装或启动MongoDB，再运行程序')
            sys.exit()

    def get_no_detail(self):
        """
        获取没有爬取detail的条数
        """
        res = []
        data = self.col.find()
        for each in data:
            if data['detail'] == 0:
                res.append(each)
        return res

    def update_no_detail(self, sid):
        """
        更新数据库信息
        """
        self.col.update({'店铺id': sid}, {"$set": {"detail": 1}})
        pass

    def get_no_review(self):
        """
        获取没有爬取review的条数
        """
        res = []
        data = self.col.find()
        for each in data:
            if data['review'] == 0:
                res.append(each)
        return res
        pass

    def update_no_review(self, sid):
        """
        更新数据库信息
        """
        self.col.update({'店铺id': sid}, {"$set": {"review": 1}})
