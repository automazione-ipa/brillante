from app.moon_api import MoonApi

moon = MoonApi('https://api.tothemoon.com', ACCESS_KEY, SECRET_KEY)

acn_2 = MoonApi('https://api.tothemoon.com', API_KEY_2, API_SECRET_2)
orders = moon.cancel_order("171583974332")

# orders = moon.get_orders()

# print(orders)

# print(moon.get_balances())
print(moon.get_balances())
# order = acn_2.create_order( trade_pair="SWA_USDT", order_type="MARKET", side="BUY", amount="4", time_in_force="GTC")
# print(order)

