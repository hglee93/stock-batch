import ssl
import json
import datetime
import mysql.connector
from urllib.request import urlopen
from bs4 import BeautifulSoup
from stocklib import CompanyCodeCrawler
from stocklib import StockPriceCrawler

companyCrawler = CompanyCodeCrawler()
stockPriceCrawler = StockPriceCrawler()

company_list = companyCrawler.getCompanyCode()
stock_price_list = stockPriceCrawler.getStockPrice(company_list)

### DB 저장 코드
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)

mycursor = mydb.cursor()

currentTimeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

values = []

# BATCH 처리
for stock_price in stock_price_list : 
    value = (currentTimeString, stock_price["now"], stock_price["rate"], stock_price["now"], stock_price["high"], stock_price["low"], stock_price["amount"], stock_price["company"])
    values.append(value)

sql = """
    INSERT INTO FinanceDB.TB_F_DAY_STOCK(
        `F_STOCK_TRANS_DATE`, 
        `F_STOCK_DAY_CLOSING_PRICE`, 
        `F_STOCK_DAY_PREV_RATE`, 
        `F_STOCK_DAY_MARKET_PRICE`, 
        `F_STOCK_DAY_HIGH_PRICE`, 
        `F_STOCK_DAY_LOW_PRICE`, 
        `F_STOCK_DAY_VOLUME`, 
        `F_STOCK_LISTED_COMPANY_CD`
    ) 
    VALUES(%s, %s, %s, %s,%s, %s, %s, %s)
"""

mycursor.executemany(sql, values)
mydb.commit()

print("Completed!")




