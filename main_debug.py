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
from function.search import Search
from utils.config import global_config
from utils.get_font_map import get_review_map_file

cookie = global_config.getRaw('config', 'cookie')
ua = global_config.getRaw('config', 'user-agent')


def get_header():
    """
    获取请求头
    :return:
    """
    header = {
        'User-Agent': ua,
        'Cookie': cookie
    }
    return header


if __name__ == '__main__':
    # Search().search('大连一方城堡', only_need_first=False, needed_pages=1)
    header = get_header()
    url = 'http://www.dianping.com/shop/i24HGIrTSjD3Tcyy/review_all'
    r = requests.get(url, headers=header)
    get_review_map_file(r.text)
