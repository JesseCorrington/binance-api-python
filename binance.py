import urllib.request
import urllib.parse
import json
import ssl
import datetime
import hmac
import hashlib
import time
from decimal import Decimal
from collections import namedtuple


# TODO: figure out how to make SSL work and get ride of this
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

__URL_BASE = "https://www.binance.com/api/"
__api_key = None
__api_secret_key = None
__log_enabled = False


def __timestamp():
    return int(round(time.time() * 1000))


def __v1_url(endpoint):
    return __URL_BASE + "v1/" + endpoint


def __v3_url(endpoint):
    return __URL_BASE + "v3/" + endpoint


def __log(msg):
    global __log_enabled
    if __log_enabled:
        print(msg)


__URLS = {
    # General
    "ping": __v1_url("ping"),
    "time": __v1_url("time"),

    # Market Data
    "depth": __v1_url("depth"),
    "agg_trades": __v1_url("aggTrades"),
    "candlesticks": __v1_url("klines"),
    "ticker_prices":  __v1_url("ticker/allPrices"),
    "ticker_books": __v1_url("ticker/allBookTickers"),
    "ticker_24hr": __v1_url("/ticker/24hr"),

    # Account
    "order": __v3_url("order"),
    "open_orders": __v3_url("openOrders"),
    "all_orders": __v3_url("allOrders"),
    "account": __v3_url("account"),
    "my_trades": __v3_url("myTrades")
}


OrderBook = namedtuple("OrderBook", "bids asks")

CandleStick = namedtuple("CandleStick", "open_time open high low close volume close_time quote_asset_volume trade_count taker_buy_base_quote_vol taker_buy_quote_asset_vol")

OrderBookTicker = namedtuple("OrderBookTicker", "bid_price, bid_qty, ask_price, ask_qty")


# Public API

def set_api_key(key, secret):
    global __api_key
    global __api_secret_key

    __api_key = key
    __api_secret_key = secret


def enable_logging(enabled):
    global __log_enabled
    __log_enabled = enabled


def geturl_json(url, query_params={}, sign=False, method="GET"):
    if query_params is not None:
        for key in list(query_params.keys()):
            if query_params[key] is None:
                del query_params[key]

        if sign:
            query_params["timestamp"] = __timestamp()

            query = urllib.parse.urlencode(query_params)
            query_params["signature"] = hmac.new(__api_secret_key.encode("utf8"), query.encode("utf8"), digestmod=hashlib.sha256).hexdigest()

        url += "?" + urllib.parse.urlencode(query_params)

    __log("GET: " + url)

    req = urllib.request.Request(url, method=method)

    if sign:

        req.add_header("X-MBX-APIKEY", __api_key)

    json_ret = {}

    try:
        resp = urllib.request.urlopen(req, context=ctx)
        json_ret = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        # TODO: need to throw too, and need to get the json returned for better error msg
        __log(e.read())
        __log(e, " - ", url)

    return json_ret


def ping():
    return geturl_json(__URLS["ping"]) == {}


def server_time():
    data = geturl_json(__URLS["time"])
    return datetime.datetime.fromtimestamp(data["serverTime"] / 1000.0)


# symbol: required
# limit: Default 100; max 100.
def order_book(symbol, limit=None):
    data = geturl_json(__URLS["depth"], {"symbol": symbol, "limit": limit})

    bids = []
    asks = []
    for bid in data["bids"]:
        price_qty = (Decimal(bid[0]), Decimal(bid[1]))
        bids.append(price_qty)

    for ask in data["asks"]:
        price_qty = (Decimal(ask[0]), Decimal(ask[1]))
        asks.append(price_qty)

    book = OrderBook(bids, asks)

    return book


def aggregate_trades(symbol, from_id=None, start_time=None, end_time=None, limit=None):
    params = {
        "symbol": symbol,
        "fromId": from_id,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit}

    trades = geturl_json(__URLS["agg_trades"], params)

    # convert price and quantity to decimals
    for trade in trades:
        trade["p"] = Decimal(trade["p"])
        trade["q"] = Decimal(trade["q"])

    return trades


def candlesticks(symbol, interval, limit=None, start_time=None, end_time=None):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": start_time,
        "endTime": end_time
    }

    candles = geturl_json(__URLS["candlesticks"], params)
    for i in range(len(candles)):
        candles[i] = candles[i][:-1]
        for j in range(len(candles[i])):
            if isinstance(candles[i][j], str):
                candles[i][j] = Decimal(candles[i][j])

        candles[i] = CandleStick(*candles[i])

    return candles


def ticker_prices():
    coins = geturl_json(__URLS["ticker_prices"])

    prices = {}
    for coin in coins:
        prices[coin["symbol"]] = Decimal(coin["price"])

    return prices


def ticker_order_books():
    coins = geturl_json(__URLS["ticker_books"])

    book_tickers = {}
    for coin in coins:
        book_tickers[coin["symbol"]] = {
            OrderBookTicker(
                Decimal(coin["bidPrice"]),
                Decimal(coin["bidQty"]),
                Decimal(coin["askPrice"]),
                Decimal(coin["askQty"])
            )
        }

    return book_tickers


def ticker_24hr(symbol):
    ticker = geturl_json(__URLS["ticker_24hr"], {"symbol": symbol})

    for key in ticker:
        if isinstance(ticker[key], str):
            ticker[key] = Decimal(ticker[key])

    return ticker

# TODO: we can maybe just make recv window a global param


def new_order(symbol, side, type, quantity, price, new_client_order_id=None, stop_price=None, iceberg_qty=None, recv_window=None):
    params = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "timeInForce": "GTC",       # TODO: does this need config?
        "quantity": quantity,
        "price": price,
        "newClientOrderId": new_client_order_id,
        "stopPrice": stop_price,
        "icebergQty": iceberg_qty,
        "recvWindow": recv_window
    }

    return geturl_json(__URLS["order"], params, True, "POST")


def query_order(symbol, order_id=None, orig_client_order_id=None, recv_window=None):
    if order_id is None and orig_client_order_id is None:
        raise Exception("param Error: must specify orderId or origClientOrderId")

    params = {
        "symbol": symbol,
        "orderId": order_id,
        "origClientOrderId": orig_client_order_id,
        "recvWindow": recv_window
    }

    return geturl_json(__URLS["order"], params, True)


def cancel_order(symbol, order_id=None, orig_client_order_id=None, new_client_order_id=None, recv_window=None):
    if order_id is None and orig_client_order_id is None:
        raise Exception("param Error: must specify orderId or origClientOrderId")

    params = {
        "symbol": symbol,
        "orderId": order_id,
        "origClientOrderId": orig_client_order_id,
        "newClientOrderId": new_client_order_id,
        "recvWindow": recv_window
    }

    return geturl_json(__URLS["order"], params, True, method="DELETE")


def open_orders(symbol):
    return geturl_json(__URLS["open_orders"], {"symbol": symbol}, True)


def all_orders(symbol, order_id=None, limit=None):
    params = {
        "symbol": symbol,
        "orderId": order_id,
        "limit": limit
    }

    return geturl_json(__URLS["all_orders"], params, True)


def account_info():
    return geturl_json(__URLS["account"], sign=True)


def my_trades(symbol, limit=None, from_id=None):
    params = {
        "symbol": symbol,
        "limit": limit,
        "fromId": from_id
    }

    return geturl_json(__URLS["my_trades"], params, True)
