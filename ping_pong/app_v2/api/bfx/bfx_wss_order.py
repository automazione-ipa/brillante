import os

from bfxapi import Client, WSS_HOST

from bfxapi.types import Notification, Order

bfx = Client(
    wss_host=WSS_HOST,
    api_key=os.getenv("BFX_API_KEY"),
    api_secret=os.getenv("BFX_API_SECRET")
)

@bfx.wss.on("authenticated")
async def on_authenticated(_):
    await bfx.wss.inputs.submit_order(
        type="EXCHANGE LIMIT", symbol="tBTCUSD", amount=0.165212, price=30264.0)

@bfx.wss.on("order_new")
def on_order_new(order: Order):
    print(f"Successful new order for {order.symbol} at {order.price}$.")

@bfx.wss.on("on-req-notification")
def on_notification(notification: Notification[Order]):
    if notification.status == "ERROR":
        raise Exception(f"Something went wrong: {notification.text}")

bfx.wss.run()