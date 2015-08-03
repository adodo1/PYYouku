#!/usr/bin/env python
# encoding: utf-8
import sys, os, re, time, requests, random, json, urllib

USER_AGENT = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36";
REFERER = "http://www.youku.com";
FORM_ENCODE = "GBK";
TO_ENCODE = "UTF-8";

class Youku():
    # 视频解析类
    def __init__(self):
        # 初始化
        self.base = 'http://v.youku.com/player/getPlaylist/VideoIDS/'
        self.source = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890'
        self.sz = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
                   -1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,1,2,3,4,5,
                   6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,35,
                   36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1]
        self.str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        
    def parse(self, url):
        # 解析
        matches = re.search('id\_([\w=]+)', url, re.I)
        if (matches==None):
            # 匹配失败
            print 'Match fail !'
            html = self.cget(url)
            matches = re.search('videoId2\s*=\s*\'(\w+)\'', html, re.I)
            if (matches==None): return False

        
        # 根据you vid 获取相应的视频地址
        return self.getYouku(matches.group(1).strip())

    def cget(self, url, convert=False, timeout=10):
        # 获取html
        headers = {
               'User-Agent': USER_AGENT,
               'Content-Type': 'application/x-www-form-urlencoded'
               #'Origin': REFERER,
               #'Referer': REFERER,
               #'Accept-Language': 'zh-CN,zh;q=0.8'
              }
        result = requests.get(url, headers=headers)
        return result.text

    def getSid(self):
        # start 获得优酷视频需要用到的方法
        sid = '{0}{1}'.format(int(time.time()), 10000 + random.randint(0,9000))
        return sid

    def getKey(self, key1, key2):
        # 计算KEY
        # 注意 key1 必须是16进制的
        #      key2 是一个字符串
        a = int(key1)
        b = a ^ 0xA55AA5A5                  # 异或运算
        b = hex(b)[2:].replace('L', '')     # 转16进制去掉结尾的L
        return '{0}{1}'.format(key2, b)

    def getFileid(self, fileId, seed):
        # 通过种子解码字符串
        # 参数1: 16*42*20*16*62*16*16*20*16*16*5*35*57*24*16*35*32*19*47*24*19*48*20*33*44*42*42*33*37*19*37*33*18*57*19*57*48*5*6*33*19*57*48*6*57*32*62*20*6*32*47*57*62*6*42*19*33*32*57*47*48*16*24*44*33*57*
        # 参数2: 5832
        # 结果1: pcskj5-Od_rRh:/a0xF61qLiCfmYT.GQE9J4WDSyzX3lA\I8BgHnZPoub7MUvV2etNwK
        # 结果2: 0310200100547C04E68C6B19A339D6D9F767B5-967B-7E21-E872-369E78B0CA97
        mixed = self.getMixString(seed)
        ids = fileId.strip().split('*')
        realId = ''
        for idx in ids:
            if (idx == ''): continue
            index = int(idx)
            realId += mixed[index:index+1]
        return realId

    def getMixString(self, seed):
        # CG混淆
        mixed = ''
        source = self.source
        size = len(source)
        for i in range(0, size):
            seed = (seed * 211 + 30031) % 65536
            index = int(seed / 65536.0 * len(source))
            c = source[index:index+1]
            mixed += c
            source = source.replace(c, '')
        return mixed

    def yk_d(self, a):
        # 什么鬼算法完全看不懂
        if (a == ''): return ''
        f = len(a)
        b = 0
        strs = self.str
        c = ''
        while(b < f):
            e = self.charCodeAt(a, b) & 255
            b += 1
            if (b == f):
                c += self.charAt(strs, e >> 2)
                c += self.charAt(strs, (e & 3) << 4)
                c += '=='
                break
            g = self.charCodeAt(a, b)
            b += 1
            if (b == f):
                c += self.charAt(strs, e >> 2)
                c += self.charAt(strs, (e & 3) << 4 | (g & 240) >> 4)
                c += self.charAt(strs, (g & 15) << 2)
                c += '='
                break
            h = self.charCodeAt(a, b)
            b += 1
            c += self.charAt(strs, e >> 2)
            c += self.charAt(strs, (e & 3) << 4 | (g & 240) >> 4)
            c += self.charAt(strs, (g & 15) << 2 | (h & 192) >> 6)
            c += self.charAt(strs, h & 63)
        return c

    def yk_na(self, a):
        # 比上面的算法更看不懂
        if (a == ''): return ''
        h = self.sz
        i = len(a)
        f = 0
        e = ''
        while(f < i):
            while True:
                c = h[self.charCodeAt(a, f) & 255]
                f += 1
                if (f < i and -1==c): continue
                else: break
            if (-1 == c): break
            while True:
                b = h[self.charCodeAt(a, f) & 255]
                f += 1
                if (f < i and -1 == b): continue
                else: break
            if (-1 == b): break
            e += self.fromCharCode(c << 2 | (b & 48) >> 4)
            while True:
                c = self.charCodeAt(a, f) & 255
                f += 1
                if (61 == c): return e
                c = h[c]
                if (f < i and -1==c): continue
                else: break
            if (-1 == c): break
            e += self.fromCharCode((b & 15) << 4 | (c & 60) >> 2)
            while True:
                b = self.charCodeAt(a, f) & 255
                f += 1
                if (61 == b): return e
                b = h[b]
                if (f < i and -1==b): continue
                else: break
            if (-1 == b): break
            e += self.fromCharCode((c & 3) << 6 | b)
        return e

    def yk_e(self, a, c):
        # 还是看不懂的算法
        f = 0
        i = ''
        e = ''
        h = 0
        b = {}
        for h in range(0, 256):
            b[h] = h
        for h in range(0, 256):
            f = ((f + b[h]) + self.charCodeAt(a, h % len(a))) % 256
            i = b[h]
            b[h] = b[f]
            b[f] = i
        q = f = h = 0
        for q in range(0, len(c)):
            h = (h + 1) % 256
            f = (f + b[h]) % 256
            i = b[h]
            b[h] = b[f]
            b[f] = i
            e += self.fromCharCode(self.charCodeAt(c, q) ^ b[(b[h] + b[f]) % 256])
        return e

    def fromCharCode(self, codes):
        # 不知道
        return chr(codes)

    def charCodeAt(self, strs, index):
        # F**k!
        c = strs[index:index+1]
        return ord(c)

    def charAt(self, strs, index=0):
        # 字符串中第N个字符
        return strs[index:index+1]
    

    def getYouku(self, vid):
        # $link = "http://v.youku.com/player/getPlayList/VideoIDS/{$vid}/Pf/4"; //获取视频信息json 有些视频获取不全(土豆网的 火影忍者)
        blink = self.base + vid
        link = blink + "/Pf/4/ctype/12/ev/1"
        retval = self.cget(link)
        bretval = self.cget(blink)

        if (retval != ''):
            rs = json.loads(retval)
            brs = json.loads(bretval)
            error = rs['data'][0].get('error', None)
            if (error!=None):
                print error
                return False
            data = {}
            streamtypes = rs['data'][0]['streamtypes']      # 可以输出的视频清晰度
            streamfileids = rs['data'][0]['streamfileids']  # 
            seed = rs['data'][0]['seed']
            segs = rs['data'][0]['segs']
            ip = rs['data'][0]['ip']
            bsegs = brs['data'][0]['segs']

            #print '<<<<'
            #abc = self.yk_na('NgXTTQUbL7ze1fjC/eJxVdHw6Bo01wjLWBk=')
            #print abc
            #print self.yk_e('becaf9be', abc)
            #print '<<<<'
            
            sid, token = self.yk_e('becaf9be', self.yk_na(rs['data'][0]['ep'])).split('_')
            for (key, val) in segs.items():

                if (key in streamtypes):
                    for k in range(len(val)):
                        v = val[k]
                        no = hex(int(v['no']))[2:].replace('L', '').upper()
                        if (len(no)==1): no='0'+no
                        # 构建视频地址K值
                        _k = v['k']
                        if ((_k==None or _k=='') or _k=='-1'):
                            _k = bsegs[key][k]['k']
                        fileId = self.getFileid(streamfileids[key], seed)
                        fileId = fileId[0:8]+no+fileId[10:]
                        ep = self.yk_d(self.yk_e('bf7e5f01', (((sid+'_')+fileId)+'_')+token))
                        ep = urllib.quote(ep.decode('gbk').encode('utf-8'))
                        # 判断后缀类型 、获得后缀
                        typeArray = {
                            'flv': 'flv',
                            'mp4': 'mp4',
                            'hd2': 'flv',
                            '3gp': 'flv',
                            'hd3': 'flv',
                            '3gphd': 'mp4'
                        }
                        # 判断视频清晰度
                        sharpness = {
                            'flv': 'normal',
                            'flvhd': 'normal',
                            'mp4': 'high',
                            'hd2': 'super',
                            '3gphd': 'high',
                            '3gp': 'normal',
                            'hd3': 'original'
                        }
                        fileType = typeArray[key]
                        
                        if ((sharpness[key] in data) == False): data[sharpness[key]] = {}
                        data[sharpness[key]][k] = 'http://k.youku.com/player/getFlvPath/sid/' + \
                                                  str(sid) + '_00/st/' + str(fileType) + '/fileid/' + str(fileId) + \
                                                  '?K=' + str(_k) + '&hd=1&myp=0&ts=' + str(v['seconds']) + \
                                                  '&ypp=0&ctype=12&ev=1&token=' + str(token) + '&oip=' + \
                                                  str(ip) + '&ep=' + str(ep)
            
            # 返回 图片 标题 链接 时长 视频地址
            data['img'] = rs['data'][0]['logo']
            data['title'] = rs['data'][0]['title']
            data['seconds'] = rs['data'][0]['seconds']
            return data
        else:
            return false


if __name__=='__main__':
    # Get Youku
    id = 'XODM3NDQ5MDYw'    # 视频ID
    d = '1'                 # 清晰度

    de = ''
    if (d == '2'): de = 'high'      # 高清MP4
    elif (d == '3'): de = 'super'   # 超清
    else: de = 'normal'             # 标清

    url = 'http://v.youku.com/v_show/id_{0}.html'.format(id)
    youku = Youku()
    data = youku.parse(url)
    print ''

    num = 0
    for (key, val) in data[de].items():
        num += 1
        print '{0} TITLE:{1} NUM:{2}'.format(val, data['title'], num)
        print ''

    
    
    #print youku.getKey(0x10, 'abc')
    #print youku.getFileid('38*51*38*38*38*43*43*33*38*38*63*39*8*34*43*35*51*63*57*34*27*35*43*48*28*51*51*48*20*27*20*48*44*8*27*8*35*63*45*48*27*8*35*45*8*33*13*43*45*33*57*8*13*45*51*27*48*33*8*57*35*38*34*28*48*8*', 6142)
    pass

