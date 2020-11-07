from datetime import datetime
from datetime import timedelta
import json

import schedule
import time

import matplotlib.pyplot as plt
import pandas as pd

from alpaca_api_client import AlpacaApiClient


class Analyzer():

    def bollinger_bands_for_range(self, symbol, start, end):
        json_response = api_client.get_data(symbol, start, end, '1D')
        symbol_time_series_data = json_response[symbol]
        
        df = pd.DataFrame(symbol_time_series_data)

        df['20MA'] = df['c'].rolling(20).mean()
        df['20STD'] = df['c'].rolling(20).std()
        df['Upper Bollinger'] = df['20MA'] + (2 * df['20STD'])
        df['Lower Bollinger'] = df['20MA'] - (2 * df['20STD'])
        return df


api_client = AlpacaApiClient()

def get_bollinger_and_compare():
    print("Inside the job")
    stock_universe = ['TLRY', 'SQ', 'MRO', 'AAPL', 'GM', 'SNAP', 'SHOP', 'SPLK', 'BA', 'AMZN', 'SUI', 'SUN', 'TSLA', 'CGC', 'SPWR', 'NIO', 'CAT', 'MSFT', 'PANW', 'OKTA', 'TWTR', 'TM', 'RTN', 'ATVI', 'GS', 'BAC', 'MS', 'TWLO', 'QCOM', 'C', 'DOMO']
    
    for symbol in stock_universe:
        end_time = datetime.now()
        start_time = end_time - timedelta(weeks=1)
        # bollinger_df = Analyzer().bollinger_bands_for_range(symbol, '2020-01-01T00:00:00Z', '2020-10-15T00:00:00Z')
        bollinger_df = Analyzer().bollinger_bands_for_range(
            symbol, start_time.isoformat(), end_time.isoformat)

        last_row = bollinger_df.iloc[-1]
        close_price = last_row['c']
        MA20 = last_row['20MA']
        upper_bollinger = last_row['Upper Bollinger']
        lower_bollinger = last_row['Lower Bollinger']

        print("Symbol: {}".format(symbol))
        print("Close Price: {}".format(close_price))
        print("Lower Bollinger: {}".format(lower_bollinger))
        print("Upper Bollinger: {}".format(upper_bollinger))

        position_found = False
        positions = AlpacaApiClient().get_positions()

        for position in positions:
            if position['symbol'] == symbol:
                position_found = True

        # Entry
        if close_price > upper_bollinger:
            # Short the stock
            asset_info = AlpacaApiClient().get_assets(symbol)
            
            if json.loads(asset_info)['shortable']:
                response = AlpacaApiClient().place_order(
                    symbol,
                    'sell'
                )

                print("Short order placed")
                print(response)
                print("-------------")
        elif close_price < lower_bollinger:
            # Long the stock
            
            response = AlpacaApiClient().place_order(
                symbol, 
                'buy'
            )

            print("Long order placed")
            print(response)
            print("-----------")

        # Exit
        print("Lower Exit bound: {}".format((MA20 - (MA20 * 0.02))))
        print("Upper Exit bound: {}".format((MA20 + (MA20 * 0.02))))
        if close_price > (MA20 - (MA20 * 0.02)) and close_price < (MA20 + (MA20 * 0.02)) and position_found:
            AlpacaApiClient().close_position(symbol)

        print("\n")


# get_bollinger_and_compare()

schedule.every(15).minutes.do(get_bollinger_and_compare)

while True:
    schedule.run_pending()
    time.sleep(1)



