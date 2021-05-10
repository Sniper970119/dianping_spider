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


class Search():
    def __init__(self):
        pass

    def search(self, search_url, request_type='search'):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        r = requests_util.get_requests(search_url, request_type=request_type)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密文件
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        shop_all_list = html.select('.shop-list')[0].select('li')

        search_res = []
        for shop in shop_all_list:
            try:
                image_path = shop.select('.pic')[0].select('a')[0].select('img')[0]['src']
            except:
                image_path = '-'
            try:
                shop_id = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['data-shopid']
            except:
                shop_id = '-'
            try:
                detail_url = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['href']
            except:
                detail_url = '-'
            try:
                name = shop.select('.txt')[0].select('.tit')[0].select('a')[0].text.strip()
            except:
                name = '-'
            # 两个star方式，有的页面显示详细star分数，有的显示icon
            # 解析icon
            try:
                star_point = \
                    shop.select('.txt')[0].select('.comment')[0].select('.star_icon')[0].select('span')[0]['class'][
                        1].split('_')[1]
                star_point = float(star_point) / 10
                star_point = str(star_point)
            except:
                star_point = '-'
            # 解析详细star
            try:
                star_point = \
                    shop.select('.txt')[0].select('.comment')[0].select('.star_score')[0].text
                star_point = float(star_point)
                star_point = str(star_point)
            except:
                pass
            try:
                review_number = shop.select('.txt')[0].select('.comment')[0].select('.review-num')[0].text.replace(
                    '\n', '')
            except:
                review_number = '-'
            try:
                mean_price = shop.select('.txt')[0].select('.comment')[0].select('.mean-price')[0].select('b')[
                    0].text
            except:
                mean_price = '￥0'
            try:
                tags = shop.select('.txt')[0].select('.tag-addr')[0].select('.tag')
                tag1 = tags[0].text.replace('\n', ' ').strip()
                tag2 = tags[1].text.replace('\n', ' ').strip()
            except:
                tag1 = '-'
                tag2 = '-'
            try:
                addr = shop.select('.txt')[0].select('.tag-addr')[0].select('.addr')[0].text.replace('\n',
                                                                                                     ' ').strip()
            except:
                addr = '-'
            try:
                recommend = shop.select('.recommend')[0].text.replace('\n', ' ').strip()
            except:
                recommend = '-'
            try:
                comment_list = shop.select('.comment-list')[0].text.replace('\n', ' ').strip()
            except:
                comment_list = '-'
            one_step_search_res = {
                '商铺id': shop_id,
                '商铺名': name,
                '评论个数': review_number,
                '人均价格': mean_price,
                '标签1': tag1,
                '标签2': tag2,
                '商铺地址': addr,
                '详情链接': detail_url,
                '图片链接': image_path,
                '详细评分': comment_list,
                '推荐菜': recommend,
                '店铺均分': star_point,
            }
            search_res.append(one_step_search_res)
            yield one_step_search_res
        # return search_res
