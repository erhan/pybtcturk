# pybtcturk
  
Python client for the [Btcturk Api](https://github.com/BTCTrader/broker-api-docs).  

  [![Build version](https://img.shields.io/badge/pypi-0.0.4-brightgreen.svg)](https://pypi.python.org/pypi/btcturk)
  [![License](https://img.shields.io/badge/license-mit-lightgrey.svg)](https://pypi.python.org/pypi/btcturk)
  [![Python version](https://img.shields.io/badge/python-2.7%2C3.5%2C3.6-blue.svg)](https://pypi.python.org/pypi/btcturk)
  
  
## Installation  
  
```  
pip install btcturk
```  

```  
pip install git+git://github.com/erhan/pybtcturk.git
```  
  
## Usage  

### Btcturk Pair symbols

 - BTCTRY
 - ETHTRY
 - XRPTRY


### Public Endpoint Methods  

```python 
from btcturk import Btcturk  

client = Btcturk()  
```

#### Ticker
  
```python  
client.ticker()  
```  
  
#### Get order book
  
```python  
client.get_order_book(pair_symbol)
```  
 
#### Get all trades
  
```python  
client.get_all_trades(pair_symbol)
```  

#### Get last trades
  
```python  
client.get_last_trades(pair_symbol, count)
```  

#### Get all ohlc data
  
```python  
client.get_all_ohlc(pair_symbol)
```  

#### Get daily ohlc data
  
```python  
client.get_daily_ohlc(pair_symbol, days)
```  

  
### Private Endpoint Methods  
  
```python 
from btcturk import Btcturk  

client = Btcturk("public_key", "private_key")
```
  
#### Get balances
  
```python  
client.get_balances()
# example return : 
client.get_balances_v2()
# example return : 
```  

#### Get transactions
  
```python  
client.get_transactions(limit, offset, ascending)
```

#### Get open orders
  
```python  
client.get_open_orders(pair_symbol)
```

#### Cancel order
  
```python  
client.cancel_order(order_id)
```

#### Market buy
  
```python  
client.market_buy(pair_symbol, total, total_precision)
```

#### Market sell
  
```python  
client.market_sell(pair_symbol, amount, amount_precision)
```

#### Limit buy
  
```python  
client.limit_buy(pair_symbol, amount, amount_precision, price, price_precision)
```

#### Limit sell
  
```python  
client.limit_sell(pair_symbol, amount, amount_precision, price, price_precision)
```

#### Stop buy
  
```python  
client.stop_buy(pair_symbol, total, total_precision, trigger_price, trigger_price_precision)
```

#### Stop sell
  
```python  
client.stop_sell(pair_symbol, total, total_precision, trigger_price, trigger_price_precision)
```

