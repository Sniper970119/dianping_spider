# coding=utf-8

import re

from utils.saver.saver import Saver
from utils.requests_utils import requests_util


class Comment:
    def __init__(self):
        self.saver = Saver()

    def get_page_count(self, shop_id):
        """
        获取页数
        :param shop_id:
        :return:
        """
        r = requests_util.get_requests('http://www.dianping.com/shop/' + shop_id + '/review_all', need_header=True)
        page_count = '"PageLink" title="(.*?)"'
        page_count = re.findall(page_count, r.text, re.S)
        return int(page_count[-1])

    def get_each_comment_block(self, shop_id):
        """
        取出由每一个评论的block组成的list
        :param shop_id:
        :return:
        """
        count = self.get_page_count(shop_id)
        for c in range(1, count + 1):
            url = 'http://www.dianping.com/shop/' + shop_id + '/review_all/p' + str(c)
            r = requests_util.get_requests(url=url, need_header=True)
            block_list = r.text.split('<div class="main-review">')[1:]
            for block in block_list:
                self.get_comment_info(block)

    def get_comment_info(self, block):
        """
        从每一个block中提取信息
        :param block:
        :return:
        """
        comment_match = '<div class="review-words Hide">(.*?)<div class="less-words">'
        name_match = '<div class="dper-info">(.*?)</div>'
        avg_match = '人均：(.*?)<'
        taste_match = '口味：(.*?)<'
        environment_match = '环境：(.*?)<'
        service_match = '服务：(.*?)<'
        ingredient_match = '食材：(.*?)<'
        favorite_match = '喜欢的菜：(.*?)</div>'
        score_match = 'sml-rank-stars sml-str(.*?) '
        time_match = '<span class="time">(.*?)</span>'
        reply_match = '<p class="shop-reply-content Hide">(.*?)</p>'
        comment = re.findall(comment_match, block, re.S)
        name = re.findall(name_match, block, re.S)
        taste = re.findall(taste_match, block, re.S)
        environment = re.findall(environment_match, block, re.S)
        service = re.findall(service_match, block, re.S)
        ingredient = re.findall(ingredient_match, block, re.S)
        favorite = re.findall(favorite_match, block, re.S)
        score = re.findall(score_match, block, re.S)
        reply = re.findall(reply_match, block, re.S)
        time = re.findall(time_match, block, re.S)
        avg = re.findall(avg_match, block, re.S)
        if name:
            name = self.get_name(name[0])
            print('用户昵称:' + name)
        else:
            print('用户昵称:无')
        if score:
            score = int(score[0])
            print('评分:' + str(score // 10) + '星')
        else:
            print('评分:无')
        if avg:
            avg = avg[0]
            print('人均:' + avg)
        else:
            print('人均:无')
        if comment:
            print('评论:' + comment[0][2:].strip())
        else:
            print('评论:无')
        # if taste:
        #     print('口味:' + taste[0].strip()[:-2])
        # else:
        #     print('口味:无')
        # if environment:
        #     print('环境:' + environment[0].strip()[:-2])
        # else:
        #     print('环境:无')
        # if service:
        #     print('服务:' + service[0].strip()[:-2])
        # else:
        #     print('服务:无')
        # if ingredient:
        #     print('食材:' + ingredient[0].strip()[:-2])
        # else:
        #     print('食材:无')
        if favorite:
            favorite = self.get_fav(favorite[0])
            print('喜欢的菜:', favorite)
        else:
            print('喜欢的菜:无')
        if reply:
            reply = reply[0][1:].strip()
            print('商家回复:' + reply)
        else:
            print('商家回复:无')
        if time:
            time = time[0][1:].strip().replace('&nbsp;', '').replace('\n', '')
            print('评论时间:' + time)

    def get_name(self, name_str):
        """
        获取用户名
        :param name_str:
        :return:
        """
        name_match = '>(.*?)<'
        name = re.findall(name_match, name_str, re.S)[0]
        return name.strip()

    def get_fav(self, fav_str):
        """
        获取喜欢的菜
        :param fav_str:
        :return:
        """
        fav_match = '>(.*?)<'
        fav = re.findall(fav_match, fav_str)
        return fav

    def get_rank(self, rank_str):
        rank_str = rank_str[2:-2].strip().replace('</span>', '').replace('<span class="item">', ''). \
            replace('\n', '').split()
        return rank_str

