import asyncio
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *

class Getter:

    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """判断是否达到了代理池限制"""
        if self.redis.count >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():

            loop = asyncio.get_event_loop()

            tasks = []
            for callback_label in range(self.crawler.__CrawlFuncCount__): # 迭代clwaer类里的爬虫
                callback = self.crawler.__CrawlFunc__[callback_label] # 第label个爬虫
                task = asyncio.ensure_future(eval("self.crawler.{}()".format(callback))) # 创建协程任务
                tasks.append(task)

            loop.run_until_complete(asyncio.gather(*tasks))


