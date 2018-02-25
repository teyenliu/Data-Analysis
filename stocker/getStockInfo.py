#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time

def getStockInfo(quote):
    req = requests.session()
    req.get('http://mis.twse.com.tw/stock/index.jsp',headers = {'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'})
    #response = req.get('http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={}&json=1&delay=0&_{}'.format(quote,int(time.time()*1000)))
    response = req.get('http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={}'.format(quote))
    return response.text

# Example:
lst = ('tse_t00.tw','tse_TW50.tw','tse_TWMC.tw','tse_TWIT.tw','tse_TWEI.tw',
       'tse_TWDP.tw','tse_EMP99.tw','tse_HC100.tw','tse_CG100.tw','tse_FRMSA.tw',
       'tse_t001.tw','tse_t002.tw','tse_t003.tw','tse_t011.tw','tse_t031.tw','tse_t051.tw',
       'tse_t01.tw','tse_t02.tw','tse_t03.tw','tse_t04.tw','tse_t05.tw',
       'tse_t06.tw','tse_t07.tw','tse_t21.tw','tse_t22.tw','tse_t08.tw',
       'tse_t09.tw','tse_t10.tw','tse_t11.tw','tse_t12.tw','tse_t13.tw',
       'tse_t24.tw','tse_t25.tw','tse_t26.tw','tse_t27.tw','tse_t28.tw',
       'tse_t29.tw','tse_t30.tw','tse_t31.tw','tse_t14.tw','tse_t15.tw',
       'tse_t16.tw','tse_t17.tw','tse_t18.tw','tse_t23.tw','tse_t20.tw',
       'tse_EDRL2.tw','tse_EDRIN.tw')
#print getStockInfo('|'.join([id + '_{}'.format(time.strftime("%Y%m%d", time.gmtime())) for id in lst]))
print getStockInfo('|'.join(lst))

#print getStockInfo('tse_t00.tw_{}'.format(time.strftime("%Y%m%d", time.gmtime())))
print getStockInfo('tse_t00.tw')
print getStockInfo('tse_t00.tw|otc_o00.tw|tse_FRMSA.tw')
print getStockInfo('tse_1101.tw')
print getStockInfo('tse_1101.tw|tse_1102.tw|otc_1256.tw')
print getStockInfo('tse_2317.tw|tse_2412.tw|tse_3008.tw|otc_1258.tw')