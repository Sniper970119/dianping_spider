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

from utils.get_font_map import get_search_map_file
from utils.requests_utils import requests_util


class Detail():
    def __init__(self):
        self.requests_util = requests_util

    def get_detail(self, shop_id):
        url = 'http://www.dianping.com/shop/' + str(shop_id)
        r = requests_util.get_requests(url)
        if r.status_code == 403:
            print('检查浏览器，处理验证码,替换cookie，输入y解除限制', 'http://www.dianping.com/shop/' + str(shop_id))
            while input() != 'y':
                import time
                time.sleep(1)
            self.requests_util.update_cookie()
            r = requests_util.get_requests(url)
            # logger.warning('详情页请求被ban')
            # raise Exception
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密字符串
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        """
        解析格式1（一般餐饮居多）
        """
        # 基础信息
        main_info = html.select('.main')[0]

        shop_name = '-'
        review_count = '-'
        avg_price = '-'
        score = '-'
        address = '-'
        phone = '-'
        other_info = '-'
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
                shop_name = '-'
            try:
                brief_info = main_info.select('.brief-info')[0]
                # Todo 单独json接口响应，js加密参数，由后期慢慢解决，但是仍然保留这个字段，其他解析方式有时可以解析这个字段
                # try:
                #     score = brief_info.select('.star-wrapper')[0].select('.mid-score')[0].text.strip()
                # except:
                #     score = None
                try:
                    review_count = brief_info.select('#reviewCount')[0].text.strip()
                except:
                    review_count = '-'
                try:
                    avg_price = brief_info.select('#avgPriceTitle')[0].text.strip()
                except:
                    avg_price = '-'

                # Todo 这个建议使用info中信息，这里的有可能会不准，动态参数由json返回
                # try:
                #     comment_score = brief_info.select('#comment_score')[0].text.strip()
                # except:
                #     comment_score = None

                try:
                    address = main_info.find(attrs={'itemprop': 'street-address'}).text.strip()
                except:
                    address = '-'

                try:
                    phone = main_info.select('.tel')[0].text.strip()
                except:
                    phone = '-'

                try:
                    other_info = main_info.select('.other')[0].text.replace('修改', '').strip()
                except:
                    other_info = '-'
            except:
                # Todo 前台显示手动滑动解锁
                # self.get_detail(shop_id)
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
        except:
            # 切换解析方式
            pass
        """
        解析格式2（一般酒店居多）
        """
        # Todo 这种解析方式没有加密，会在解析加密文件时报错，反正这种格式数量不多，暂时不做更改了
        # if shop_name is '-':
        #     # 名称解析不到，换一种解析方式
        #     try:
        #         base_info = html.select('base-info')[0]
        #         try:
        #             shop_name = base_info.select('.hotel-title')[0].text
        #         except:
        #             shop_name = None
        #         try:
        #             address = base_info.find(attrs={'itemprop': 'address'}).text.strip()
        #         except:
        #             address = None
        #         try:
        #             score = base_info.select('.hotel-scope')[0].select('.score')[0].text
        #         except:
        #             score = None
        #     except:
        #         # Todo 前台显示手动滑动解锁
        #         # self.get_detail(shop_id)
        #         pass
        #     pass
        return [shop_id, shop_name, review_count, avg_price, score, address, phone, other_info]
