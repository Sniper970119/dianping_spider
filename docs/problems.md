# Sniper

###  可能遇到的问题
1.显示（可能在以后的某次更新不再会出现）：

        2021-02-09 16:18:47,166 - 23532-MainThread - function\detail.py[line:42] - WARNING: 详情页请求被ban
        2021-02-09 16:18:47,166 - 23532-MainThread - function\search.py[line:161] - WARNING: 详情信息获取失败，失败id：xxx
        
原因：由于大众点评过于苛刻的，出现这个意味着您触发了大众点评的反爬措施，暂时不能访问详情页（但是并不意味着您不能访问搜索页以及评论页）

解决方法： 调整config.ini requests_times参数然后，just wait（等解封）。或者暂时只爬取详情页。（后期可能会添加补救方法）