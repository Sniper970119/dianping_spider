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

from bs4 import BeautifulSoup

from utils.logger import logger
from utils.config import global_config
from utils.get_file_map import get_map
from utils.get_font_map import get_search_map_file
from utils.saver.saver import Saver
from utils.requests_utils import requests_util


class Detail():
    def __init__(self):
        self.saver = Saver()
        self.requests_util = requests_util

    def get_detail(self, shop_id):
        url = 'http://www.dianping.com/shop/' + str(shop_id)
        r = requests_util.get_requests(url)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密字符串
        text = requests_util.replace_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        # 解析格式1
        # 基础信息
        main_info = html.select('.main')[0]
        try:
            base_info = main_info.select('#basic-info')[0]
            try:
                shop_name = base_info.select('.shop-name')[0].text
                # 过滤标题后缀，例：手机扫码 优惠买单
                remove_a = base_info.select('a')
                for each in remove_a:
                    shop_name = shop_name.replace(each.text, '')
                shop_name = shop_name.strip()
            except:
                shop_name = None
        except:
            pass
        try:
            brief_info = main_info.select('.brief-info')[0]
            try:
                score = brief_info.select('.star-wrapper')[0].select('.mid-score')[0].text.strip()
            except:
                score = None
            try:
                review_count = brief_info.select('#reviewCount')[0].text.strip()
            except:
                review_count = None
            try:
                avg_price = brief_info.select('#avgPriceTitle')[0].text.strip()
            except:
                avg_price = None

            try:
                comment_score = brief_info.select('#comment_score')[0].text.strip()
            except:
                comment_score = None

            try:
                address = main_info.find(attrs={'itemprop': 'street-address'}).text.strip()
            except:
                address = None

            try:
                phone = main_info.select('.tel')[0].text.strip()
            except:
                phone = None

            try:
                other_info = main_info.select('.other')[0].text.strip()
            except:
                other_info = None
        except:
            pass
        # Todo 促销信息 （单独接口 js加密）
        # try:
        #     sale_info = ''
        #     sales = main_info.select('#sales')
        #     for sale in sales:
        #         for tag in sale.select('.item'):
        #             try:
        #                 title = tag.select('.title')[0].text
        #                 price = tag.select('.price')[0].text
        #                 del_price = tag.select('.del-price')[0].text
        #                 sale_info += title + '\t' + price + '\t' + del_price + '\n'
        #             except:
        #                 continue
        # except:
        #     sales = None
        print()
        pass
