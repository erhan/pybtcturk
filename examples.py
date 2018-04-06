from btcturk import Btcturk

# Public Methods
client = Btcturk()
print(client.ticker())
print(client.get_order_book("BTCTRY"))
print(client.get_all_trades("BTCTRY"))
print(client.get_last_trades("BTCTRY", 5))
print(client.get_all_ohlc("XRPTRY"))
print(client.get_daily_ohlc("ETHTRY", 2))

# Private Methods
client = Btcturk("your_public_key", "your_private_key")
print(client.get_balances())
print(client.get_balances_v2())
print(client.get_transactions())
print(client.get_open_orders("ETHTRY"))
print(client.cancel_order(order_id=12345))
print(client.market_sell("ETHTRY", 0, "3"))
print(client.market_buy("ETHTRY", 20, "00"))
print(client.limit_sell("ETHTRY", 0, "001", 1600, "00"))
print(client.limit_buy("ETHTRY", 0, "001", 1500, "00"))
print(client.stop_sell("ETHTRY", 0, "001", 1500, "00", 1510, "00"))
print(client.stop_buy("ETHTRY", 0, "001", 1600, "00", 1590, "00"))
