import time
import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from app.entities import OrderParams
from app.moon_api import MoonApi
from app.utils import (
    get_pair, 
    get_order_payload, 
    get_order_id,
    random_range, 
    random_int, 
    simple_mid_price
)

# Environment constants and global variables
bot_blueprint = Blueprint('bot', __name__)
bot_running = False
log_messages = []
load_dotenv()

ORDER_SIZE_RANGE = (3, 4)
ORDER_FREQUENCY_RANGE = (30, 120)
TOTHMOON_API_BASE_URL = "https://api.tothemoon.com"

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY_2 = os.getenv("ACCESS_KEY_2")
API_SECRET_2 = os.getenv("SECRET_KEY_2")

# Initialize API client
moon_api = MoonApi(TOTHMOON_API_BASE_URL, ACCESS_KEY, SECRET_KEY)
account_2 = MoonApi(TOTHMOON_API_BASE_URL, API_KEY_2, API_SECRET_2)


def append_log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_messages.append(f"[{timestamp}] {message}")


# moon_api bot wrapper functions 
def fetch_trades(trading_pair):
    append_log("Fetching latest trades...")
    try:
        trades = moon_api.get_trades_v2(trading_pair)
        if trades.status == "OK":
            for trade in trades.data[:5]:  # Log the latest 5 trades
                append_log(f"Trade ID: {trade.trade_id}, Price: {trade.price}, Amount: {trade.amount}, Time: {trade.time}")
        else:
            append_log(f"Error fetching trades: {trades.error}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")


def fetch_trading_pairs():
    append_log("Fetching trading pairs...")
    
    try:
        trading_pairs = moon_api.get_trade_pairs()
        if trading_pairs.status == "OK":
            for pair in trading_pairs.data:
                append_log(f"Base currency: {pair.base_currency}")
                append_log(f"Quoted currency: {pair.quoted_currency}")
                append_log(f"Trade pair: {pair.trade_pair}")
        else:
            append_log(f"Error fetching trades: {trading_pairs.error}")

    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")


def fetch_account_balance():
    append_log("Fetching account balances...")
    try:
        balances = moon_api.get_balances()
        append_log(f"Account balances: {balances}")
        # if trades.status == "OK":
        #     for trade in trades.data[:5]:  # Log the latest 5 trades
        #         append_log(f"Trade ID: {trade.trade_id}, Price: {trade.price}, Amount: {trade.amount}, Time: {trade.time}")
        # else:
        #     append_log(f"Error fetching trades: {trades.error}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")


def fetch_order_book(trading_pair):
    append_log("Fetching order book...")
    try:
        order_book = moon_api.get_order_book_v2(trading_pair)
        if order_book.status == "OK":
            append_log(f"Bids: {order_book.data.bids}")  
            append_log(f"Asks: {order_book.data.asks}")  
        else:
            append_log(f"Error fetching trades: {order_book.error}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")


def random_wait(random_time):
    append_log(f"Aspetto {random_time} secondi prima del prossimo ciclo...")
    time.sleep(random_time)


def get_mid_price(trading_pair) -> float:
    orders = moon_api.get_order_book_v2(trading_pair)
    append_log(f"{orders.data.asks}")
    return simple_mid_price(
        orders.data.bids, orders.data.asks
    )


def make_order(trading_pair, order_type, side, order_size, price):
    append_log("Making an order...")
    
    try:
        buy_order_data = moon_api.create_order(
            trade_pair=trading_pair, order_type=order_type, side=side,
            amount=order_size, time_in_force="GTC", price=price
        )
        append_log(f"Raw Order response: {buy_order_data}")

    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")


def cancel_order(order_id):
    append_log(f"Cancelling order: {order_id}")

    try: 
        data = moon_api.cancel_order(order_id)
        append_log(f"Raw Order response: {data}")
    except Exception as e:
        append_log(f"Exception occurred: {str(e)}")


