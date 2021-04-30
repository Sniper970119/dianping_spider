# Sniper

**ip代理的配置项专业性较强，如果您阅读config.ini和这里后不懂参数的意义，说明您欠缺这方面的相关知识，
建议百度 [python 代理ip的使用](https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd=python+%E4%BB%A3%E7%90%86ip%E7%9A%84%E4%BD%BF%E7%94%A8 )**

对于当前版本(2021-04-30)，ip代理的增益有限（有），但是对于下个版本（预计五月中旬左右）。
ip代理的增益将会巨大提升。因此，这个配置对于比较大规模的爬取有较大意义。

**诚招代理广告位哈哈哈哈哈**

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

