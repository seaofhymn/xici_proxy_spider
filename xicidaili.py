import requests
from lxml import etree
import time
import random
import threading
import pymysql

def getip():
    try:
        conn = pymysql.connect(host='', user='', passwd='', port=3306, db='')
        sql = """select ip,stat from dyn where randid=9;"""
        cur=conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
        if ret:
            sta = ret[0][1]
            if sta:
                ip = ret[0][0] + ':808'
                print(ip)
                conn.close()
                return ip
        else:
            print("请等待")
            return 0
    except Exception as e:
        print(e)
        return 0

class parse_xici():
    def __init__(self):
        self.url = "http://www.xicidaili.com/nn/{}"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
        self.ua = [
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
                    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
                    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
                    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
                    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
                    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
                   ]

    def get_page_list(self,n):
        total = []
        for i in range(1,n):
            total.append(self.url.format(i))
        return total

    def send_requests(self,page_list):
        con_list = []
        # while True:
        p = getip()
        if p:
            proxy = {
                'https': 'https://{}'.format(p),
                'http': 'http://{}'.format(p)
            }
        else:
            proxy =None
        for each in page_list:
            con_list.append(requests.get(each, headers={'User-Agent':random.choice(self.ua)},proxies = proxy,timeout=10).content.decode())
        return con_list

    def deal_page_content(self,con_list):
        ip_list = []
        for each in con_list:
            html = etree.HTML(each)
            tr_list = html.xpath("//table[@id = 'ip_list']//td[contains(.,'HTTPS')]/..")
            for tr in tr_list:
                    ip_list.append("https://"+''.join(tr.xpath("./td[2]/text()"))+":"+"".join(tr.xpath("./td[3]/text()")))
        return ip_list

    def make_sure(self,ips):
        print(len(ips))
        for ip in ips:
            proxy = {'https':ip,'http':ip}
            print("正在验证%s有效性"%ip)
            try:
                ret = requests.get('https://www.baidu.com',headers = self.headers,proxies = proxy,timeout=5).content.decode()
                print(ret)
                if len(ret)>1000:
                    print("有效ip")
                else:
                    print("无效ip")
                    ips.remove(ip)
            except Exception as e:
                print("此ip无效")
                ips.remove(ip)
        print(len(ips))
        return ips

    def run(self,n):
        pages = self.get_page_list(n)
        content_li = self.send_requests(pages)
        ip_list = self.deal_page_content(content_li)
        return ip_list

def main():
    daili = parse_xici()
    while True:
        try:
            ips = daili.run(3)
            print(ips)
        # valid_ips = daili.make_sure(ips)
        # print("全部有效ip为%s"%valid_ips)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    main()


