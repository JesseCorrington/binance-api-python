# Python Binance API
A python wrapper for the [Binance API](https://www.binance.com/restapipub.html).
It supports all public endpoints, signed endpoints, and websocket data streams.
All numeric types returned from the API are converted to Decimal, to prevent
floating point innacuracies, since we're dealing with financial data.

### Installation
Simply copy binance.py into your project and import it.
You will also need to install the websockets library. Python 3.6 or newer is required.
```
pip install websockets  
```

## Public Endpoints
These don't require setting up your API key and are all static methods

### Turn logging on or off
```python
import binance
binance.enable_logging(True)
binance.enable_logging(False)
```

### Ping Binance.com to see if it's online
```python
binance.ping()
```
#### Output
```python
True
```


### Get the server time
```python
binance.server()
```
#### Output
```python
2017-10-20 12:14:10.171000
```


### Get the order book for a specific symbol
```python
order_book = binance.order_book("BNBBTC", 5)
print(order_book)
```
#### Output
```python
OrderBook(bids=[(Decimal('0.00020759'), Decimal('97.00000000')), (Decimal('0.00020750'), Decimal('550.00000000')), (Decimal('0.00020702'), Decimal('50.00000000')), (Decimal('0.00020677'), Decimal('64.00000000')), (Decimal('0.00020669'), Decimal('5.00000000'))], asks=[(Decimal('0.00020799'), Decimal('1200.00000000')), (Decimal('0.00020800'), Decimal('10055.00000000')), (Decimal('0.00021083'), Decimal('5141.00000000')), (Decimal('0.00021084'), Decimal('7.00000000')), (Decimal('0.00021297'), Decimal('836.00000000'))])
```


### Get aggregated trades
```python
trades = binance.aggregate_trades("BNBBTC", limit=5)
print(trades)
```
#### Output
```python
[{'a': 1367857, 'p': Decimal('0.00020752'), 'q': Decimal('76.00000000'), 'f': 1501629, 'l': 1501629, 'T': 1508527146843, 'm': True, 'M': True}, {'a': 1367858, 'p': Decimal('0.00020795'), 'q': Decimal('16.00000000'), 'f': 1501630, 'l': 1501630, 'T': 1508527182319, 'm': False, 'M': True}, {'a': 1367859, ...
```


### Get candlesicks
```python
candles = binance.candlesticks("BNBBTC", "1m")
print(candles)
```
#### Output
```python
[CandleStick(open_time=1508497320000, open=Decimal('0.00022551'), high=Decimal('0.00022551'), low=Decimal('0.00022551'), close=Decimal('0.00022551'), volume=Decimal('14.00000000'), close_time=1508497379999, quote_asset_volume=Decimal('0.00315714'), trade_count=1, taker_buy_base_quote_vol=Decimal('0E-8'), taker_buy_quote_asset_vol=Decimal('0E-8')), CandleStick(open_time=1508497380000,...
```


### Get current prices for all markets
```python
prices = binance.ticker_prices()
print(prices)
```
#### Output
```python
{'ETHBTC': Decimal('0.05129400'), 'LTCBTC': Decimal('0.01019000'), 'BNBBTC': Decimal('0.00020800'), 'NEOBTC': Decimal('0.00474300'),...
```


### Get the top order book entry for all markets
```python
print("Current ticker for order books")
order_books = binance.ticker_order_books()
print(order_books["ETHBTC"])
```

#### Output
```python
{OrderBookTicker(bid_price=Decimal('0.05104700'), bid_qty=Decimal('10.00000000'), ask_price=Decimal('0.05135500'), ask_qty=Decimal('15.00000000'))}
```


### Gets the 24 hour price change statistics for a specific symbol
```python
last_24hr = binance.ticker_24hr("BNBBTC")
print(last_24hr)
```
#### Output
```python
{'priceChange': Decimal('-0.00001848'), 'priceChangePercent': Decimal('-8.177'), 'weightedAvgPrice': Decimal('0.00022479'), 'prevClosePrice': Decimal('0.00022600'), 'lastPrice': Decimal('0.00020752'), 'lastQty': Decimal('81.00000000'), 'bidPrice': Decimal('0.00020751'), 'bidQty': Decimal('267.00000000'), 'askPrice': Decimal('0.00020798'), 'askQty': Decimal('315.00000000'), 'openPrice': Decimal('0.00022600'), 'highPrice': Decimal('0.00023987'), 'lowPrice': Decimal('0.00020750'), 'volume': Decimal('1098837.00000000'), 'quoteVolume': Decimal('247.01269419'), 'openTime': 1508441273823, 'closeTime': 1508527673823, 'firstId': 1494258, 'lastId': 1501663, 'count': 7406}
```


## Signed Endpoints
These require using an API key and API secret for authentication.
If you don't have a key, log into binance.com and create one [here](https://www.binance.com/userCenter/createApi.html]).
Be sure to never commit your keys to source control.

### Create a new account object
The account object is how you access all the signed enpoints
```python
account = binance.Account("<api_key>", "<secret_key>")
```


### Set the receive window for all signed requests
This is the number of milliseconds a request must be processed within before being rejected by the server. If not set, the default is 5000 ms
```python
account.set_receive_window(3000)
```


### Place a new limit order
```python
# a buy limit order
account.new_order("ETHBTC", "BUY", "LIMIT", 0.0513605, 4)

# or a sell limit order
account.new_order("ETHBTC", "SELL", "LIMIT", 0.0513605, 4)
```


### Place a new market order
```python
# a buy market order
account.new_order("ETHBTC", "BUY", "MARKET", 4)

# or a sell market order
account.new_order("ETHBTC", "SELL", "MARKET", 4)
```


### Query an order
```python
account.query_order("ETHBTC", <order-id>)
```


### Cancel an order
```python
account.cancel_order("ETHBTC", <order-id>)
```


### Get all open orders for a given symbol
```python
account.open_orders("ETHBTC")
```


### Get all account orders; active, canceled, or filled
```python
account.all_orders("ETHBTC")
```


### Get your account info, including balances for all symbols
```python
info = account.account_info()
```


### Get trades for a specific account and symbol
```python
trades = account.my_trades("ETHBTC")
```


## Websocket Data Streams
In addition to the requests above for getting market data, you can also stream
the order books, candlesticks, and aggregated trades.


### Create a new stream
You just need to create a single stream object, and then you can add ass many data sources to it as you need.
```python
stream = binance.BinanceStream()
```


### Add an order book data stream
```python
def on_order_book(data):
    print("order book update - ", data)

stream.add_order_book("ETHBTC", on_order_book)
```


### Add a candlestick data stream
```python
def on_candlestick(data):
    print("candlestick update - ", data)

stream.add_candlesticks("ETHBTC", "1m", on_candlestick)
```


### Add a trades data stream
```python
def on_trades(data):
    print("trade update - ", data)

stream.add_trades("ETHBTC", on_trades)
```


### Remove an order book data stream
```python
stream.remove_order_book("ETHBTC")
```


### Remove a candlestick data stream
```python
stream.remove_candlesticks("ETHBTC", "1m")
```


### Remove a trades data stream
```python
stream.remove_trades("ETHBTC")
```


### Close all data streams
```python
stream.close_all()
```


### Run until all data streams are closed
```python
asyncio.get_event_loop().run_forever()
```