# Sniper

**ip代理的配置项专业性较强，如果您阅读config.ini和这里后不懂参数的意义，说明您欠缺这方面的相关知识，
建议百度 [python 代理ip的使用](https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd=python+%E4%BB%A3%E7%90%86ip%E7%9A%84%E4%BD%BF%E7%94%A8 )**

**诚招代理广告位哈哈哈哈哈**

## 我为什么要使用代理？

ip代理可以理解为伪装你的ip。

由于反爬虫最重要的手段之一就是通过ip判断行为，如果一个ip快速频繁访问，则判定这个ip为爬虫。

因此通过不断的变换你的ip来迷惑服务器。

## 代理的效果怎么样？

目前的版本，由于已经适配了加密接口（非登录数据），因此可以在代理的加持下可以大规模爬取数据。

但是对于登录数据，代理的加持并不那么明显（但是从我几次试验的效果来看，依然有一定效果）。

## ip代理说明

ip代理，目前只适配了json格式，还没有适配秘钥格式的代理。

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
    
但是本质上没区别，如果需要自行更改。