def ping(trading_pair, mid_price: float, order_size, pong=False):
    usr_1 = "Account 1"
    usr_2 = "Account 2"
    
    if pong is True:
        usr_2 = usr_1
        usr_1 = "Account 2"

    float_mid_price = float(mid_price)
    # price = str(price_rnd(float_mid_price))
    
    append_log(f"BUY - Size: {order_size}, Prezzo: {float_mid_price} STARTED From {usr_1}: piazzo ordine di acquisto.")
    
    if pong is True:
        buy_order_data = account_2.create_order(
            trade_pair=trading_pair, order_type="LIMIT", side="BUY",
            amount=order_size, time_in_force="GTC", price=float_mid_price # ttl="", client_order_id = "", quote_order_qty="" 
        )
    else:
        buy_order_data = moon_api.create_order(
            trade_pair=trading_pair, order_type="LIMIT", side="BUY",
            amount=order_size, time_in_force="GTC",  price=float_mid_price, 
        )
    # Log Id Ordine e Attesa di un Tempo Casuale Tra 1 e 2 secondi
    append_log(f"Order Id: {buy_order_data}")
    time.sleep(random_range(tpl_range=(3,10),precision=2)) 

    append_log(f"SELL STARTED From {usr_2}: colpisco l'ordine di {usr_1} vendendo.")
    
    if pong is True:
        sell_order_data = moon_api.create_order(
            trade_pair=trading_pair, order_type="LIMIT", side="SELL",
            amount=order_size, time_in_force="GTC",  price=float_mid_price, 
        )
    else:
        sell_order_data = account_2.create_order(
            trade_pair=trading_pair, order_type="LIMIT", side="SELL",
            amount=order_size, time_in_force="GTC", price=float_mid_price
        )
    
    # Log Id Ordine e Attesa di un Tempo Casuale Tra 30 e 120 secondi
    append_log(f"Order Id: {sell_order_data}")
    random_wait(random_int(ORDER_FREQUENCY_RANGE)) # Aspetta un tempo coerente con la frequenza media di ping


def ping_pong_bot(trading_pair):
    append_log("Avvio del bot PING-PONG...")
    while True:
        try:
            order_size = random_range(ORDER_SIZE_RANGE,6)
            mid_price: str = str(get_mid_price(trading_pair))

            if mid_price is None:
                append_log("Impossibile ottenere il prezzo medio, riprovo...")
                time.sleep(5)
                continue
            # PING
            append_log(f"Price: {mid_price}")
            ping(trading_pair, mid_price, order_size)
            # PONG
            mid_price: str = str(get_mid_price(trading_pair))
            ping(trading_pair, mid_price, order_size, pong=True)
        except Exception as e:
            append_log(f"Errore nel bot: {e}")
            time.sleep(5)


@bot_blueprint.route('/start', methods=['POST'])
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        append_log("Bot started.")
        return jsonify({"message": "Bot started."}), 200
    else:
        return jsonify({"message": "Bot already running."}), 400


@bot_blueprint.route('/stop', methods=['POST'])
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        append_log("Bot stopped.")
        return jsonify({"message": "Bot stopped."}), 200
    else:
        return jsonify({"message": "Bot is not running."}), 400


@bot_blueprint.route('/fetch_trades', methods=['POST'])
def fetch_trades_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    fetch_trades(get_pair(request))

    return jsonify({"message": "Trades fetched and logged."}), 200


@bot_blueprint.route('/fetch_order_book', methods=['POST'])
def fetch_order_book_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    fetch_order_book(get_pair(request))

    return jsonify({"message": "Order book fetched and logged."}), 200


@bot_blueprint.route('/fetch_trading_pairs', methods=['POST'])
def fetch_trading_pairs_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    fetch_trading_pairs()

    return jsonify({"message": "Trading pairs and logged."}), 200


@bot_blueprint.route('/fetch_account_balance', methods=['POST'])
def fetch_account_balance_endpoint():
    if bot_running:
        fetch_account_balance()
        return jsonify({"message": "Account balance fetched and logged."}), 200
    else:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400


@bot_blueprint.route('/order', methods=['POST'])
def order_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400
    
    params: OrderParams = get_order_payload(request)
    make_order(
        params.trade_pair, params.order_type, params.side, params.amount, params.price
    )
    return jsonify({"message": "Order placed."}), 200


@bot_blueprint.route('/cancel_order', methods=['POST'])
def cancel_order_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    cancel_order(get_order_id(request))
    return jsonify({"message": "Account balance fetched and logged."}), 200


@bot_blueprint.route('/ping', methods=['POST'])
def ping_endpoint():
    if not bot_running:
        return jsonify({"message": "Bot is not running. Start the bot first."}), 400

    ping_pong_bot(get_pair(request))

    return jsonify({"message": "Order book fetched and logged."}), 200


@bot_blueprint.route('/logs', methods=['GET'])
def get_logs():
    logs = "\n".join(log_messages[-50:])
    return jsonify(logs), 200