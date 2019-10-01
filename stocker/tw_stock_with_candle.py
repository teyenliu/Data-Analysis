# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:21:37 2018

@author: liudanny
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import string


def getMonthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)


"""
Transfer TW's year to AD year
"""
def replaceTW_to_AD(tw_date):
    idx = tw_date.find("/")
    year = str(int(tw_date[0:idx])+1911)

    return string.replace(tw_date, tw_date[0:idx], year)


"""
Argument: URL string
Return The dataframe of stock data
"""
def connectTW_Stock_Source(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        print('Error Retrieving Data.')
        print(e)

    return retriveTW_Stock_Data(soup, 9)


"""
Argument: BeautifulSoup obj, Dataframe of stock data, 
          column size of stock table
Return The dataframe of stock data
"""
def retriveTW_Stock_Data(soup, column_size=9):
    table = soup.find_all('tbody')[0] # Grab the first table
    row_marker = 0
    stock_table = None
    try:
        for row in table.find_all('tr'):
            column_marker = 0
            new_row_table = pd.DataFrame(columns=range(0,column_size), index = [0])
            columns = row.find_all('td')
        
            for column in columns:
                new_row_table.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
        
            if stock_table is not None:
                stock_table = stock_table.append(new_row_table)
            else:
                stock_table = new_row_table
    except Exception as e:
        print('Error Retrieving Data.')
        print(e)
    return stock_table


#we default analyze 5 years long data
url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={0}&stockNo={1}"
date_range = []
column_size=9
for m in range(-12 * 5, 0):
    date_range.append(getMonthdelta(datetime.now(), m).strftime('%Y%m%d'))

stock_data = pd.DataFrame(columns=range(0, column_size))
for date in date_range:
    my_url = url.format(date, "2330")
    print(my_url)
    tmp_stock_data = connectTW_Stock_Source(my_url)
    print(tmp_stock_data)
    stock_data = stock_data.append(tmp_stock_data)
    print("wait for 3 seconds to retrieve next data...")
    time.sleep(3)

stock_data.columns = ['Date', 'Volume', 'Turnover', 'Open', 'High', 'Low', 'Close', 'Diff', 'Count']
# Set the index to a column called Date
#stock_data = stock_data.set_index('Date')
stock_data = stock_data.reset_index(level=0)
stock_data['Volume'] = stock_data['Volume'].str.replace(',', '')
stock_data = stock_data.apply(pd.to_numeric, errors='ignore')
stock_data['Date'] = stock_data['Date'].map(lambda a: replaceTW_to_AD(a))
stock_data['Date']=pd.to_datetime(stock_data['Date'], format='%Y-%m-%d')
stock_data.index=stock_data['Date']
stock_data2 = stock_data.iloc[:,[4,5,6,7,2]] # Open High Low Close Volume

#momentum function
def momentum(price,periond):
    lagPrice=price.shift(periond)
    momen=price-lagPrice
    momen= momen.dropna()
    return(momen)

Close=stock_data.Close

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, \
                                DayLocator, MONDAY, date2num
from mpl_finance import candlestick_ohlc

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

momen35=momentum(Close,7)
import candle
candle.candleLinePlots(stock_data2,\
               candleTitle=u'TW Stock:2330 K Line',\
               splitFigures=True,Data=momen35,\
               title=u'7 day momentum',ylabel=u'7 day momentum')

plt.show()
