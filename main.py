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

import argparse

from function.search import Search
from utils.config import global_config
from utils.logger import logger

parser = argparse.ArgumentParser()

parser.add_argument('--normal', type=int, required=False, default=1,
                    help='spider as normal(search->detail->review)')
parser.add_argument('--detail', type=int, required=False, default=0,
                    help='spider as custom(just detail)')
parser.add_argument('--review', type=int, required=False, default=0,
                    help='spider as custom(just review)')
parser.add_argument('--shop_id', type=str, required=False, default='',
                    help='custom shop id')
args = parser.parse_args()
if __name__ == '__main__':
    # args.review = 1
    # args.normal = 0
    # args.shop_id = 'l8QDQukrl2tXhzmY'
    if args.normal == 1:
        keyword = global_config.getRaw('detail', 'keyword')
        need_first = True if global_config.getRaw('detail', 'need_first') is 'True' else False
        need_pages = int(global_config.getRaw('detail', 'need_pages'))

        s = Search()
        s.search(keyword, need_first, need_pages)
    if args.detail == 1:
        from function.detail import Detail

        shop_id = args.shop_id
        logger.info('爬取店铺id：' + shop_id + '详情')
        d = Detail()
        d.get_detail(shop_id)
    if args.review == 1:
        from function.review import Review

        shop_id = args.shop_id
        logger.info('爬取店铺id：' + shop_id+ '评论')
        r = Review()
        r.get_review(shop_id)

