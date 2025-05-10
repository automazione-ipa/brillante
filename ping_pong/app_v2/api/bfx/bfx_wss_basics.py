from bfxapi import Client, REST_HOST
from bfxapi.types import Notification, Order
from typing import Dict, Any

api_key = "<YOUR BFX API-KEY>"
api_secret = "<YOUR BFX API-SECRET>"

bfx = Client(
    rest_host=REST_HOST,
    api_key=api_key,
    api_secret=api_secret
)

# Quickstart
notification: Notification[Order] = bfx.rest.auth.submit_order(
    type="EXCHANGE LIMIT", symbol="tBTCUSD", amount=0.165212, price=30264.0)

order: Order = notification.data

if notification.status == "SUCCESS":
    print(f"Successful new order for {order.symbol} at {order.price}$.")

if notification.status == "ERROR":
    raise Exception(f"Something went wrong: {notification.text}")

# Client instance
PUB_WSS_HOST = "wss://api.bitfinex.com/ws/2"
PUB_WSS_HOST = "wss://api-pub.bitfinex.com/ws/2"
bfx = Client(wss_host=PUB_WSS_HOST)
# Authentication
@bfx.wss.on("authenticated")
def on_authenticated(data: Dict[str, Any]):
    print(f"Successful login for user <{data['userId']}>.")

@bfx.wss.on("authenticated")
def on_authenticated(data: Dict[str, Any]):
    if not data["caps"]["orders"]["read"]:
        raise Exception("This application requires read permissions on orders.")

    if not data["caps"]["positions"]["write"]:
        raise Exception("This application requires write permissions on positions.")
# Running the client
bfx.wss.run()

async def start():
    """
    if an event loop is already running, start the client 
    with BfxWebSocketClient::start
    """
    await bfx.wss.start()


@bfx.wss.on("open")
async def on_open():
    """
    If the client succeeds in connecting to the server, it will emit the open event.
    This is the right place for all bootstrap activities, such as subscribing to public channels. 
    """
    await bfx.wss.subscribe("ticker", symbol="tBTCUSD")

async def close():
    await bfx.wss.close(code=1001, reason="Going Away")    


@bfx.wss.on("disconnected")
def on_disconnected(code: int, reason: str):
    if code == 1000 or code == 1001:
        print("Closing the connection without errors!")

# Subscribe / Unsubscribe 
async def subscribe(): 
    await bfx.wss.subscribe("ticker", symbol="tBTCUSD")

@bfx.wss.on("subscribed")
def on_subscribed(subscription: subscriptions.Subscription):
    if subscription["channel"] == "ticker":
        print(f"{subscription['symbol']}: {subscription['sub_id']}") # tBTCUSD: f2757df2-7e11-4244-9bb7-a53b7343bef8

async def unsubscribe(sub_id:str = "f2757df2-7e11-4244-9bb7-a53b7343bef8"): 
    await bfx.wss.unsubscribe(sub_id=sub_id)
