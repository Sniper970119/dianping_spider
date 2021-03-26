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


class DataBaseUtils():
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

    def get_no_detail(self):
        pass

    def update_no_detail(self):
        pass

    def get_no_review(self):
        pass

    def update_no_detail(self):
        pass
