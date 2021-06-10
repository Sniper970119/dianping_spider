# Sniper

**ip代理的配置项专业性较强，如果您阅读config.ini和这里后不懂参数的意义，说明您欠缺这方面的相关知识，
建议百度 [python 代理ip的使用](https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd=python+%E4%BB%A3%E7%90%86ip%E7%9A%84%E4%BD%BF%E7%94%A8 )**

代理是需要买的，代理是需要买的，代理是需要买的。

**诚招代理广告位哈哈哈哈哈**

## 我为什么要使用代理？

ip代理可以理解为伪装你的ip。

由于反爬虫最重要的手段之一就是通过ip判断行为，如果一个ip快速频繁访问，则判定这个ip为爬虫。

因此通过不断的变换你的ip来迷惑服务器。

## 代理的效果怎么样？

目前的版本，由于已经适配了加密接口（非登录数据），因此可以在代理的加持下可以大规模爬取数据。

但是对于登录数据，代理的加持并不那么明显（但是从我几次试验的效果来看，依然有一定效果）。

## ip代理说明

ip代理，目前只适配了json格式。

json格式由于各家代理json格式也不一样，目前只适配了一种格式：
    
    [
        {
            "ip":"xxx.xxx.xxx.xxx",
            "port":"xxxxx"
        },
        {
            "ip":"xxx.xxx.xxx.xxx",
            "port":"xxxxx"
        },
    ]
    
已知还有另一种json格式，并没有适配

    "state":"ok",
    "data":[
            {
                "ip":"xxx.xxx.xxx.xxx",
                "port":"xxxxx"
            },
            {
                "ip":"xxx.xxx.xxx.xxx",
                "port":"xxxxx"
            },
        ]
    
但是本质上没区别，如果需要自行更改。（utils -> requests_utils.py -> 265行）

## 秘钥模式

只适配了（***），***打码了，一个是不想打广告，再一个是这家有点拽，现在已经不给个人用户用，只对企业用户开放。
（而且总的来说代理质量一般，好处是允许以小时为单位购买（1元/小时））。

适配格式如下：

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": host,
                "port": port,
                "user": user（id）,
                "pass": pass(key),
            }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

其实不仅是这家，大部分的隧道模式应该都是这个格式，如果不是自己简单改一下就行。（utils -> requests_utils.py -> 313行）

## 其他

对于need_detail=False情况下依然要配置cookie，原因是搜索页需要cookie才能访问
（虽然第一页不用，但是第一页对于匿名访问有格外限制，与其浪费代理撞出来，不如用cookie，最多点一下验证码而已）。
