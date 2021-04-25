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
from tqdm import tqdm
from bs4 import BeautifulSoup

from function.detail import Detail
from function.review import Review

from utils.logger import logger
from utils.config import global_config
from utils.get_font_map import get_search_map_file
from utils.saver.saver import saver
from utils.requests_utils import requests_util


class Search():
    def __init__(self):
        self.location_id = global_config.getRaw('detail', 'location_id')
        self.channel_id = global_config.getRaw('detail', 'channel_id')
        self.custom_search_url = global_config.getRaw('detail', 'search_url')
        self.need_detail = global_config.getRaw('detail', 'need_detail')
        self.need_comment = global_config.getRaw('detail', 'need_comment')
        self.requests_util = requests_util
        self.jump_wait = False

    def search(self, key_word, only_need_first=True, needed_pages=50):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        # Todo 不需要详情页和评论，只需要首页搜索 不需要cookie
        assert isinstance(key_word, str)
        assert key_word != None or key_word.strip() != ''
        if self.custom_search_url != '':
            key_word = self.custom_search_url
        logger.info('开始搜索:' + key_word)
        # header = self.get_header()
        for i in tqdm(range(1, needed_pages + 1), desc='页数'):
            # 针对只需要收条的情况，跳出页数循环
            if only_need_first is True and i != 1:
                break

            url = 'http://www.dianping.com/search/keyword/' + str(self.location_id) + '/' + str(
                self.channel_id) + '_' + str(key_word) + '/p' + str(i)
            # 第一页不是用页码标识，会出发验证码
            if i == 1:
                url = 'http://www.dianping.com/search/keyword/' + str(self.location_id) + '/' + str(
                    self.channel_id) + '_' + str(key_word)

                # 替换url，并且过滤掉p1（p1会触发验证码）
            if self.custom_search_url != '':
                url = self.custom_search_url + str(i)
                if i == 1:
                    url = self.custom_search_url[:-1]
            r = requests_util.get_requests(url, request_type='search')
            # r = requests.get(url, headers=header)
            text = r.text
            # 获取加密文件
            file_map = get_search_map_file(text)
            # 替换加密文件
            text = requests_util.replace_search_html(text, file_map)

            # 网页解析
            html = BeautifulSoup(text, 'lxml')
            shop_all_list = html.select('.shop-list')[0].select('li')

            search_res = []
            for shop in shop_all_list:
                try:
                    image_path = shop.select('.pic')[0].select('a')[0].select('img')[0]['src']
                except:
                    image_path = '-'
                try:
                    shop_id = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['data-shopid']
                except:
                    shop_id = '-'
                try:
                    detail_url = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['href']
                except:
                    detail_url = '-'
                try:
                    name = shop.select('.txt')[0].select('.tit')[0].select('a')[0].text.strip()
                except:
                    name = '-'
                # 两个star方式，有的页面显示详细star分数，有的显示icon
                # 解析icon
                try:
                    star_point = \
                        shop.select('.txt')[0].select('.comment')[0].select('.star_icon')[0].select('span')[0]['class'][
                            1].split('_')[1]
                    star_point = float(star_point) / 10
                    star_point = str(star_point)
                except:
                    star_point = '-'
                # 解析详细star
                try:
                    star_point = \
                        shop.select('.txt')[0].select('.comment')[0].select('.star_score')[0].text
                    star_point = float(star_point)
                    star_point = str(star_point)
                except:
                    pass
                try:
                    review_number = shop.select('.txt')[0].select('.comment')[0].select('.review-num')[0].text.replace(
                        '\n', '')
                except:
                    review_number = '-'
                try:
                    mean_price = shop.select('.txt')[0].select('.comment')[0].select('.mean-price')[0].select('b')[
                        0].text
                except:
                    mean_price = '￥0'
                try:
                    tags = shop.select('.txt')[0].select('.tag-addr')[0].select('.tag')
                    tag1 = tags[0].text.replace('\n', ' ').strip()
                    tag2 = tags[1].text.replace('\n', ' ').strip()
                except:
                    tag1 = '-'
                    tag2 = '-'
                try:
                    addr = shop.select('.txt')[0].select('.tag-addr')[0].select('.addr')[0].text.replace('\n',
                                                                                                         ' ').strip()
                except:
                    addr = '-'
                try:
                    recommend = shop.select('.recommend')[0].text.replace('\n', ' ').strip()
                except:
                    recommend = '-'
                try:
                    commend_list = shop.select('.comment-list')[0].text.replace('\n', ' ').strip()
                except:
                    commend_list = '-'
                one_step_search_res = [shop_id, name, star_point, review_number, mean_price, tag1, tag2, addr,
                                       recommend, commend_list, image_path, detail_url, '1', '1']  # 最后两位是搜索标记
                # 这个数据结构暂时没用
                search_res.append(one_step_search_res)
                # 只要首条，跳出
                if only_need_first is True:
                    break
                # 解析详情页
                if self.need_detail == '1':
                    try:
                        detail = Detail().get_detail(shop_id)
                        print('\n' + ','.join(detail) + '\n')
                        # self.saver.save_data([detail], 'detail')
                    except:
                        # 设置标记
                        one_step_search_res[-2] = '0'
                        logger.warning('详情信息获取失败，失败id：' + shop_id)
                        print('\n' + ','.join(one_step_search_res) + '\n')
                        if self.jump_wait is False:
                            print('检查浏览器，处理验证码，输入y程序继续运行,输入n跳过检查', 'http://www.dianping.com/shop/' + str(shop_id))
                            if input() == 'y':
                                continue
                            elif input() == 'n':
                                self.jump_wait = True
                else:
                    print('\n' + ','.join(one_step_search_res) + '\n')
                # 解析评论页
                if self.need_comment == '1':
                    try:
                        review = Review().get_review(shop_id)
                        print('获取', name, '评论', len(review), '条')
                        # self.saver.save_data(review, 'review')
                    except:
                        # 设置标记
                        one_step_search_res[-1] = '0'
                        logger.warning('评论获取失败，失败id：' + shop_id)

                # 保存数据
                saver.save_data([one_step_search_res], 'search')
        logger.info('解析完成:' + key_word)
