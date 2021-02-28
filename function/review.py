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
from utils.get_font_map import get_review_map_file
from utils.requests_utils import requests_util


class Review():
    def __init__(self):
        self.requests_util = requests_util
        self.pages_needed = global_config.getRaw('save', 'review_pages')
        pass

    def get_review(self, shop_id):
        all_pages = -1
        cur_pages = 1
        all_review = []
        while all_pages == -1 or all_pages > 0:
            url = 'http://www.dianping.com/shop/' + str(shop_id) + '/review_all/p' + str(cur_pages)
            # 访问p1会触发验证码，因此对第一页单独处理
            if cur_pages == 1:
                url = 'http://www.dianping.com/shop/' + str(shop_id) + '/review_all'
            r = requests_util.get_requests(url)
            if r.status_code == 403:
                logger.warning('评论页请求被ban')
                raise Exception

            text = r.text
            # 获取加密文件
            file_map = get_review_map_file(text)
            # 替换加密字符串
            text = requests_util.replace_review_html(text, file_map)
            html = BeautifulSoup(text, 'lxml')
            # 更新页数
            if all_pages == -1:
                all_pages = min(int(html.select('.reviews-pages')[0].select('a')[-2].text), int(self.pages_needed))

            reviews = html.select('.reviews-items')[0].select('.main-review')
            for review in reviews:
                # single_review = []
                try:
                    user_name = review.select('.name')[0].text.strip()
                except:
                    user_name = '-'
                try:
                    score = review.select('.score')[0].text.replace(' ', '').replace('\n', ' ').strip()
                except:
                    score = '-'
                try:
                    review_text = review.select('.review-words')[0].text.replace(' ', ''). \
                        replace('收起评价', '').replace('\r', ' ').replace('\n', ' ').strip()
                except:
                    review_text = '-'
                try:
                    like = review.select('.review-recommend')[0].text.replace(' ', '').\
                        replace('\r', ' ').replace('\n', ' ').strip()
                except:
                    like = '-'
                try:
                    time = review.select('.time')[0].text.strip()
                except:
                    time = '-'
                try:
                    review_id = review.select('.actions')[0].select('a')[0].attrs['data-id']
                except:
                    review_id = '-'
                all_review.append([review_id, shop_id, user_name, score, review_text, like, time])
            cur_pages += 1
            all_pages -= 1
        return all_review
