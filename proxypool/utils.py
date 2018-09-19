
import asyncio
from aiohttp import ClientSession

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


async def fetch(sem, url, session, options={}):
    """下载器"""
    headers = dict(base_headers, **options)
    async with sem:  # 限制最大操作
        async with session.get(url, headers=headers, timeout=10) as response:  # 发送请求
            return await response.text()  # 获取响应文件, 注意不是马上获取, 异步操作要加await


async def get_page(urls, options={}):
        print('正在抓取', urls)
        try:
            task_list = []
            sem = asyncio.Semaphore(1024)  # 设置最大操作
            # 创建可复用的 Session减少开销
            async with ClientSession() as session:
                for each in urls:
                    tasks = asyncio.ensure_future(fetch(sem, each, session, options={}))  # 每个预请求
                    task_list.append(tasks)
                # 使用 gather(*tasks) 收集数据，wait(tasks) 不收集数据
                return await asyncio.gather(*task_list)
        except Exception:
            print('抓取失败', urls)
            return None


