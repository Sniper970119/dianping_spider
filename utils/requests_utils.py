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


class RequestsUtils():
    """
    请求工具类，用于完成全部的请求相关的操作，并进行全局防ban sleep
    """

    def __init__(self):
        requests_times = global_config.getRaw('config', 'requests_times')
        self.cookie = global_config.getRaw('config', 'Cookie')
        self.ua = global_config.getRaw('config', 'user-agent')

        self.ua_engine = Factory.create()

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

    def get_requests(self, url, need_header=True):
        """
        获取请求
        :param url:
        :return:
        """
        # 不需要请求头的请求不计入统计（比如字体文件下载）
        if need_header is False:
            r = requests.get(url)
            return r
        # 需要请求头的请求全局监控，全局暂停
        self.global_time += 1
        for each_stop_time in self.stop_times:
            if self.global_time % int(each_stop_time[0]) == 0:
                for i in tqdm(range(int(each_stop_time[1])), desc='全局等待'):
                    time.sleep(1)
                break
        header = self.get_header()
        r = requests.get(url, headers=header)
        return r

    def get_header(self):
        """
        获取请求头
        :return:
        """
        if self.ua is not None:
            ua = self.ua
        else:
            ua = self.ua_engine.user_agent()
        header = {
            'User-Agent': ua,
            'Cookie': self.cookie
        }
        return header

    def replace_html(self, page_source, file_map):
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


requests_util = RequestsUtils()
