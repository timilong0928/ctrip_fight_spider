# coding:utf-8

import urllib2
from lxml import etree
import json
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_json2(date, rk, CK, r):
    '''根据构造出的url获取到航班数据'''
    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SHA&ACity1=SIA&SearchType=S&DDate1=%s&IsNearAirportRecommond=0&rk=%s&CK=%s&r=%s"%(date,rk,CK,r)
    headers = {
        'Host': "flights.ctrip.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        'Referer': "http://flights.ctrip.com/booking/SHA-CKG-day-1.html?ddate1=2018-02-14"
    }
    headers['Referer'] = "http://flights.ctrip.com/booking/SHA-CKG-day-1.html?ddate1=%s" % date
    req = urllib2.Request(url,headers=headers)
    res = urllib2.urlopen(req)
    content = res.read()
    dict_content = json.loads(content,encoding="gb2312")
    length = len(dict_content['fis']) 
    i = 0
    for i in range(length):
        if ((dict_content['fis'][i][u'lp']) < 1600 ):
            print(dict_content['fis'][i][u'lp']),
            print(dict_content['fis'][i][u'dt']),
            print(dict_content['fis'][i][u'at']),
            print(dict_content['fis'][i][u'dpbn'])  


def get_parameter(date):
    '''获取重要的参数
    date:日期，格式示例：2016-05-13
    '''
    url='http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s'%date
    res=urllib2.urlopen(url).read()
    tree=etree.HTML(res)
    pp=tree.xpath('''//body/script[1]/text()''')[0].split()
    CK_original=pp[3][-34:-2]
    CK=CK_original[0:5]+CK_original[13]+CK_original[5:13]+CK_original[14:]

    rk=pp[-1][18:24]
    num=random.random()*10
    num_str="%.15f"%num
    rk=num_str+rk
    r=pp[-1][27:len(pp[-1])-3]

    return rk, CK, r

if __name__=='__main__':
    dates=['2018-02-13', '2018-02-14']

    for date in dates:
        rk, CK, r = get_parameter(date)
        get_json2(date, rk, CK, r)
        print "-----"
