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

import os
import sys
import time
import requests
from tqdm import tqdm
from faker import Factory

from utils.config import global_config
from utils.logger import logger
from utils.get_file_map import get_map
from utils.cookie_utils import cookie_cache
from utils.spider_config import spider_config


class RequestsUtils():
    """
    请求工具类，用于完成全部的请求相关的操作，并进行全局防ban sleep
    """

    def __init__(self):
        requests_times = spider_config.REQUESTS_TIMES
        self.cookie = spider_config.COOKIE
        self.ua = spider_config.USER_AGENT
        self.ua_engine = Factory.create()
        if self.ua is None:
            logger.error('user agent 暂时不支持为空')
            sys.exit()

        self.cookie_pool = spider_config.USE_COOKIE_POOL
        if self.cookie_pool is True:
            logger.info('使用cookie池')
            if not os.path.exists('cookies.txt'):
                logger.error('cookies.txt文件不存在')
                sys.exit()

        self.ip_proxy = spider_config.USE_PROXY
        if self.ip_proxy:
            self.proxy_pool = []

        try:
            self.stop_times = self.parse_stop_time(requests_times)
        except:
            logger.error('配置文件requests_times解析错误，检查输入（必须英文标点）')
            sys.exit()
        self.global_time = 0

    def create_dir(self, file_name):
        """
        创建文件夹
        :param file_name:
        :return:
        """
        if os.path.exists(file_name):
            return
        else:
            os.mkdir(file_name)

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
        assert request_type in ['no header', 'no proxy, cookie', 'no proxy, no cookie', 'proxy, no cookie',
                                'proxy, cookie']

        # 不需要请求头的请求不计入统计（比如字体文件下载）
        if request_type == 'no header':
            r = requests.get(url=url)
            return r

        # 所有本地ip的请求都进入全局监控，no header由于只用于字体文件下载，不计入监控
        if 'no proxy' in request_type:
            self.freeze_time()

            if request_type == 'no proxy, no cookie':
                r = requests.get(url, headers=self.get_header(cookie=None, need_cookie=False))

            if request_type == 'no proxy, cookie':
                cur_cookie = self.get_cookie(url)
                r = requests.get(url, headers=self.get_header(cookie=cur_cookie, need_cookie=True))

            return self.handle_verify(r=r, url=url, request_type=request_type)

        """
        下面两个虽然标记使用代理，但是依然判断。
        使用这种标记的意味着这些请求可以由代理完成，但是理所应当可以不用代理。
        当然，建议使用代理。
        """
        if request_type == 'proxy, no cookie':
            if self.ip_proxy:
                # 这个while是处理代理失效的问题（通常是超时等问题）
                while True:
                    try:
                        r = requests.get(url, headers=self.get_header(None, False), proxies=self.get_proxy())
                        break
                    except:
                        pass
            else:
                r = requests.get(url, headers=self.get_header(None, False))
            return self.handle_verify(r, url, request_type)

        if request_type == 'proxy, cookie':
            # 对于携带cookie的请求，依然计入全局监控
            self.freeze_time()

            cur_cookie = self.get_cookie(url)
            header = self.get_header(cookie=cur_cookie, need_cookie=True)

            if self.ip_proxy:
                while True:
                    try:
                        r = requests.get(url, headers=header, proxies=self.get_proxy())
                        break
                    except:
                        pass
            else:
                r = requests.get(url, headers=header)

            # 对于cookie池的使用，反馈cookie池状态
            if spider_config.USE_COOKIE_POOL and r.status_code != 200:
                if cur_cookie is not None:
                    cookie_cache.change_state(cur_cookie, self.judge_request_type(url))
                    #  失效之后重复调用本方法直至200
                    return self.get_requests(url, request_type)
            else:
                return self.handle_verify(r, url, request_type)
            return self.handle_verify(r, url, request_type)
        # 其他
        raise AttributeError

    def freeze_time(self):
        """
        时间暂停术！
        @return:
        """
        self.global_time += 1
        if self.global_time != 1:
            for each_stop_time in self.stop_times:
                if self.global_time % int(each_stop_time[0]) == 0:
                    for i in tqdm(range(int(each_stop_time[1])), desc='全局等待'):
                        import random
                        sleep_time = 1 + (random.randint(1, 10) / 100)
                        time.sleep(sleep_time)
                    break

    def handle_verify(self, r, url, request_type):
        if 'verify' in r.url:
            """
            不管是使用真实ip还是真实cookie，都对验证码进行处理
            这里有一个特例，就是cookie池到底处不处理验证码，如果处理，
            一定程度上丧失了cookie池的意义，如果不处理，失效的太快。
            暂时处理
            """
            if request_type is not 'proxy, no cookie' or not spider_config.USE_PROXY:
                print('处理验证码，按任意键回车后继续', r.url)
                input()
            else:
                print('verify')
            return self.get_requests(url, request_type)
        else:
            return r

    def get_cookie(self, url):
        """
        获取cookie
        @return:
        """
        if spider_config.USE_COOKIE_POOL:
            while True:
                cur_cookie = cookie_cache.get_cookie(mission_type=self.judge_request_type(url))
                if cur_cookie is not None:
                    break
                logger.info('所有cookie均已失效，替换（替换后会自动继续）或等待解封')
                time.sleep(60)
        else:
            cur_cookie = self.cookie
        return cur_cookie

    def judge_request_type(self, url):
        """
        判断请求类型，由于cookie池是分开维护的，搜索、详情、评论也不是一起被ban的，
        需要对每个cookie的每个页面进行分类
        @param url:
        @return:
        """
        if 'shop' in url:
            return 'detail'
        elif 'review' in url:
            return 'review'
        else:
            return 'search'

    def get_header(self, cookie, need_cookie=True):
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

        if need_cookie:
            header = {
                'User-Agent': ua,
                'Cookie': cookie
            }
        else:
            header = {
                'User-Agent': ua,
            }
        return header

    def get_proxy(self):
        """
        获取代理
        """
        repeat_nub = spider_config.REPEAT_NUMBER
        # http 提取模式
        if spider_config.HTTP_EXTRACT:
            # 代理池为空，提取代理
            if len(self.proxy_pool) == 0:
                proxy_url = spider_config.HTTP_LINK
                r = requests.get(proxy_url)
                r_json = r.json()
                for proxy in r_json:
                    # 重复添加，多次利用
                    for _ in range(repeat_nub):
                        self.proxy_pool.append([proxy['ip'], proxy['port']])
            # 获取ip
            proxies = self.http_proxy_utils(self.proxy_pool[0][0], self.proxy_pool[0][1])
            self.proxy_pool.remove(self.proxy_pool[0])
            return proxies
        # 秘钥提取模式
        elif spider_config.KEY_EXTRACT:
            pass
        pass

    def http_proxy_utils(self, ip, port):
        """
        专属http链接的代理格式
        @param ip:
        @param port:
        @return:
        """
        proxyMeta = "http://%(host)s:%(port)s" % {

            "host": ip,
            "port": port,
        }

        proxies = {

            "http": proxyMeta,
            "https": proxyMeta
        }
        return proxies

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

    def replace_json_text(self, json_text, file_map):
        """
        替换json文本，根据加密字体文件映射替换json加密文本
        :param page_source:
        :param file_map:
        :return:
        """
        for k_f, v_f in file_map.items():
            font_map = get_map(v_f)
            for k, v in font_map.items():
                key = str(k).replace('uni', '&#x')
                key = '\\"' + str(k_f) + '\\">' + key + ';'
                value = '\\"' + str(k_f) + '\\">' + v
                json_text = json_text.replace(key, value)
        return json_text

    def update_cookie(self):
        self.cookie = global_config.getRaw('config', 'Cookie')


requests_util = RequestsUtils()
