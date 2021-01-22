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

from utils.config import global_config
from utils.get_file_map import get_map


class Search():
    def __init__(self):
        self.cookie = global_config.getRaw('config', 'Cookie')
        self.ua_engine = Factory.create()
        self.word_map = get_map('../files/font_map.json')
        # self.word_map = get_map('./files/font_map.json')
        self.location_map = get_map('../files/location_map.json')
        # self.location_map = get_map('./files/location_map.json')
        pass

    def get_header(self):
        fake_ua = self.ua_engine.user_agent()
        header = {
            'User-Agent': fake_ua,
            'Cookie': self.cookie,
        }
        return header

    def search(self, key_word, need_first_page=True):
        assert isinstance(key_word, str)
        assert key_word != None or key_word.strip() != ''
        header = self.get_header()
        url = 'http://www.dianping.com/search/keyword/19/0_' + str(key_word)
        r = requests.get(url, headers=header)
        html = BeautifulSoup(r.text, 'lxml')


if __name__ == '__main__':
    Search().search('大连一方城堡')
