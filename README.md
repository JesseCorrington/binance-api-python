# Python Binance API
A python wrapper for the [Binance API](https://www.binance.com/restapipub.html).
It supports all public endpoints, signed endpoints, and websocket data streams.
All numeric types returned from the API are converted to Decimal, to prevent
floating point innacuracies, since we're dealing with financial data.

#### Installation
Simply copy binance.py into your project and import it.
You will also need to install the websockets library
```
pip install websockets  
```

### Public endpoints started
This don't require settign up your API key and are all static methods

## enable_logging
Turn logging on or off. It's off by default.
```python
import binance
binance.enable_logging(True)
binance.enable_logging(False)
```

## ping
Ping Binance.com to see if it's online and we can hit it.
```python
binance.ping()
```

<details>
<summary>View Response</summary>
```python
True
```
</summary>

## server_time
Get the server time from binance
```python
binance.server()
```

## order_book
Get the order book for a specific symbol
```python
binance.order_book()
```