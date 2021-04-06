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

import sys
import time
import requests
from tqdm import tqdm
from faker import Factory

from utils.config import global_config
from utils.logger import logger
from utils.get_file_map import get_map
from utils.cookie_utils import cookie_cache


class RequestsUtils():
    """
    请求工具类，用于完成全部的请求相关的操作，并进行全局防ban sleep
    """

    def __init__(self):
        requests_times = global_config.getRaw('config', 'requests_times')
        self.cookie = global_config.getRaw('config', 'Cookie')
        self.ua = global_config.getRaw('config', 'user-agent')

        self.ua_engine = Factory.create()

        self.cookie_pool = global_config.getRaw('config', 'use_cookie_pool')
        self.cookie_pool = True if self.cookie_pool == 'True' else False

        try:
            self.stop_times = self.parse_stop_time(requests_times)
        except:
            logger.error('配置文件requests_times解析错误，检查输入（必须英文标点）')
            sys.exit()
        self.global_time = 0
        pass

    def parse_stop_time(self, requests_times):
        """
        解析暂停时间
        :param requests_times:
        :return:
        """
        each_stop = requests_times.split(';')
        stop_time = []
        for i in range(len(each_stop) - 1, -1, -1):
            stop_time.append(each_stop[i].split(','))
        return stop_time

    def get_requests(self, url, request_type):
        """
        获取请求
        :param url:
        :return:
        """
        assert request_type in ['search', 'detail', 'review', 'no header']
        # 不需要请求头的请求不计入统计（比如字体文件下载）
        if request_type == 'no header':
            r = requests.get(url)
            return r
        # 需要请求头的请求全局监控，全局暂停
        self.global_time += 1
        for each_stop_time in self.stop_times:
            if self.global_time % int(each_stop_time[0]) == 0:
                for i in tqdm(range(int(each_stop_time[1])), desc='全局等待'):
                    import random
                    sleep_time = 1 + (random.randint(1, 10) / 100)
                    time.sleep(sleep_time)
                # 全局魂系
                break
        if self.cookie_pool is True:
            cookie = cookie_cache.get_cookie(request_type)
        else:
            cookie = None
        header = self.get_header(cookie)
        r = requests.get(url, headers=header)
        return r

    def get_header(self, cookie):
        """
        获取请求头
        :return:
        """
        if self.ua is not None:
            ua = self.ua
        else:
            ua = self.ua_engine.user_agent()

        # cookie选择
        if cookie is None:
            cookie = self.cookie
        header = {
            'User-Agent': ua,
            # 'Host': 'http://www.dianping.com/',
            'Cookie': cookie
        }
        return header

    def replace_search_html(self, page_source, file_map):
        """
        替换html文本，根据加密字体文件映射替换page source加密代码
        :param page_source:
        :param file_map:
        :return:
        """
        for k_f, v_f in file_map.items():
            font_map = get_map(v_f)
            for k, v in font_map.items():
                key = str(k).replace('uni', '&#x')
                key = '"' + str(k_f) + '">' + key + ';'
                value = '"' + str(k_f) + '">' + v
                page_source = page_source.replace(key, value)
        return page_source

    def replace_review_html(self, page_source, file_map):
        """
        替换html文本，根据加密字体文件映射替换page source加密代码
        :param page_source:
        :param file_map:
        :return:
        """
        for k_f, v_f in file_map.items():
            font_map = get_map(v_f)
            for k, v in font_map.items():
                key = str(k).replace('uni', '&#x')
                key = '"' + str(k) + '"><'
                value = '"' + str(k) + '">' + str(v) + '<'
                page_source = page_source.replace(key, value)
        return page_source

    def update_cookie(self):
        self.cookie = global_config.getRaw('config', 'Cookie')


requests_util = RequestsUtils()
