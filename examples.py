import binance
import asyncio


# Turn logging on, its off by default
binance.enable_logging(True)


api_key = ""
api_secret_key = ""

def market_data():
    # ping binance to see if it's online and verify we can hit it
    print("Connection ok? ", binance.ping())

    # Get the current server time in milliseconds
    print("Server time: ", binance.server_time())

    # Get the order book for a symbol with max 5 entries
    order_book = binance.order_book("BNBBTC", 5)
    print(order_book)


    print("Order book for BNB-BTC")
    print("asks")
    for (price, quantity) in order_book.asks:
        print(price, quantity)

    print("bids")
    for (price, quantity) in order_book.bids:
        print(price, quantity)


    # Get aggregated trades
    print(binance.aggregate_trades("BNBBTC", limit=5))

    candles = binance.candlesticks("BNBBTC", "1m")
    print(candles)

    # Ticker operations
    print("Current ticker prices")
    prices = binance.ticker_prices()
    print(prices)

    print("Current ticker for order books")
    order_books = binance.ticker_order_books()
    print(order_books["ETHBTC"])

    print("Order book ticker for ETHBTC")
    book = order_books["ETHBTC"]
    print(book)

    print("Order book ticker for BNBBTC")
    book = order_books["BNBBTC"]
    print(book)


    last_24hr = binance.ticker_24hr("BNBBTC")
    print(last_24hr)


def account():
    # For signed requests we create an Account instance and give it the api key and secret
    account = binance.Account("<api_key>", "<secret_key>")

    account.set_receive_window(6000)

    account.new_order("ETHBTC", "BUY", "LIMIT", .1, 0.01)

    order = account.query_order("ETHBTC", 100)
    print(order)

    account.open_orders("ETHBTC")

    account.all_orders("ETHBTC")

    info = account.account_info()
    print(info)

    trades = account.my_trades("ETHBTC")
    print(trades)


def user_stream():
    stream = binance.Streamer()

    def on_user_data(data):
        print("new user data: ", data)
        if data == "keepalive":
            stream.close_user()
            asyncio.get_event_loop().stop()

    stream.start_user(api_key, on_user_data)

    asyncio.get_event_loop().run_forever()

def data_streams():
    stream = binance.Streamer()

    def on_order_book(data):
        print("order book update - ", data)

    stream.add_order_book("ETHBTC", on_order_book)


    def on_candlestick(data):
        print("candlestick update - ", data)

    stream.add_candlesticks("ETHBTC", "1m", on_candlestick)


    def on_trades(data):
        print("trade update - ", data)

    stream.add_trades("ETHBTC", on_trades)


    asyncio.get_event_loop().run_forever()


#market_data()
#account()
#user_stream()
data_streams()