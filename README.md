# Sniper

*仅限学习交流使用，禁止商用*

[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
<a href="https://github.com/pnoker/iot-dc3/blob/master/LICENSE"><img src="https://img.shields.io/github/license/pnoker/iot-dc3.svg"></a>

### 求求大家给个star吧！！这个对我真的很重要！！

大众点评爬虫框架，开发中。

商家搜索结果展示：
![image](./imgs/base_info.jpg)

- 预期实现：
  - 商家搜索、各种信息获取
  - 评论爬取、详情信息爬取
  - 相关二进制文件下载
 
- 已实现：
  - 搜索页字体反爬处理，字体映射json生成
  - 评论页字体反爬处理，字体映射json生成
  - 存储器
  - 搜索页面以及存储
  - 字体文件映射缓存
  - 全局请求监控等待
  
- 已知问题：
  - 优惠券信息使用单独的json接口，由js回调，js加密，加密位置已经找到，暂时没时间解出来。(main-shop.min--->195 fun(h)
  - 详情页的部分参数由单独的加密接口获取（看来我逃不过了，唉），近期找时间解决吧
  
- 相关功能笔记
  - [搜索页字体加密加密](http://www.sniper97.cn/index.php/note/carwler/3694/)
  - [评论页字体加密加密](http://www.sniper97.cn/index.php/note/carwler/3707/)

如果你想加快进度，点个star吧呜呜呜
