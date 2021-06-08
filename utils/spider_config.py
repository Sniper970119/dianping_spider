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
from utils.config import global_config, require_config
from utils.logger import logger


class Config():
    """
    全局配置类，不再动态加载
    而是在程序初始化的时候统一加载，各处直接调用
    """

    def __init__(self):
        # config 的 config
        self.USE_COOKIE_POOL = True if global_config.getRaw('config', 'use_cookie_pool') == 'True' else False
        self.COOKIE = global_config.getRaw('config', 'Cookie')
        self.USER_AGENT = global_config.getRaw('config', 'user-agent')
        self.SAVE_MODE = global_config.getRaw('config', 'save_mode')
        self.MONGO_PATH = global_config.getRaw('config', 'mongo_path')
        self.REQUESTS_TIMES = global_config.getRaw('config', 'requests_times')
        self.UUID = global_config.getRaw('config', 'uuid')
        self.TCV = global_config.getRaw('config', 'tcv')

        # config 的 detail
        self.KEYWORD = global_config.getRaw('detail', 'keyword')
        self.LOCATION_ID = global_config.getRaw('detail', 'location_id')
        self.CHANNEL_ID = global_config.getRaw('detail', 'channel_id')
        self.SEARCH_URL = global_config.getRaw('detail', 'search_url')
        assert self.SEARCH_URL == '' or self.SEARCH_URL.endswith('p'), 'search_url 没有拼接p'
        self.NEED_FIRST = True if global_config.getRaw('detail', 'need_first') == 'True' else False
        try:
            self.NEED_SEARCH_PAGES = int(global_config.getRaw('detail', 'need_pages'))
        except:
            logger.error('need_pages 必须为整数')
            exit()

        # config 的 proxy
        self.USE_PROXY = True if global_config.getRaw('proxy', 'use_proxy') == 'True' else False
        if self.USE_PROXY:
            try:
                self.REPEAT_NUMBER = int(global_config.getRaw('proxy', 'repeat_nub'))
            except:
                logger.error('repeat_nub 必须为整数')
                exit()
        else:
            self.REPEAT_NUMBER = 0
        self.HTTP_EXTRACT = True if global_config.getRaw('proxy', 'http_extract') == 'True' else False
        self.HTTP_LINK = global_config.getRaw('proxy', 'http_link')
        self.KEY_EXTRACT = True if global_config.getRaw('proxy', 'key_extract') == 'True' else False
        self.PROXY_HOST = global_config.getRaw('proxy', 'proxy_host').strip()
        self.PROXY_PORT = global_config.getRaw('proxy', 'proxy_port').strip()
        self.KEY_ID = global_config.getRaw('proxy', 'key_id')
        self.KEY_KEY = global_config.getRaw('proxy', 'key_key')
        assert not (self.HTTP_EXTRACT is True and self.KEY_EXTRACT is True), '代理模式不可以全为True'

        # require 的 shop phone
        self.NEED_DETAIL = True if require_config.getRaw('shop_phone', 'need') == 'True' else False
        self.NEED_PHONE_DETAIL = True if require_config.getRaw('shop_phone', 'need_detail') == 'True' else False
        if self.NEED_PHONE_DETAIL:
            logger.warn('开启了电话详情模式，会降低速度并增加反爬概率')

        # require 的 shop review
        self.NEED_REVIEW = True if require_config.getRaw('shop_review', 'need') == 'True' else False
        self.NEED_REVIEW_DETAIL = True if require_config.getRaw('shop_review', 'more_detail') == 'True' else False
        if self.NEED_REVIEW_DETAIL:
            logger.warn('开启了评论详情模式，会降低速度并增加反爬概率')
            try:
                self.NEED_REVIEW_PAGES = int(require_config.getRaw('shop_review', 'need_pages'))
            except:
                logger.error('need_pages 必须为整数')
                exit()
        else:
            self.NEED_REVIEW_PAGES = 0


spider_config = Config()
