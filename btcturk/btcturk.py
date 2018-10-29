import time
import base64
import hmac
import hashlib
import requests


class Btcturk():
    BASE_URL = "https://www.btcturk.com/api/"

    def __init__(self, public_key=None, private_key=None):
        self.public_key = public_key
        self.private_key = private_key

    def _headers(self, protection):
        if protection:
            if self.public_key and self.private_key:
                stamp = str(int(time.time()))
                data = "{}{}".format(self.public_key, stamp).encode('utf-8')
                private_key = base64.b64decode(self.private_key)
                signature = hmac.new(private_key, data, hashlib.sha256).digest()

                return {
                    "X-PCK": self.public_key,
                    "X-Stamp": stamp,
                    "X-Signature": base64.b64encode(signature)
                }
            else:
                raise ValueError("You must set your public and private key for this method.")
        return {}

    def _make_request(self, method="GET", path="", params={}, data={}, protection=True):
        resp = None
        url = requests.compat.urljoin(self.BASE_URL, path)
        headers = self._headers(protection)
        headers["user-agent"] = "Mozilla/5.0"
        if method == "GET":
            resp = requests.get(url=url, headers=headers, params=params, data=data)
        elif method == "POST":
            resp = requests.post(url=url, headers=headers, params=params, data=data)
        return resp.json()

    def _make_order(self, pair_symbol, order_method, order_type, total, total_precision, amount, amount_precision, price,
                    price_precision, trigger_price, trigger_price_precision):
        data = {
            "PairSymbol": pair_symbol,
            "OrderMethod": order_method,
            "OrderType": order_type,
            "Total": total,
            "TotalPrecision": total_precision,
            "Amount": amount,
            "AmountPrecision": amount_precision,
            "Price": price,
            "PricePrecision": price_precision,
            "TriggerPrice": trigger_price,
            "TriggerPricePrecision": trigger_price_precision,
            "DenominatorPrecision": 2
        }
        return self._make_request(method="POST", path="exchange", data=data)

    def ticker(self):
        """
        Get the market info ticker
        :returns: API response
        """
        return self._make_request(method="GET", path="ticker", protection=False)

    def get_order_book(self, pair_symbol="BTCTRY"):
        """
        Get the order book
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :returns: API response
        """
        params = {"pairSymbol": pair_symbol}
        return self._make_request(method="GET", path="orderbook", params=params, protection=False)

    def get_all_trades(self, pair_symbol="BTCTRY"):
        """
        Get the all trades in the market.
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :returns: API response
        """
        params = {"pairSymbol": pair_symbol}
        return self._make_request(method="GET", path="trades", params=params, protection=False)

    def get_last_trades(self, pair_symbol="BTCTRY", count=10):
        """
        Get the last trades in the market
        :param str pair_symbol: Currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int count: The number of trades that will be requested.
        :returns: API response
        """
        params = {"last": count, "pairSymbol": pair_symbol}
        return self._make_request(method="GET", path="trades", params=params, protection=False)

    def get_all_ohlc(self, pair_symbol="BTCTRY"):
        """
        Get the all open, high, low, close, average etc. data in the market
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :returns: API response
        """
        params = {"pairSymbol": pair_symbol}
        return self._make_request(method="GET", path="ohlcdata", params=params, protection=False)

    def get_daily_ohlc(self, pair_symbol="BTCTRY", days=1):
        """
        Get the daily open, high, low, close, average etc. data in the market
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int days: The number of days to request
        :returns: API response
        """
        params = {"last": days, "pairSymbol": pair_symbol}
        return self._make_request(method="GET", path="ohlcdata", params=params, protection=False)

    def get_balances(self):
        """
        Get the authenticated account's balance
        :returns: API response
        """
        return self._make_request(method="GET", path="balance")

    def get_balances_v2(self):
        """
        Get the authenticated account's balance V2 (return with xrp balance)
        :returns: API response
        """
        return self._make_request(method="GET", path="balanceV2")

    def get_transactions(self, limit=25, offset=0, ascending=True):
        """
        Get the authenticated account's latest transactions. Includes all balance changes. Buys, sells, deposits, withdrawals and fees.
        :param int limit: Limit result to that many transactions. Default value is 25.
        :param int offset: Skip that many transactions before beginning to return results. Default value is 0.
        :param bool ascending: Results are sorted by date and time. Default value is ascending True.
        :returns: API response
        """
        if ascending:
            sort = "asc"
        else:
            sort = "desc"
        params = {
            "limit": limit,
            "offset": offset,
            "sort": sort
        }
        return self._make_request(method="GET", path="userTransactions", params=params)

    def get_open_orders(self, pair_symbol="BTCTRY"):
        """
        Get all open orders of the user
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :returns: API response
        """
        params = {"pairSymbol": pair_symbol}
        return self._make_request(method="GET", path="openOrders", params=params)

    def cancel_order(self, order_id):
        """
        Cancel order with given OrderId
        :param int order_id: order id for cancel order.
        :returns: API response
        """
        data = {"id": order_id}
        return self._make_request(method="POST", path="cancelOrder", data=data)

    def market_buy(self, pair_symbol, total, total_precision):
        """
        Buy crypto with market price
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int total: The total amount you will spend with this order. You will buy from different prices until your order is filled as described above
        :param str total_precision: Precision of the total (.001)
        :returns: API response
        """
        return self._make_order(pair_symbol=pair_symbol, order_method=1, order_type=0, total=total,
                                total_precision=total_precision, amount="0",
                                amount_precision="0", price="0", price_precision="0", trigger_price="0",
                                trigger_price_precision="0")

    def market_sell(self, pair_symbol, amount, amount_precision):
        """
        Sell crypto with market price
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int amount: Amount field will be ignored for buy market orders. The amount will be calculated according to the total value that you send.
        :param str amount_precision: Precision of the amount (.001)
        :returns: API response
        """
        return self._make_order(pair_symbol=pair_symbol, order_method=1, order_type=1, total="0", total_precision="00",
                                amount=amount, amount_precision=amount_precision, price="0", price_precision="00",
                                trigger_price="0", trigger_price_precision="00")

    def limit_buy(self, pair_symbol, total, total_precision, price, price_precision):
        """
        Send in a new limit buy order
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int total: The total amount you will spend with this order. You will buy from different prices until your order is filled as described above
        :param str total_precision: Precision of the total (.001)
        :param int price: Price field will be ignored for market orders. Market orders get filled with different prices until your order is completely filled.
        :param str price_precision: Precision of the price (.001)
        :returns: API response
        """
        return self._make_order(pair_symbol=pair_symbol, order_method=0, order_type=0, total="0",
                                total_precision="00", amount=total, amount_precision=total_precision, price=price,
                                price_precision=price_precision, trigger_price="0", trigger_price_precision="0")

    def limit_sell(self, pair_symbol, total, total_precision, price, price_precision):
        """
        Send in a new limit sell order
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int total: The total amount you will spend with this order. You will buy from different prices until your order is filled as described above
        :param str total_precision: Precision of the total (.001)
        :param int price: Price field will be ignored for market orders. Market orders get filled with different prices until your order is completely filled.
        :param str price_precision: Precision of the price (.001)
        :returns: API response
        """
        return self._make_order(pair_symbol=pair_symbol, order_method=0, order_type=1, total="0", total_precision="00",
                                amount=total, amount_precision=total_precision, price=price,
                                price_precision=price_precision, trigger_price="0", trigger_price_precision="00")

    def stop_buy(self, pair_symbol, total, total_precision, price, price_precision, trigger_price,
                 trigger_price_precision):
        """
        Send in a new limit buy order with stop trigger price
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int total: The total amount you will spend with this order. You will buy from different prices until your order is filled as described above
        :param str total_precision: Precision of the total (.001)
        :param int price: Price field will be ignored for market orders. Market orders get filled with different prices until your order is completely filled.
        :param str price_precision: Precision of the price (.001)
        :param int trigger_price: For stop orders
        :param str trigger_price_precision: Precision of the TriggerPrice (.001)
        :returns: API response
        """
        return self._make_order(pair_symbol=pair_symbol, order_method=2, order_type=0, total="0",
                                total_precision="00", amount=total, amount_precision=total_precision, price=price,
                                price_precision=price_precision, trigger_price=trigger_price,
                                trigger_price_precision=trigger_price_precision)

    def stop_sell(self, pair_symbol, total, total_precision, price, price_precision, trigger_price,
                  trigger_price_precision):
        """
        Send in a new limit sell order with stop trigger price
        :param str pair_symbol: currency symbol pair (BTCTRY, ETHTRY, XRPTRY)
        :param int total: The total amount you will spend with this order. You will buy from different prices until your order is filled as described above
        :param str total_precision: Precision of the total (.001)
        :param int price: Price field will be ignored for market orders. Market orders get filled with different prices until your order is completely filled.
        :param str price_precision: Precision of the price (.001)
        :param int trigger_price: For stop orders
        :param str trigger_price_precision: Precision of the TriggerPrice (.001)
        :returns: API response
        """
        return self._make_order(pair_symbol=pair_symbol, order_method=2, order_type=1, total="0", total_precision="00",
                                amount=total, amount_precision=total_precision, price=price,
                                price_precision=price_precision, trigger_price=trigger_price,
                                trigger_price_precision=trigger_price_precision)
