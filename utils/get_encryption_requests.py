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
import json
import zlib
import base64
import time
import datetime
from bs4 import BeautifulSoup

from utils.requests_utils import requests_util
from utils.cache import cache
from utils.logger import logger

from function.detail import Detail


def get_token(shop_url):
    ts = int(time.time() * 1000)
    cts = int(time.time() * 1000) - 600
    tokens = str({"rId": '100041', "ver": "1.0.6", "ts": ts, "cts": cts, "brVD": [1920, 186],
                  "brR": [[1920, 1080], [1920, 1040], 24, 24], "bI": [shop_url, shop_url],
                  "mT": ["1244,588"], "kT": [], "aT": [], "tT": [], "aM": "",
                  "sign": "eJxTKs7IL/BMsTU2NTAwMLVUAgApvgRP"}).encode()
    _token = zlib.compress(tokens)
    token = base64.b64encode(_token).decode()
    return token


def get_shop_url(shop_id):
    """
    根据shop id 拼接shop url
    @param shop_id:
    @return:
    """
    shop_url = 'http://www.dianping.com/shop/' + str(shop_id)
    return shop_url


def get_font_msg():
    """
    获取加密字体映射文件，如果常规流程，这一步应该是由search中完成并存入缓存。
    如果冷启动，一次search更新缓存
    @return:
    """
    if cache.search_font_map != {}:
        return cache.search_font_map
    else:
        Detail().get_detail('l3BEUN08X4TT52bm', just_need_map=True)
        return cache.search_font_map


def get_basic_hidden_info(shop_id):
    """
    获取基础隐藏信息（名称、地址、电话号、cityid）
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?' \
          'shopId=' + str(shop_id) + '&_token=' + str(get_token(
        shop_url)) + '&tcv=ck9rmnrofg&uuid=6ca1f51a-7653-b987-3cd6-95f3aadb13b8.1619854599&platform=1' \
                     '&partner=150&optimusCode=10&originUrl=' + str(shop_url)
    r = requests_util.get_requests(url, request_type='json')
    r_text = requests_util.replace_json_text(r.text, get_font_msg())
    r_json = json.loads(r_text)
    # 验证码处理
    if r_json['code'] == 406:
        verify_page_url = r_json['customData']['verifyPageUrl']
        logger.warning('处理验证码，按任意键继续：', verify_page_url)
        input()
    elif r_json['code'] == 200:
        msg = r_json['msg']['shopInfo']
        shop_name = msg['shopName']
        shop_address = BeautifulSoup(msg['address'], 'lxml').text + BeautifulSoup(msg['crossRoad'], 'lxml').text
        shop_number = BeautifulSoup(msg['phoneNo'], 'lxml').text + BeautifulSoup(msg['phoneNo2'], 'lxml').text
        return [shop_name, shop_address, shop_number]
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')


def get_review_and_star(shop_id):
    """
    获取评分、人均，评论数
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?shopId=' + str(
        shop_id) + '&cityId=19&mainCategoryId=2821&_token=' + str(get_token(
        shop_url)) + '&uuid=38af1c67-4a50-3220-06f6-bf9f16e71c41.1611146098&platform=1&partner=150&optimusCode=10' \
                     '&originUrl=' + shop_url
    r = requests_util.get_requests(url, request_type='json')
    r_text = requests_util.replace_json_text(r.text, get_font_msg())
    r_json = json.loads(r_text)
    # 验证码处理
    if r_json['code'] == 406:
        verify_page_url = r_json['customData']['verifyPageUrl']
        logger.warning('处理验证码，按任意键继续：', verify_page_url)
        input()
    elif r_json['code'] == 200:
        shop_base_score = r_json['fiveScore']
        score_title_list = r_json['shopScoreTitleList']
        avg_price = BeautifulSoup(r_json['avgPrice'], 'lxml').text
        review_count = BeautifulSoup(r_json['defaultReviewCount'], 'lxml').text
        score_list = []
        for each in r_json['shopRefinedScoreValueList']:
            score_list.append(BeautifulSoup(each, 'lxml').text)
        scores = ''
        for i, score in enumerate(score_list):
            scores = scores + ' ' + score_title_list[i] + score_list[i]
        return [shop_base_score, scores, avg_price, review_count]
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')


def get_shop_tabs(shop_id):
    """
    获取招牌菜、店铺环境等
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'ttp://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?shopId=' + str(
        shop_id) + '&cityId=19&mainCategoryId=2821&_token=' + str(get_token(
        shop_url)) + '&uuid=38af1c67-4a50-3220-06f6-bf9f16e71c41.1611146098&platform=1&partner=150&optimusCode=10' \
                     '&originUrl=' + shop_url
    r = requests_util.get_requests(url, request_type='json')
    r_text = requests_util.replace_json_text(r.text, get_font_msg())
    r_json = json.loads(r_text)
    # 验证码处理
    if r_json['code'] == 406:
        verify_page_url = r_json['customData']['verifyPageUrl']
        logger.warning('处理验证码，按任意键继续：', verify_page_url)
        input()
    elif r_json['code'] == 200:
        msg = r_json['msg']['shopInfo']
        shop_name = msg['shopName']
        shop_address = BeautifulSoup(msg['address'], 'lxml').text + BeautifulSoup(msg['crossRoad'], 'lxml').text
        shop_number = BeautifulSoup(msg['phoneNo'], 'lxml').text + BeautifulSoup(msg['phoneNo2'], 'lxml').text
        return [shop_name, shop_address, shop_number]
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')


def get_promo_info(shop_id):
    """
    优惠券信息
    @param shop_id:
    @return:
    """
    assert len(shop_id) == len('H2noKWCDigM0H9c1')
    shop_url = get_shop_url(shop_id)
    url = 'ttp://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?shopId=' + str(
        shop_id) + '&cityId=19&mainCategoryId=2821&_token=' + str(get_token(
        shop_url)) + '&uuid=38af1c67-4a50-3220-06f6-bf9f16e71c41.1611146098&platform=1&partner=150&optimusCode=10' \
                     '&originUrl=' + shop_url
    r = requests_util.get_requests(url, request_type='json')
    r_text = requests_util.replace_json_text(r.text, get_font_msg())
    r_json = json.loads(r_text)
    # 验证码处理
    if r_json['code'] == 406:
        verify_page_url = r_json['customData']['verifyPageUrl']
        logger.warning('处理验证码，按任意键继续：', verify_page_url)
        input()
    elif r_json['code'] == 200:
        msg = r_json['msg']['shopInfo']
        shop_name = msg['shopName']
        shop_address = BeautifulSoup(msg['address'], 'lxml').text + BeautifulSoup(msg['crossRoad'], 'lxml').text
        shop_number = BeautifulSoup(msg['phoneNo'], 'lxml').text + BeautifulSoup(msg['phoneNo2'], 'lxml').text
        return [shop_name, shop_address, shop_number]
    else:
        logger.warning('json响应码异常，尝试更改提pr，或者提issue')
