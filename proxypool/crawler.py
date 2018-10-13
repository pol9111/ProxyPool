from proxypool.db import RedisClient
from .utils import get_page
from pyquery import PyQuery as pq
import re
import sys

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = [] # 爬虫列表
        for k, v in attrs.items(): # 类所有的属性和方法
            if 'crawl_' in k: # {'crawl_': return}下面类的爬取函数, 函数名和函数返回值
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count # 多少个爬虫
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass): # 继承ProxyMetaclass, 拥有__CrawlFunc__, __CrawlFuncCount__两个属性
    def __init__(self):
        self.redis = RedisClient()

    def save_to_db(self, proxies):
        for proxy in proxies:
            sys.stdout.flush()
            print('成功获取到代理', proxy)
            self.redis.add(proxy)

    async def crawl_daili66(self):
        """获取代理66, 外国ip多"""
        urls = ['http://www.66ip.cn/{}.html'.format(page) for page in range(1, 5)]
        print('Crawling')
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                doc = pq(page)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    ip_port = ':'.join([ip, port])
                    proxy = {'https':'http://'+ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_ip3366(self):
        """云代理index"""
        urls = ['http://www.ip3366.net/?stype=1&page={}'.format(page) for page in range(1, 5)]
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(page)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        ip_port = address_port.replace(' ','')
                        proxy = {'https':'http://'+ip_port}
                        proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_ip3366_(self):
        """云代理free"""
        urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(page) for page in range(1, 5)]
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                re_ip_address = ip_address.findall(page)
                # ip_port = [(re_ip_address[i] + ':' + re_port[i]).replace(' ', '') for i in range(len(re_port))]
                # proxies.append(ip_port)
                for address, port in re_ip_address:
                    result = address+':'+ port
                    ip_port = result.replace(' ', '')
                    proxy = {'https': 'http://' + ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_kuaidaili(self):
        """快代理(都是http的)"""
        urls = ['http://www.kuaidaili.com/free/inha/{}/'.format(page) for page in range(1, 5)]
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(page)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(page)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    ip_port = address_port.replace(' ','')
                    proxy = {'https': 'http://' + ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_xicidaili(self):
        """西刺代理"""
        urls = ['http://www.xicidaili.com/nn/{}'.format(page) for page in range(1, 4)]
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
            'Host':'www.xicidaili.com',
            'Referer':'http://www.xicidaili.com/nn/3',
            'Upgrade-Insecure-Requests':'1',
        }
        html = await get_page(urls, options=headers)
        if html:
            proxies = []
            for page in html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(page)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        ip_port = address_port.replace(' ', '')
                        proxy = {'https':'http://'+ip_port}
                        proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_iphai(self):
        """ip海"""
        urls = ['http://www.iphai.com/']
        html = await get_page(urls)
        if html:
            proxies = []
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html[0])
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    ip_port = address_port.replace(' ', '')
                    proxy = {'https': 'http://' + ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_data5u(self):
        """data5u"""
        urls = ['http://www.data5u.com/free/gngn/index.shtml']
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = await get_page(urls, options=headers)
        if html:
            proxies = []
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html[0])
            for address, port in re_ip_address:
                result = address + ':' + port
                ip_port = result.replace(' ', '')
                proxy = {'https': 'http://' + ip_port}
                proxies.append(proxy)
            self.save_to_db(proxies)

# 近期修改的

    async def crawl_goubanjia(self):
        """全网ip"""
        urls = ['http://www.goubanjia.com']
        html = await get_page(urls)
        if html:
            proxies = []
            doc = pq(html[0])
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                ip_port = td.text().replace('\n', '')
                proxy = {'https': 'http://' + ip_port}
                proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_89ip(self):
        """89ip"""
        urls = ['http://www.89ip.cn/index_{}.html'.format(page) for page in range(1, 4)]
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                doc = pq(page)
                ips = doc('tr td:nth-child(1)').items()
                ports = doc('tr td:nth-child(2)').items()
                for ip, port in zip(ips, ports):
                    result = ip.text() + ':' + port.text()
                    ip_port = result.replace(' ', '')
                    proxy = {'https': 'http://' + ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_ip181(self):
        """讯代理api接口"""
        urls = ['http://www.ip181.com/']
        html = await get_page(urls)
        if html:
            proxies = []
            json_ = eval(html[0])
            RESULT = json_.get('RESULT')
            for i in RESULT:
                ip = i.get('ip')
                port = i.get('port')
                result = ip + ':' + port
                ip_port = result.replace(' ', '')
                proxy = {'https': 'http://' + ip_port}
                proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_premproxy(self):
        """premproxy"""
        urls = ['https://premproxy.com/proxy-by-country/{}.htm'.format(country) for country in ('China-01','China-02','China-03','China-04','Taiwan-01')]
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
                re_ip_address = ip_address.findall(page)
                for address_port in re_ip_address:
                    ip_port = address_port.replace(' ', '')
                    proxy = {'https': 'http://' + ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

    async def crawl_xroxy(self):
        """xroxy 换了网址不挂代理, 访问很慢"""
        urls = ['https://www.xroxy.com/proxy-country-{}'.format(country) for country in ('cn','tw')]
        html = await get_page(urls)
        if html:
            proxies = []
            for page in html:
                ip_address1 = re.compile('<td class="sorting_1">(\d+\.\d+\.\d+\.\d+)</td>')
                re_ip_address1 = ip_address1.findall(page)
                print(re_ip_address1)
                ip_address2 = re.compile("<td>\d[3-5]</td>")
                re_ip_address2 = ip_address2.findall(page)
                print(re_ip_address2)
                for address,port in zip(re_ip_address1,re_ip_address2):
                    address_port = address+':'+port
                    ip_port = address_port.replace(' ','')
                    proxy = {'https': 'http://' + ip_port}
                    proxies.append(proxy)
            self.save_to_db(proxies)

# 网页没了, 其他原因用不了的

   # # ip可用度低算了
   #  def crawl_ip181(self):
   #      """讯代理api接口"""
   #      start_url = 'http://www.ip181.com/'
   #      chrome_options = webdriver.ChromeOptions()
   #      chrome_options.add_argument('--headless')
   #      browser = webdriver.Chrome(chrome_options=chrome_options)
   #      wait = WebDriverWait(browser, 15)
   #
   #      browser.get(start_url)
   #      wait.until(EC.presence_of_element_located((By.XPATH, '//body')))
   #      html = browser.page_source
   #
   #      body = re.findall('<body>(.*?)</body>', html)
   #      ips_ = json.loads(body[0])
   #      ips = ips_.get('RESULT')
   #      for i in ips:
   #          ip = i.get('ip')
   #          port = i.get('port')
   #          ip_port = ip + ':' + port
   #          yield ip_port

    # def crawl_proxy360(self):
    #     """
    #     获取Proxy360
    #     :return: 代理
    #     """
    #     start_url = 'http://www.proxy360.cn/Region/China'
    #     print('Crawling', start_url)
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         lines = doc('div[name="list_proxy_ip"]').items()
    #         for line in lines:
    #             ip = line.find('.tbBottomLine:nth-child(1)').text()
    #             port = line.find('.tbBottomLine:nth-child(2)').text()
    #             yield ':'.join([ip, port])

    # def crawl_daxiang(self):
    #     """大象代理"""
    #     url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
    #     html = get_page(url)
    #     if html:
    #         urls = html.split('\n')
    #         for url in urls:
    #             yield url


    # def crawl_kxdaili(self):
    #     for i in range(1, 11):
    #         start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
    #         html = get_page(start_url)
    #         ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #         # \s* 匹配空格，起到换行作用
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')
