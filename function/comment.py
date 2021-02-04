# coding=gbk

import re
import json
from faker import Factory
from utils.config import global_config
from utils.saver.saver import Saver
from utils.requests_utils import requests_util


class Comment:
    def __init__(self):
        self.cookie = global_config.getRaw('config', 'cookie')
        self.ua = global_config.getRaw('config', 'user-agent')
        self.location_id = global_config.getRaw('config', 'location_id')
        self.ua_engine = Factory.create()
        self.saver = Saver()

    def get_header(self):
        if self.ua is not None:
            ua = self.ua
        else:
            ua = self.ua_engine.user_agent()
        header = {
            'User-Agent': ua,
            'Cookie': self.cookie
        }
        return header

    def get_page_count(self, shop_id):
        r = requests_util.get_requests('http://www.dianping.com/shop/' + shop_id + '/review_all', need_header=True)
        page_count = '"PageLink" title="(.*?)"'
        page_count = re.findall(page_count, r.text, re.S)
        return int(page_count[-1])

    # ȡ����ÿһ�����۵�block��ɵ�list
    def get_each_comment_block(self, shop_id):
        count = self.get_page_count(shop_id)
        for c in range(1, count+1):
            url = 'http://www.dianping.com/shop/' + shop_id + '/review_all/p' + str(c)
            r = requests_util.get_requests(url=url, need_header=True)
            block_list = r.text.split('<div class="main-review">')[1:]
            for block in block_list:
                self.get_comment_info(block)

    # ��ÿһ��block����ȡ��Ϣ
    def get_comment_info(self, block):
        comment_match = '<div class="review-words Hide">(.*?)<div class="less-words">'
        name_match = '<div class="dper-info">(.*?)</div>'
        avg_match = '�˾���(.*?)<'
        taste_match = '��ζ��(.*?)<'
        environment_match = '������(.*?)<'
        service_match = '����(.*?)<'
        ingredient_match = 'ʳ�ģ�(.*?)<'
        favorite_match = 'ϲ���Ĳˣ�(.*?)</div>'
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
            print('�û��ǳ�:' + name)
        else:
            print('�û��ǳ�:��')
        if score:
            score = int(score[0])
            print('����:' + str(score//10) + '��')
        else:
            print('����:��')
        if avg:
            avg = avg[0]
            print('�˾�:' + avg)
        else:
            print('�˾�:��')
        if comment:
            print('����:' + comment[0][2:].strip())
        else:
            print('����:��')
        if taste:
            print('��ζ:' + taste[0].strip()[:-2])
        else:
            print('��ζ:��')
        if environment:
            print('����:' + environment[0].strip()[:-2])
        else:
            print('����:��')
        if service:
            print('����:' + service[0].strip()[:-2])
        else:
            print('����:��')
        if ingredient:
            print('ʳ��:' + ingredient[0].strip()[:-2])
        else:
            print('ʳ��:��')
        if favorite:
            favorite = self.get_fav(favorite[0])
            print('ϲ���Ĳ�:', favorite)
        else:
            print('ϲ���Ĳ�:��')
        if reply:
            reply = reply[0][1:].strip()
            print('�̼һظ�:' + reply)
        else:
            print('�̼һظ�:��')
        if time:
            time = time[0][1:].strip().replace('&nbsp;', '').replace('\n', '')
            print('����ʱ��:' + time)

    def get_name(self, name_str):
        name_match = '>(.*?)<'
        name = re.findall(name_match, name_str, re.S)[0]
        return name.strip()

    def get_fav(self, fav_str):
        fav_match = '>(.*?)<'
        fav = re.findall(fav_match, fav_str)
        return fav

