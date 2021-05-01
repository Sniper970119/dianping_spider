# Sniper



[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
<img src="https://img.shields.io/badge/license-GPL--3.0-brightgreen">

*仅限学习交流使用，禁止商用*

##### 本项目遵守GPT-3.0开源协议

##### 您可以使用本项目for yourself，如果您使用本项目获利（包括但不限于商用、程序代做以及其他私活），则不被允许；除非给我分红 : >

##### 如果您未经允许使用本项目获利，本人保留因侵权连带的一切追责行为



### 求求大家给个star吧！！这个对我真的很重要！！

本程序可以爬取大众点评搜索页、详情页以及评论页中的相关信息，并将结果写入文件或数据库中。支持多cookie。

目前支持的写入类型如下：
- MongoDB数据库
- csv

如果您需要其他数据库支持，联系我们或者您添加后提PR。

**本项目可能对新手并不友好，因为配置项较多并且运行门槛相对不低，因此：**

**如果您是发现了bug或者有什么更好的提议，欢迎给我发邮件提issues、或PR，但是跟程序运行有关的所有问题请自行解决或查看[这里](https://github.com/Sniper970119/dianping_spider#%E8%BF%90%E8%A1%8C%E7%A8%8B%E5%BA%8F )。**

## 开发计划

### 已支持

- 搜索信息（搜索结果，粗）

- 详情信息（比前一个多 地址、电话、营业时间）

- 评论信息

- cookie池

- ip代理


### 计划支持

- 强势优化ip代理的作用（真的很强）

- 优惠券信息

## 环境配置
语言：python3

开发环境：python 3.6 （其他版本没有测试，不排除有问题）

系统：Windows/Linux/MacOS

其他环境配置：

需要：lxml、requests、tqdm、faker、beautifulsoup4、fontTools、pymongo（optional）

或者一键配置：

    pip install -r requirements.txt

## 使用方法：
### 配置配置文件
首先配置config.ini，参数意义在文件内已经有了详细说明，这里进行简单说明。

|参数|说明|
|:-----  |-----|
|config：      |  |
|use_cookie_pool      |是否使用cookie池 |
|Cookie      |Cookie信息（注意大写，之所以不一样是方便将浏览器信息直接复制进去而不做更改）。|
|user-agent      |浏览器UA信息，不填则随机UA。|
|save_mode      |保存方式，具体格式参照config.ini提示。|
|mongo_path      |mongo数据库配置，具体格式参照config.ini提示|
|requests_times      |爬虫间隔时间，具体格式参照config.ini提示。  |
|detail：      |  |
|keyword      | 搜索关键字 |
|location_id      |地区id，具体格式参照config.ini提示。  |
|channel_id      |频道id，具体格式参照config.ini提示。  |
|search_url      |搜索url，详见config.ini内提示。  |
|need_detail      |是否需要详情页  |
|need_comment      |是否需要评论页  |
|need_first      |是否只需要首页首条  |
|need_pages      |需要搜索的页数（搜索页）  |
|save:      |  |
|review_pages      |获取的评论页页数  |
|proxy:      |  |
|use_proxy |是否使用代理 |
|repeat_nub |ip重复次数，详见config.ini |
|http_extract |http提取 |
|key_extract |秘钥提取 |
|http_link |http提取接口 |
|key_id |秘钥id |
|key_key |秘钥key |


### 运行程序

正常搜索（完整流程，搜索->详情[可选]->评论[可选]）：
- 运行main.py

定制化搜索（不需要搜索，只需要详情或评论）:
- 只需要详情,shop_id 自行修改 （只给命令行格式，编译器运行则自行配置或修改代码）

    `python main.py --normal 0 --detail 1  --shop_id k30YbaScPKFS0hfP`

- 只需要评论 

    `python main.py --normal 0 --review 1  --shop_id k30YbaScPKFS0hfP`

- 需要详情和评论 

    `python main.py --normal 0  --detail 1 --review 1  --shop_id k30YbaScPKFS0hfP`
    
如果遇到其他问题，详见[这里](./docs/problems.md)
和[issues](https://github.com/Sniper970119/dianping_spider/issues?q=is%3Aissue+is%3Aclosed)

 
## 字段结果展示
由于大众点评反扒措施相对严重以及不同频道字段格式复杂，因此很多数据在爬取阶段不做处理。原样保存，后续自行清洗。
### 商家搜索结果展示：
![image](./imgs/info.jpg)

### 商家详情页展示：
![image](./imgs/detail.jpg)


### 商家评论页展示：
![image](./imgs/review.jpg)

## 一些碎碎念


关于cookie以及cookie池的一些碎碎念：[这里](./docs/cookie_pool.md)

关于存储的一些碎碎念：[这里](./docs/save.md)

关于ip代理的一些碎碎念：[这里](./docs/proxy.md)

一些可能遇到的小问题：[这里](./docs/problems.md)





  
## 相关功能笔记
  - [搜索页字体加密加密](http://www.sniper97.cn/index.php/note/carwler/3694/)
  - [评论页字体加密加密](http://www.sniper97.cn/index.php/note/carwler/3707/)

如果你想加快进度，点个star吧呜呜呜
