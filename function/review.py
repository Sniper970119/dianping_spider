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
from utils.get_font_map import get_review_map_file
from utils.requests_utils import requests_util
from utils.spider_config import spider_config


class Review():
    def __init__(self):
        self.pages_needed = spider_config.NEED_REVIEW_PAGES

    def get_review(self, shop_id):
        all_pages = -1
        cur_pages = 1
        all_review = []
        while all_pages == -1 or all_pages > 0:
            url = 'http://www.dianping.com/shop/' + str(shop_id) + '/review_all/p' + str(cur_pages)
            # 访问p1会触发验证码，因此对第一页单独处理
            if cur_pages == 1:
                url = 'http://www.dianping.com/shop/' + str(shop_id) + '/review_all'
            r = requests_util.get_requests(url, request_type='review')
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
                    like = review.select('.review-recommend')[0].text.replace(' ', ''). \
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
                each_review = {
                    '商铺id': shop_id,
                    '评论id': review_id,
                    '用户名': user_name,
                    '用户打分': score,
                    '评论正文': review_text,
                    '评论点赞': like,
                    '发表时间': time,
                }
                all_review.append(each_review)
            cur_pages += 1
            all_pages -= 1
        # saver.save_data(all_review, 'review')
        return all_review
