

from decimal import Decimal
from typing import List, Optional, Tuple, Union
from bfxapi import Client as BFXClient
from bfxapi.exceptions import BfxBaseException

from bfxapi.types import (
    DepositAddress,
    Order,
    FundingOffer,
    LightningNetworkInvoice,
    Notification,
    PositionClaim,
    Transfer,
    Wallet,
    Withdrawal,
    DerivativePositionCollateral,
    DerivativePositionCollateralLimits,
)

from fastapi import requests
from app_v2.logic.entities import BFXOrderRequest


class ApiCallBitfinex:
    def __init__(self, api_key, secret_key):
        self.bfx = BFXClient(
            api_key=api_key,
            api_secret=secret_key,
        )
    
    # USEFUL STATS
    # TODO : Complete Find Opportunity Function which is Mocked Here. Retrieves a small list of best pairs to farm.
    def fetch_best_trading_pair(self):
        """
        Mocked function to fetch the best trading pair for farming funding rates.
        Replace this logic with a real API call to your backend for production.
        """
        # Mocking the best trading pair
        print("Fetching the best trading pair to farm funding rates...")
        return "ADA"

    # OK
    def get_funding_offer(self, symbol: str = "fUSD"):
        """Get all {symbol} active funding offers."""
        offers = self.bfx.rest.auth.get_funding_offers(symbol)

        print(f"Offers ({symbol}):", offers)
        return offers
    
    # OK
    def get_ticker_data(
            self, ticker: str = "tADAUSD"
        ):
        url = f"https://api-pub.bitfinex.com/v2/ticker/{ticker}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        data = response.json()
        print(f"Ticker: {ticker}  Data: {data}  Type: {type(data)}")

        return data

    # OK
    def get_deriv_funding_Ct_data(
            self, ticker_1: str = "tADAF0", ticker_2: str = "tETHF0", stable: str = "AUSDF0"
        ):
        url = f"https://api-pub.bitfinex.com/v2/status/deriv?keys={ticker_1}%3{stable}%2C{ticker_2}%3{stable}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        deriv = response.json()
        print(type(deriv))
        print(f"FUNDING RATE DERIV FUNDING: {ticker_1}{stable} Ct {ticker_2}{stable}\n\nDeriv Data: {deriv}")

        return deriv
    
    # OK
    def get_funding_offer(
            self,
            amount: Union[str, float, Decimal],
            rate: Union[str, float, Decimal] = 0.001,
            type: str = "LIMIT",
            symbol: str = "fUSD",
            period: int = 2,
        ):
        """Submit a new funding offer"""
        funding_offer: Notification[FundingOffer] = self.bfx.rest.auth.submit_funding_offer(
            type, symbol, amount, rate, period
        )

        print("Funding Offer notification:", funding_offer)
        return funding_offer.data

    # WALLET FUNCTIONS
    # OK - wallets = get_wallets_v2(); e.g. wallet_balance = wallets[0].balance
    def get_wallets_v2(self) -> List[Wallet]:
        wallets: List[Wallet] = self.bfx.rest.auth.get_wallets()
        return wallets
    
    # OK
    def get_btc_deposit_address(
            self, wallet: str = "exchange", method: str = "bitcoin"
        ):
        """Retrieves the deposit address for bitcoin currency in exchange wallet."""
        btc_deposit_address: Notification[DepositAddress] = self.bfx.rest.auth.get_deposit_address(
            wallet=wallet, method=method, op_renew=False
        )
        print("Deposit address:", btc_deposit_address.data)

        return btc_deposit_address.data
    
    # OK
    def deposit_lightning_invoice(
            self, wallet: str = "funding", currency: str = "LNX", amount: float = 0.001
        ):
        """Generates a lightning network deposit invoice"""
        btc_deposit: Notification[LightningNetworkInvoice] = self.bfx.rest.auth.generate_deposit_invoice(
            wallet, currency, amount
        )
        print("Lightning network invoice:", btc_deposit.data)
        return btc_deposit.data
    
    # OK
    def withdraw(
        self, 
        address: str,
        amount: float = 1.0,
        wallet: str = "exchange",
        method: str = "tetheruse",
    ):
        """Withdraws 1.0 UST from user's exchange wallet to address 0x742d35..."""
        withdrawal: Notification[Withdrawal] = self.bfx.rest.auth.submit_wallet_withdrawal(
            wallet, method, address, amount
        )
        print("Withdrawal:", withdrawal.data)
        return withdrawal.data
    
    # transfer_funds(from_wallet="exchange", to_wallet="funding", currency="ETH", currency_to="ETH", amount=0.001)
    def transfer_funds(
        self,
        amount: float = 0.001,
        from_wallet: str = "exchange",
        to_wallet: str = "funding",
        currency: str = "ETH",
        currency_to: str = "ETH",
        ):
        """Transfers funds (0.001 ETH) from exchange wallet to funding wallet."""
        transfer: Notification[Transfer] = self.bfx.rest.auth.transfer_between_wallets(
            from_wallet, to_wallet, currency, currency_to, amount
        )

        print("Transfer:", transfer.data)

        return transfer.data
    
    def claim_all(self):
        """Claims all active positions."""
        claims = []

        for position in self.bfx.rest.auth.get_positions():
            pos_claim: Notification[PositionClaim] = self.bfx.rest.auth.claim_position(
                position.position_id
            )
            claim: PositionClaim = pos_claim.data
            print(f"Position: {position} | PositionClaim: {claim}")
            claims.append(
                {
                    "position": position,
                    "claim": claim
                }
            )
        
        return claims

    # ORDER FUNCTIONS
    # OK
    def get_orders_v2(self, symbol: Optional[str], ids: Optional[List[str]]):
        """Gets all active orders."""
        try:
            orders = self.bfx.rest.auth.get_orders(symbol=symbol,ids=ids)
            return orders
        except BfxBaseException as e:
            return e

    # OK
    def bfx_submit_limit_order(
            self,
            request: BFXOrderRequest,
            short: Optional[bool] = False
        ):
        """
        Place a long order with leverage on Bitfinex.
        """
        print(f"\n\nPlacing a long order on Bitfinex: symbol={request.symbol}, amount={request.amount}, leverage={request.leverage}, price={request.price}")
        try:
            short_desc = "Long"
            amount = request.amount
            if short is True:
                short_desc = "Short"
                amount = - amount
            
            # Place a leveraged long or short order
            response = self.bfx.rest.auth.submit_order(
                type=request.order_type,
                symbol=request.symbol,
                amount=str(amount),
                price=request.price,
                lev=request.leverage
            )
            if response.status == "SUCCESS":
                print(f"\n\n{short_desc} order placed successfully:", response.data)
                return True
            else:
                print("Error placing long order:", response.status)
                return False
        except Exception as e:
            print("Exception while placing long order:", str(e))
            return False

    def collateral_min_max(self, symbol: str = "tADAF0:USTF0"):
        """Calculate the minimum and maximum collateral that can be assigned to {symbol}."""
        derivative_position_collateral_limits: DerivativePositionCollateralLimits = (
            self.bfx.rest.auth.get_derivative_position_collateral_limits(symbol)
        )

        print(
            f"Minimum collateral: {derivative_position_collateral_limits.min_collateral} | "
            f"Maximum collateral: {derivative_position_collateral_limits.max_collateral}"
        )

        return {
            "symbol": symbol,
            "max": derivative_position_collateral_limits.max_collateral, 
            "min": derivative_position_collateral_limits.min_collateral, 
        }

    # Update the amount of collateral for tADAF0:USTF0 derivative position
    # OK
    def bfx_set_collateral(
            self,
            symbol: str = "tADAF0:USTF0",
            collateral: float = 10.0
        ):
        """Increase existing order collateral on Bitfinex.
        """
        print(f"\n\Increasing collateral for an order on Bitfinex: {symbol=}, {collateral=}")
        try:
            derivative_position_collateral: DerivativePositionCollateral = (
                    self.bfx.rest.auth.set_derivative_position_collateral(
                    symbol, collateral
                )
            )
            print("Status:", bool(derivative_position_collateral.status))
            return derivative_position_collateral.status

        except Exception as e:
            print("Exception while increasing collateral:", str(e))
            return False

    # OK
    def update_order_v2(self, id: str, amount: float, price: int,):
        """Updates an order given the ID."""
        try:
            update_order_notification: Notification[Order] = self.bfx.rest.auth.update_order(
                id, amount, price
            )
            print("Update order notification:", update_order_notification)

            return update_order_notification.data
        except Exception as e:
            print("Exception while increasing collateral:", str(e))
            return False
            
    # OK
    def cancel_order_v2(
            self,
            id: Optional[int] = None,
            cid: Optional[int] = None,
            cid_date: Optional[str] = None,
        ):
        """Cancel an order given the ID."""
        cancel = self.bfx.rest.auth.cancel_order(
            id=id, cid=cid, cid_date=cid_date
        )
        
        return cancel.data
        
    # OK
    def cancel_order_multi(
            self,
            id: Optional[List[int]] = None,
            cid: Optional[List[Tuple[int, str]]] = None,
            gid: Optional[List[int]] = None,
            all: Optional[bool] = None,
    ):
        cancel_multi = self.bfx.rest.auth.cancel_order_multi(
            id=id,cid=cid,gid=gid,all=all    
        )

        return cancel_multi.data
    
    # USEFUL FUNCTIONS THAT COULD BE ADDED LATER OR WHEN SUPPORTED
    # OK
    # def check_correct_key_v2(self):
    #    try:
    #        res = self.session_v2.get_account_info()
    #        return res, True
    #    except BaseException as x:
    #        return x, False

    # OK
    # def get_last_price_v2(self):
    #    return self.session_v2.get_tickers(category="spot",symbol="STETHUSDT")

    # OK
    # def get_info_account_v2(self):
    #    try:
    #        return [self.session_v2.get_api_key_information(), True]
    #    except InvalidRequestError as e:
    #        return [e, False]

    # OK
    # def get_wallet_balance_unified_by_coin_v2(self, coin):
    #    res = self.session_v2.get_wallet_balance(
    #        accountType="UNIFIED", coin=coin)
     #   return res

    # OK
    # def get_wallet_balance_fund_v2(self):
    #    res = self.session_v2.get_coins_balance(
    #        accountType="FUND", coin="USDT")
    #    return res
