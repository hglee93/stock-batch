import mysql.connector
from datetime import datetime

class StockDao:
    def __init__(self, _host, _user, _password):
        self.stockdb = mysql.connector.connect(
            host = _host,
            user = _user,
            password = _password
        )
    
    def insertStockPriceListBatch(self, stock_price_list):
        currentTimeString = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        # Execute INSERT BATCH statement
        cursor = self.stockdb.cursor()
        cursor.executemany(sql, values)
        self.stockdb.commit()