import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    t = 0
    try:
        while t < 80:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                ip =response.text
                t += 1
                yield ip

    except ConnectionError:
        return None


def write_ip(ip):
    t = 0
    proxy_list = []  # 已有(已写入)的列表
    for each_ip in ip:
        if not each_ip in proxy_list:
            with open('C:\\Users\Alex\Desktop\Memorandum\Scrapy\IP.txt', 'a+') as f:
                content = '{\"http\":' + ' ' + '\"https://' + '' + each_ip + '\"' + '},' + '\n'
                # content = '{\"ip_prot\":' + '\"' + each_ip + '\"' + '},' + '\n'
                f.write(content)
                t += 1
                print('写入成功-' + str(t))
                proxy_list.append(each_ip)
        else:
            pass


if __name__ == '__main__':
    text = get_proxy()
    write_ip(text)


