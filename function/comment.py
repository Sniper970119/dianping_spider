# coding=gbk

import re
import requests
import json
from faker import Factory
from utils.config import global_config
from utils.saver.saver import Saver


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
        headers = self.get_header()
        r = requests.get('http://www.dianping.com/shop/' + shop_id + '/review_all', headers=headers)
        page_count = '"PageLink" title="(.*?)"'
        page_count = re.findall(page_count, r.text, re.S)
        return page_count[-1]

    def get_comment(self, shop_id):
        headers = self.get_header()
        count = self.get_page_count(shop_id)
        for c in range(1, count+1):
            r = requests.get('http://www.dianping.com/shop/' + shop_id + '/review_all/p' + str(c), headers=headers)
            with open('./review_font_map.json', 'r', encoding='utf8') as f:
                hash_map = json.load(f)
            comment_match = '<div class="review-words Hide">(.*?)<div class="less-words">'
            res = re.findall(comment_match, r.text, re.S)
            for i in range(len(res)):
                for k, v in hash_map.items():
                    s = '<svgmtsi class="' + k + '"></svgmtsi>'
                    res[i] = res[i].replace(s, v)
                emoji = '&#x.{2};'
                temp = re.findall(emoji, res[i], re.S)
                for j in temp:
                    res[i] = res[i].replace(j, '')
                print(res[i])

