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


class CSV():
    def __init__(self):
        self.create_dir('./output')

    def save_data(self, data, data_type):
        """
        保存数据
        :param data:
        :param data_type:
        :return:
        """
        assert data_type in ['search', 'detail', 'comment']
        if data_type == 'search':
            self.save_search_list(data)
        elif data_type == 'detail':
            self.save_detail_list(data)
        elif data_type == 'comment':
            self.save_comment_list(data)
        else:
            raise Exception

    def save_search_list(self, data):
        """
        保存搜索结果
        :param data:
        :return:
        """
        if os.path.exists('./output/search_res.csv'):
            with open('./output/search_res.csv', 'a+', encoding='utf-8') as f:
                for each in data:
                    f.write(','.join(each) + '\n')
        else:
            with open('./output/search_res.csv', 'a+', encoding='utf-8') as f:
                title = ['店铺id', '店铺名称', '店铺评分', '评论数量', '平均价格', '标签1', '标签2', '地址', '推荐', '评分', '图片链接', '详情链接']
                f.write(','.join(title) + '\n')
            self.save_search_list(data)

    def save_detail_list(self, data):
        """
        保存详细结果
        :param data:
        :return:
        """
        if os.path.exists('./output/detail_res.csv'):
            with open('./output/detail_res.csv', 'a+', encoding='utf-8') as f:
                for each in data:
                    f.write(','.join(each) + '\n')
        else:
            with open('./output/detail_res.csv', 'a+', encoding='utf-8') as f:
                title = ['店铺id', '店铺名称', '评论数量', '平均价格', '评分', '地址', '电话', '其他信息']
                f.write(','.join(title) + '\n')
            self.save_detail_list(data)

    def save_comment_list(self, data):
        """
        保存评论数据
        :param data:
        :return:
        """
        pass

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
