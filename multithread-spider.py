import time
import threading
from queue import Queue
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

def get_detail():
    while True:
        url = detail_url_list.get()

        try:
            data = requests.get(url).text
            dom_tree = etree.HTML(data)
            title = dom_tree.xpath('//div[@class="show-title"]/text()')
            print(title)

        except requests.exceptions.ConnectionError:
            print('连接被拒绝！')
            break


def get_url():
    while True:
        for page in range(2,10):
            try:
                data = requests.get('http://news.gzcc.cn/html/xiaoyuanxinwen/' + str(page) + '.html', headers=headers).text
                print('开始爬取第{}页的所有url'.format(str(page)))
                dom_tree = etree.HTML(data)
                results = dom_tree.xpath('//ul[@class="hot-list"]/li/a/@href')
                for index, url in enumerate(results):
                    print(url)
                    detail_url_list.put(url)
                print('第{}页url爬取完毕'.format(str(page)))
            except requests.exceptions.ConnectionError:
                print('连接被拒绝！')
                break

if __name__ == '__main__':
    detail_url_list = Queue()

    #爬取url线程
    thread_get_url = threading.Thread(target=get_url)
    thread_get_url.start()

    #爬取详情页线程
    for i in range(10):
        detail_thread = threading.Thread(target=get_detail)
        detail_thread.start()

