#!/usr/bin/env python
# encoding: utf-8
import sys, os, requests, socket

socket.setdefaulttimeout(10)    # 10s超时

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'

class Youku:
    # 优酷视频解析

    def __init__(self):
        # 初始化
        self.base = 'http://www.id97.com/videos/flashxml/token/authtoken/ykurl/'

    def parse(self, url):
        # 解析
        # url: 视频地址
        print self.getdata('http://www.id97.com/videos/flashxml/token/authtoken/ykurl/aHR0cDovL3YueW91a3UuY29tL3Zfc2hvdy9pZF9YT1RRek5EUTBOVGN5Lmh0bWw=')        
        pass
        
    def getdata(self, url):
        # GET请求
        
        qxd = 'auto'
        headers = {
               'User-Agent': USER_AGENT,
               'Content-Type': 'application/x-www-form-urlencoded'
              }
        # auto:最高 normal:标清 high:高清(mp4) super:超清 original:1080P
        cookies = { 'qxd': 'auto' }
        result = requests.get(url, headers=headers, cookies=cookies)
        return result.text

def main():
    # 主函数
    url = 'http://v.youku.com/v_show/id_XOTQzNDQ0NTcy.html'
    youku = Youku()
    data = youku.parse(url)


if __name__=='__main__':
    # 程序入口
    main()
    print 'Finish.'
    


