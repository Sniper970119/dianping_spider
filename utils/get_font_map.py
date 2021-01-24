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

import re
import json
import requests
from faker import Factory
from fontTools.ttLib import TTFont

import logging

from utils.logger import logger as global_logger
from utils.get_file_map import get_map


def get_map_file(page_source):
    """
    获取映射文件
    :param page_source: 页面源码
    :return:
    """
    # 如果无法在页面信息中解析出字体css文件，说明被反爬或者cookie失效
    try:
        font_base_url = re.findall(' href="(//s3plus.meituan.net/v1/.*?)">', page_source)[0]
    except:
        global_logger.warning('cookie失效或者被限制访问，更新cookie或登录大众点评滑动验证')
        return
    font_base_url = 'https:' + font_base_url
    header = get_header()
    r = requests.get(font_base_url, headers=header)
    text = r.text
    woff_urls = re.findall(',url\("(.*?\.woff"\).*?\{)', text)
    # 设置logger等级，解析woff会生成无关日志，屏蔽
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    # 处理css中的woff链接
    for each in woff_urls:
        # 解析address woff
        if 'address' in each:
            address_map_woff_url = re.findall('(//.*?woff)', each)[0]
            address_map_woff_url = 'https:' + address_map_woff_url
            download_woff(address_map_woff_url, 'address.woff')
            parse_woff('address.woff')
            parse_xml('address.xml')
        if 'shopNum' in each:
            shop_num_map_woff_url = re.findall('(//.*?woff)', each)[0]
            shop_num_map_woff_url = 'https:' + shop_num_map_woff_url
            download_woff(shop_num_map_woff_url, 'shopNum.woff')
            parse_woff('shopNum.woff')
            parse_xml('shopNum.xml')
        if 'tagName' in each:
            tag_name_map_woff_url = re.findall('(//.*?woff)', each)[0]
            tag_name_map_woff_url = 'https:' + tag_name_map_woff_url
            download_woff(tag_name_map_woff_url, 'tagName.woff')
            parse_woff('tagName.woff')
            parse_xml('tagName.xml')
        if 'reviewTag' in each:
            review_tag_map_woff_url = re.findall('(//.*?woff)', each)[0]
            review_tag_map_woff_url = 'https:' + review_tag_map_woff_url
            download_woff(review_tag_map_woff_url, 'reviewTag.woff')
            parse_woff('reviewTag.woff')
            parse_xml('reviewTag.xml')
    # 将logger等级恢复
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def download_woff(woff_url, filename):
    """
    下载字体文件
    :param woff_url:
    :param filename:
    :return:
    """
    r = requests.get(woff_url)
    with open('./tmp/' + filename, 'wb') as f:
        f.write(r.content)


def parse_xml(filename):
    """
    解析xml
    :param filename:
    :return:
    """
    saved_name = filename.replace('.xml', '.json')
    # 获取已经处理好的文字映射
    data = get_map('./files/template_map.json')

    # 读取xml文件
    with open('tmp/' + filename, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    # 找出xml中核心部分
    res = re.findall('<GlyphOrder>(.*?)</GlyphOrder>', xml_content, re.S)[0]
    # 解析文字映射
    change_res = re.findall('<GlyphID id=".*?" name="(.*?)"/>', res)

    final_res = {}
    # 映射匹配
    for i in range(2, 603):
        tmpstr = 'glyph' + str(i)
        final_res[change_res[i]] = data[tmpstr]
    # 保存字典
    with open('tmp/' + saved_name, 'w', encoding='utf-8') as f:
        json.dump(final_res, f, ensure_ascii=False)


def parse_woff(filename):
    """
    解析woff文件，生成xml文件
    :param filename:
    :return:
    """
    saved_name = filename.replace('.woff', '.xml')
    font_data = TTFont('./tmp/' + filename)
    font_data.saveXML('./tmp/' + saved_name)
    return saved_name


def get_header():
    """
    生成请求头
    :return:
    """
    ua_engine = Factory.create()
    ua = ua_engine.user_agent()
    header = {
        'User-Agent': ua,
    }
    return header
