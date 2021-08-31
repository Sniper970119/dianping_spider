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
from utils.spider_controller import controller
from utils.config import global_config
from utils.logger import logger
from utils.spider_config import spider_config

parser = argparse.ArgumentParser()

parser.add_argument('--normal', type=int, required=False, default=1,
                    help='spider as normal(search->detail->review)')
parser.add_argument('--detail', type=int, required=False, default=0,
                    help='spider as custom(just detail)')
parser.add_argument('--review', type=int, required=False, default=0,
                    help='spider as custom(just review)')
parser.add_argument('--shop_id', type=str, required=False, default='',
                    help='custom shop id')
parser.add_argument('--need_more', type=bool, required=False, default=False,
                    help='need detail')
args = parser.parse_args()
if __name__ == '__main__':
    if args.normal == 1:
        controller.main()
    if args.detail == 1:
        shop_id = args.shop_id
        logger.info('爬取店铺id：' + shop_id + '详情')
        controller.get_detail(shop_id, detail=args.need_more)
    if args.review == 1:
        shop_id = args.shop_id
        logger.info('爬取店铺id：' + shop_id + '评论')
        controller.get_review(shop_id, detail=args.need_more)
