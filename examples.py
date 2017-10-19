import binance


# Set api key and secret key (only needed for signed account requests)
binance.set_api_key(
    "<api_key>",
    "<secret_key>"
)

# Turn logging on, its off by default
binance.enable_logging(True)

# ping binance to see if it's online and verify we can hit it
#print("Connection ok? ", binance.ping())

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

print(binance.candlesticks("BNBBTC", "1m"))

# Ticker operations
#print("Current ticker prices")
#prices = binance.ticker_prices()
#for key in prices:
#    print(key, " - ", prices[key])


print("Current ticker for order books")
order_books = binance.ticker_order_books()

print("Order book ticker for ETHBTC")
book = order_books["ETHBTC"]
print(book)

print("Order book ticker for BNBBTC")
book = order_books["BNBBTC"]
print(book)


#print(binance.ticker_24hr("BNBBTC"))


#print(binance.new_order("ETHBTC", "BUY", "LIMIT", .1, .01))

#print(binance.query_order("ETHBTC", 100))


#print(binance.open_orders("ETHBTC"))
#print(binance.all_orders("ETHBTC"))

#print(binance.account_info())

#print(binance.my_trades("ETHBTC"))
