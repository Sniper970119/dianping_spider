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
        self.is_ban = False

    def get_review(self, shop_id, request_type='proxy, cookie', last_chance=False):
        if self.is_ban and spider_config.USE_COOKIE_POOL is False:
            logger.warning('评论页请求被ban，程序继续运行')
            return_data = {
                '店铺id': shop_id,
                '评论摘要': 'ban',
                '评论总数': 'ban',
                '好评个数': 'ban',
                '中评个数': 'ban',
                '差评个数': 'ban',
                '带图评论个数': 'ban',
                '精选评论': 'ban',
            }
            return return_data
        all_pages = -1
        cur_pages = 1
        all_review = []
        while all_pages == -1 or all_pages > 0:
            url = 'http://www.dianping.com/shop/' + str(shop_id) + '/review_all/p' + str(cur_pages)
            # 访问p1会触发验证码，因此对第一页单独处理
            if cur_pages == 1:
                url = 'http://www.dianping.com/shop/' + str(shop_id) + '/review_all'
            r = requests_util.get_requests(url, request_type=request_type)
            # 给一次retry的机会，如果依然403则判断为被ban
            if r.status_code == 403:
                if last_chance is True:
                    self.is_ban = True
                return self.get_review(shop_id=shop_id, request_type=request_type, last_chance=True)

            text = r.text
            # 获取加密文件
            file_map = get_review_map_file(text)
            # 替换加密字符串
            text = requests_util.replace_review_html(text, file_map)
            html = BeautifulSoup(text, 'lxml')
            # 更新页数
            if all_pages == -1:
                # 处理评论只有一页的情况，没有换页按钮无法解析
                try:
                    all_pages = min(int(html.select('.reviews-pages')[0].select('a')[-2].text), int(self.pages_needed))
                except:
                    all_pages = 1
                # 只用解析一次的东西比如评论个数也放这里来
                summaries = []
                try:
                    for summary in html.select('.content')[0].select('span'):
                        try:
                            tag_string = summary.text.strip().replace('\n', '').split()
                            string = tag_string[0]
                            count = tag_string[1][1:-1]
                            summaries.append({
                                '描述': string,
                                '个数': count,
                            })
                        except:
                            pass
                except:
                    pass
                # 各种评论个数
                try:
                    review_with_pic_count = html.select('.filter-pic')[0].select('.count')[0].text[1:-1]
                except:
                    review_with_pic_count = 0
                try:
                    good_review_count = html.select('.filter-good')[0].select('.count')[0].text[1:-1]
                except:
                    good_review_count = 0
                try:
                    mid_review_count = html.select('.filter-middle')[0].select('.count')[0].text[1:-1]
                except:
                    mid_review_count = 0
                try:
                    bad_review_count = html.select('.filter-bad')[0].select('.count')[0].text[1:-1]
                except:
                    bad_review_count = 0
                try:
                    all_review_count = int(good_review_count) + int(mid_review_count) + int(bad_review_count)
                except:
                    all_review_count = '-'

            reviews = html.select('.reviews-items')[0].select('.main-review')
            for review in reviews:
                try:
                    review_username = review.select('.name')[0].text.strip()
                except:
                    review_username = '-'

                try:
                    user_id = review.select('.name')[0]['href'].split('/')[-1]
                except:
                    user_id = '-'

                try:
                    review_score_detail = {}
                    review_avg_price = ''
                    review_score_detail_temp = review.select('.score')[0].text.replace(' ', '').replace('\n',
                                                                                                        ' ').strip().split()
                    for each in review_score_detail_temp:
                        if '人均' in each:
                            review_avg_price = each.split('：')[1].replace('元', '')
                        else:
                            temp = each.split('：')
                            review_score_detail[temp[0]] = temp[1]
                except:
                    review_score_detail = {}
                    review_avg_price = ''

                try:
                    review_text = review.select('.review-words')[0].text.replace(' ', ''). \
                        replace('收起评价', '').replace('\r', ' ').replace('\n', ' ').strip()
                except:
                    review_text = '-'
                try:
                    review_like_dish = review.select('.review-recommend')[0].text.replace(' ', ''). \
                                           replace('\r', ' ').replace('\n', ' ').strip()[5:].split()
                except:
                    review_like_dish = []
                try:
                    review_publish_time = review.select('.time')[0].text.strip()
                except:
                    review_publish_time = '-'
                try:
                    review_id = review.select('.actions')[0].select('a')[0].attrs['data-id']
                except:
                    review_id = '-'

                try:
                    review_pic_list = []
                    review_pic_list_temp = review.select('.review-pictures')[0].select('a')
                    for each in review_pic_list_temp:
                        url = each['href']
                        review_pic_list.append('http://www.dianping.com' + str(url))
                except:
                    review_pic_list = []

                try:
                    review_merchant_reply = review.select('.shop-reply-content')[0].text.strip()
                except:
                    review_merchant_reply = ''

                each_review = {
                    '店铺id': shop_id,
                    '评论id': review_id,
                    '用户id': user_id,
                    '用户名': review_username,
                    '用户打分': review_score_detail,
                    '评论内容': review_text,
                    '人均价格': review_avg_price,
                    '喜欢的菜': review_like_dish,
                    '发布时间': review_publish_time,
                    '商家回复': review_merchant_reply,
                    '评论图片': review_pic_list,
                }
                all_review.append(each_review)
            cur_pages += 1
            all_pages -= 1
        return_data = {
            '店铺id': shop_id,
            '评论摘要': summaries,
            '评论总数': all_review_count,
            '好评个数': good_review_count,
            '中评个数': mid_review_count,
            '差评个数': bad_review_count,
            '带图评论个数': review_with_pic_count,
            '精选评论': all_review,
        }
        return return_data
