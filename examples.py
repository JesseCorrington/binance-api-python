import binance
import asyncio


# Turn logging on, its off by default
binance.enable_logging(True)

# ping binance to see if it's online and verify we can hit it
print("Connection ok? ", binance.ping())

# Get the current server time in milliseconds
#print("Server time: ", binance.server_time())

# Get the order book for a symbol with max 5 entries
#order_book = binance.order_book("BNBBTC", 5)

# TODO: sorting seems wrong here
#print("Order book for BNB-BTC")
#print("asks")
#for (price, quantity) in order_book.asks:
#    print(price, quantity)

#print("bids")
#for (price, quantity) in order_book.bids:
#    print(price, quantity)


# Get aggregated trades
#print(binance.aggregate_trades("BNBBTC"))

#print(binance.candlesticks("BNBBTC", "1m"))

# Ticker operations
#print("Current ticker prices")
#prices = binance.ticker_prices()
#for key in prices:
#    print(key, " - ", prices[key])




#print("Current ticker for order books")
#order_books = binance.ticker_order_books()

#print("Order book ticker for ETHBTC")
#book = order_books["ETHBTC"]
#print(book)

#print("Order book ticker for BNBBTC")
#book = order_books["BNBBTC"]
#print(book)


#print(binance.ticker_24hr("BNBBTC"))


# For signed requests we create an Account instance and give it the api key and secret
#account = binance.Account("<api_key>", "<secret_key>")

#rint(account.new_order("ETHBTC", "BUY", "LIMIT", .1, .01))

#print(account.query_order("ETHBTC", 100))

#print(account.open_orders("ETHBTC"))

#print(account.all_orders("ETHBTC"))

#print(account.account_info())

#print(account.my_trades("ETHBTC"))




stream = binance.BinanceStream()

def on_depth(data):
    print("Depth update - ", data)

def on_kline(data):
    print("kline update - ", data)

def on_trades(data):
    print("trade update - ", data)



#stream.add_order_book("ETHBTC", on_depth)
stream.add_candlesticks("ETHBTC", "1m", on_kline)
#stream.add_trades("ETHBTC", on_trades)


asyncio.get_event_loop().run_forever()
