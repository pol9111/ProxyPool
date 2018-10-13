import asyncio
import aiohttp
import time
import sys
from aiohttp import ClientError
from proxypool.db import RedisClient
from proxypool.setting import *


class Tester(object):

    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, session, proxy):
        """测试单个代理"""
        try:
            real_proxy = eval(proxy)['https']
            print('正在测试', proxy)
            async with session.get(TEST_URL, proxy=real_proxy, timeout=20, allow_redirects=False) as response:
                if response.status in VALID_STATUS_CODES:
                    rst = await response.text()
                    if rst:
                        resp_ip = '//'+eval(rst).get('headers').get('X-Forwarded-For')
                        proxy_ip = real_proxy.split(':')
                        if resp_ip == proxy_ip[1]:
                            self.redis.max(proxy)
                            print('代理可用', proxy)
                else:
                    self.redis.decrease(proxy)
                    print('请求响应码不合法 ', response.status, 'IP', proxy)
        except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
            self.redis.decrease(proxy)
            print('代理请求失败', proxy)

    async def set_test_tasks(self, loop):
        """设置测试任务"""
        count = self.redis.count
        print('当前剩余', count, '个代理')
        for start in range(0, count, BATCH_TEST_SIZE): # 一段一段创建任务, 每一段一个Session减少内存开销
            stop = min(start + BATCH_TEST_SIZE, count)
            print('正在测试第', start + 1, '-', stop, '个代理')
            test_proxies = self.redis.batch(start, stop)
            # conn = aiohttp.TCPConnector(verify_ssl=False)
            conn = aiohttp.TCPConnector()
            async with aiohttp.ClientSession(connector=conn, loop=loop) as session:
                tasks = [self.test_single_proxy(session, proxy) for proxy in test_proxies]
                await asyncio.wait(tasks)

    def run(self):
        """测试主函数"""
        print('测试器开始运行')
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.set_test_tasks(loop))
            sys.stdout.flush()  # 马上print不用等到循环结束
            time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)