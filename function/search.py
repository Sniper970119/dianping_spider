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
import requests
from faker import Factory
from bs4 import BeautifulSoup

from utils.logger import logger
from utils.config import global_config
from utils.get_file_map import get_map
from utils.get_font_map import get_search_map_file
from utils.saver.saver import Saver
from utils.requests_utils import requests_util


class Search():
    def __init__(self):
        self.cookie = global_config.getRaw('config', 'cookie')
        self.ua = global_config.getRaw('config', 'user-agent')
        self.location_id = global_config.getRaw('config', 'location_id')
        self.ua_engine = Factory.create()
        self.saver = Saver()
        self.requests_util = requests_util

    def update_font_map(self):
        """
        更新字体信息
        :return:
        """
        self.shopNum_map = get_map('./tmp/shopNum.json')
        self.address_map = get_map('./tmp/address.json')
        self.tagName = get_map('./tmp/tagName.json')
        self.reviewTag = get_map('./tmp/reviewTag.json')

    def get_header(self):
        """
        获取请求头
        :return:
        """
        if self.ua is not None:
            ua = self.ua
        else:
            ua = self.ua_engine.user_agent()
        header = {
            'User-Agent': ua,
            'Cookie': self.cookie
        }
        return header

    def search(self, key_word, only_need_first=True, needed_pages=50):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        assert isinstance(key_word, str)
        assert key_word != None or key_word.strip() != ''
        logger.info('开始搜索:' + key_word)
        header = self.get_header()
        for i in range(1, needed_pages + 1):
            # 针对只需要收条的情况，跳出页数循环
            if only_need_first is True and i != 1:
                break
            url = 'http://www.dianping.com/search/keyword/' + str(self.location_id) + '/0_' + str(
                key_word) + '/p' + str(i)
            r = requests_util.get_requests(url)
            # r = requests.get(url, headers=header)
            text = r.text
            # Todo 加密文件是否有必要每次都获取，继续观察
            # 获取加密文件
            get_search_map_file(text)
            # 更新加密映射缓存
            self.update_font_map()

            # 加密字符串替换
            for k, v in self.shopNum_map.items():
                key = str(k).replace('uni', '&#x')
                key = '"shopNum">' + key + ';'
                value = '"shopNum">' + v
                text = text.replace(key, value)

            for k, v in self.address_map.items():
                key = str(k).replace('uni', '&#x')
                key = '"address">' + key + ';'
                value = '"address">' + v
                text = text.replace(key, value)

            for k, v in self.tagName.items():
                key = str(k).replace('uni', '&#x')
                key = '"tagName">' + key + ';'
                value = '"tagName">' + v
                text = text.replace(key, value)

            for k, v in self.reviewTag.items():
                key = str(k).replace('uni', '&#x')
                key = '"reviewTag">' + key + ';'
                value = '"reviewTag">' + v
                text = text.replace(key, value)

            # 网页解析
            html = BeautifulSoup(text, 'lxml')
            logger.info('解析完成:' + key_word)
            shop_all_list = html.select('.shop-list')[0].select('li')

            search_res = []
            for shop in shop_all_list:
                try:
                    image_path = shop.select('.pic')[0].select('a')[0].select('img')[0]['src']
                except:
                    image_path = None
                try:
                    shop_id = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['data-shopid']
                except:
                    shop_id = None
                try:
                    detail_url = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['href']
                except:
                    detail_url = None
                try:
                    name = shop.select('.txt')[0].select('.tit')[0].select('a')[0].text.strip()
                except:
                    name = None
                try:
                    star_point = \
                        shop.select('.txt')[0].select('.comment')[0].select('.star_icon')[0].select('span')[0]['class'][
                            1].split('_')[1]
                except:
                    star_point = None
                try:
                    review_number = shop.select('.txt')[0].select('.comment')[0].select('.review-num')[0].text.replace(
                        '\n', '')
                except:
                    review_number = None
                try:
                    mean_price = shop.select('.txt')[0].select('.comment')[0].select('.mean-price')[0].select('b')[
                        0].text
                except:
                    mean_price = '￥0'
                try:
                    tags = shop.select('.txt')[0].select('.tag-addr')[0].select('.tag')
                    tag1 = tags[0].text
                    tag2 = tags[1].text
                except:
                    tag1 = None
                    tag2 = None
                try:
                    recommend = shop.select('.recommend')[0].text
                except:
                    recommend = None
                try:
                    commend_list = shop.select('.comment-list')[0].text
                except:
                    commend_list = None

                search_res.append(
                    [shop_id, name, star_point, review_number, mean_price, tag1, tag2, recommend, commend_list,
                     image_path,
                     detail_url])
                # 只要首条，跳出
                if only_need_first is True:
                    break
            # 保存数据
            self.saver.save_data(search_res, 'search')
        # Todo 解析信息的保存
        print()
