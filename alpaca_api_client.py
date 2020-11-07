import json
import requests



class AlpacaApiClient():
    
    API_KEY_ID = 'PKEWKSHZ3VKKO4AYOLRX'
    SECRET_KEY = 'fFCDJdmF3Nn8eiwRc53Qy5SmOqkC2KuvkXRu98SH'

    BASE_URL = 'https://paper-api.alpaca.markets'
    BASE_DATA_URL = 'https://data.alpaca.markets/v1'
    API_HEADERS = {
        'APCA-API-KEY-ID': API_KEY_ID,
        'APCA-API-SECRET-KEY': SECRET_KEY
    }

    def get_assets(self, symbol):
        r = requests.get(
            self.BASE_URL + '/v2/assets/{}'.format(symbol),
            headers=self.API_HEADERS
        )

        return r.content

    def get_data(self, symbols, start, end, interval='1D'):
        """
        Get timeseries data for one or more securities from Alpaca

        :param symbols str: Comma delimited string of each symbol we want data for
        :param start timestamp: Start date of data range in ISO format
        :param end timestamp: End Date of data range in ISO format
        :param interval string: Time interval we want our data from alpaca to be in
        """
        response = requests.get(
            self.BASE_DATA_URL + '/bars/{interval}?symbols={symbols}&start={start}&end={end}'.format(
                interval=interval,
                symbols=symbols,
                start=start,
                end=end
            ), 
            headers=self.API_HEADERS
        )

        return json.loads(response.content)

    def place_order(self, symbol, side):
        # In order to place a short order, we need to place a sell order
        # for a security we have no position in
        data = {
                'symbol': symbol,
                'side': side,
                'type': 'market',
                'qty': 1,
                'time_in_force': 'gtc'
            }

        print(data)

        response = requests.post(
            self.BASE_URL + '/v2/orders',
            data=json.dumps(data),
            headers=self.API_HEADERS
        )

        print(response)
        print(response.content)

        return response.content

    def get_orders(self):
        requests.get(
            self.BASE_URL + '/v2/orders',
            headers=self.API_HEADERS
        )

    def get_positions(self):
        response = requests.get(
            self.BASE_URL + '/v2/positions',
            headers=self.API_HEADERS
        )

        return json.loads(response.content)

    def close_position(self, symbol):
        response = requests.delete(
            self.BASE_URL + '/v2/positions/{}'.format(symbol),
            headers=self.API_HEADERS
        )