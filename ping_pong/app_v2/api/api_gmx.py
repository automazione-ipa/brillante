# Gmx Api
from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager
from gmx_python_sdk.scripts.v2.order.order_argument_parser import (
    OrderArgumentParser
)
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
from gmx_python_sdk.scripts.v2.order.create_increase_order import (
    IncreaseOrder, 
)
from gmx_python_sdk.scripts.v2.order.create_swap_order import (
    SwapOrder
)
from gmx_python_sdk.scripts.v2.order.create_increase_order import (
    IncreaseOrder
)
from gmx_python_sdk.scripts.v2.order.create_decrease_order import (
    DecreaseOrder
)
from gmx_python_sdk.scripts.v2.order.create_withdrawal_order import (
    WithdrawOrder
)
from gmx_python_sdk.scripts.v2.order.liquidity_argument_parser import (
    LiquidityArgumentParser
)
from gmx_python_sdk.scripts.v2.order.create_deposit_order import (
    DepositOrder
)
from gmx_python_sdk.scripts.v2.order.create_withdrawal_order import (
    WithdrawOrder
)

# Stats Start
from gmx_python_sdk.scripts.v2.get.get_available_liquidity import (
    GetAvailableLiquidity
)
from gmx_python_sdk.scripts.v2.get.get_borrow_apr import (
    GetBorrowAPR
)
from gmx_python_sdk.scripts.v2.get.get_claimable_fees import (
    GetClaimableFees
)
from gmx_python_sdk.scripts.v2.get.get_contract_balance import (
    GetPoolTVL as ContractTVL
) 
from gmx_python_sdk.scripts.v2.get.get_funding_apr import (
    GetFundingFee
)
from gmx_python_sdk.scripts.v2.get.get_gm_prices import (
    GMPrices
)
from gmx_python_sdk.scripts.v2.get.get_markets import (
    Markets
)
from gmx_python_sdk.scripts.v2.get.get_open_interest import (
    OpenInterest
)
from gmx_python_sdk.scripts.v2.get.get_oracle_prices import (
    OraclePrices
)
from gmx_python_sdk.scripts.v2.get.get_pool_tvl import (
    GetPoolTVL
)
from gmx_python_sdk.scripts.v2.get.get_glv_stats import (
    GlvStats
)
from gmx_python_sdk.scripts.v2.get.get_open_positions import (
    GetOpenPositions
)
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
# Stats End
from app_v2.logic.entities import (
    GMXIncreaseRequest,
    GMXDecreaseRequest,
    GMXSwapRequest,
    GMXDepositRequest,
    GMXWithdrawRequest,
    GMXFarmingRequest
)

class ApiCallGMX:
    def __init__(self, chain, to_json=True, to_csv=True):
        """
        Configured instance of GMX ConfigManager based on the provided chain.

        :param chain: The blockchain chain name to be used for configuration.
        :return: An instance of ConfigManager.
        """
        self.gmx_config = ConfigManager(
            chain=chain
        )
        self.gmx_config.set_config(filepath="config.yaml")
        self.to_json = to_json
        self.to_csv = to_csv

    # Stats Start
    def fetch_positions(self, address: str = None):
        """
        Get open positions for an address on a given network.
        If address is not passed it will take the address from the users config
        file.

        Parameters
        ----------
        address : str, optional
            address to fetch open positions for. The default is None.

        Returns
        -------
        positions : dict
            dictionary containing all open positions.
        """
        if address is None:
            address = self.gmx_config.user_wallet_address
            if address is None:
                raise Exception("No address passed in function or config!")

        if self.gmx_config.chain == 'arbitrum':
            positions = GetOpenPositions(config=self.gmx_config, address=address).get_data()
        else:
            positions = GetOpenPositions(config=self.gmx_config, address=address).get_raw_data()

        return {"positions": positions}

    def get_available_liquidity(self):
        return GetAvailableLiquidity(self.gmx_config).get_data(to_csv=self.to_csv, to_json=self.to_json)

    def get_borrow_apr(self):
        return GetBorrowAPR(self.gmx_config).get_data(to_csv=self.to_csv, to_json=self.to_json)

    def get_claimable_fees(self):
        return GetClaimableFees(self.gmx_config).get_data(to_csv=self.to_csv, to_json=self.to_json)

    def get_contract_tvl(self):
        return ContractTVL(self.gmx_config).get_pool_balances(to_json=self.to_json)

    def get_funding_apr(self):
        return GetFundingFee(self.gmx_config).get_data(to_csv=self.to_csv, to_json=self.to_json)

    def get_gm_price(self):
        return GMPrices(self.gmx_config).get_price_traders(to_csv=self.to_csv, to_json=self.to_json)

    def get_available_markets(self):
        return Markets(self.gmx_config).get_available_markets()

    def get_open_interest(self):
        return OpenInterest(self.gmx_config).get_data(to_csv=self.to_csv, to_json=self.to_json)

    def get_oracle_prices(self):
        return OraclePrices(self.gmx_config.chain).get_recent_prices()

    def get_pool_tvl(self):
        return GetPoolTVL(self.gmx_config).get_pool_balances(to_csv=self.to_csv, to_json=self.to_json)

    def get_glv_stats(self):
        return GlvStats(self.gmx_config).get_glv_stats()
    # Stats End

    # OK
    def submit_order(self, increase_request: GMXIncreaseRequest):
        """Endpoint to create an order on GMX."""
        increase_order_params = OrderArgumentParser(
                self.gmx_config, is_increase=True
            ).process_parameters_dictionary(
                increase_request.dict(exclude={"debug_mode"})
            )

        increase_order = IncreaseOrder(
            config=self.gmx_config,
            market_key=increase_order_params['market_key'],
            collateral_address=increase_order_params['start_token_address'],
            index_token_address=increase_order_params['index_token_address'],
            is_long=increase_order_params['is_long'],
            size_delta=increase_order_params['size_delta'],
            initial_collateral_delta_amount=(
                increase_order_params['initial_collateral_delta']
            ),
            slippage_percent=increase_order_params['slippage_percent'],
            swap_path=increase_order_params['swap_path'],
            debug_mode=increase_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": increase_order_params}

    # OK
    def increase_order(self, increase_request: GMXIncreaseRequest):
        """Endpoint to create an increase order on GMX."""
        increase_order_params = OrderArgumentParser(
            self.gmx_config, is_increase=True
        ).process_parameters_dictionary(
            increase_request.dict(exclude={"debug_mode"})
        )

        increase_order = IncreaseOrder(
            config=self.gmx_config,
            market_key=increase_order_params['market_key'],
            collateral_address=increase_order_params['start_token_address'],
            index_token_address=increase_order_params['index_token_address'],
            is_long=increase_order_params['is_long'],
            size_delta=increase_order_params['size_delta'],
            initial_collateral_delta_amount=(
                increase_order_params['initial_collateral_delta']
            ),
            slippage_percent=increase_order_params['slippage_percent'],
            swap_path=increase_order_params['swap_path'],
            debug_mode=increase_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": increase_order_params}

    #OK
    def decrease_order(self, decrease_request: GMXDecreaseRequest):
        """Endpoint to create a decrease order on GMX."""
        decrease_params = OrderArgumentParser(
            self.gmx_config, is_decrease=True
        ).process_parameters_dictionary(
            decrease_request.dict(exclude={"debug_mode"})
        )

        decrease_order = DecreaseOrder(
            config=self.gmx_config,
            market_key=decrease_params['market_key'],
            collateral_address=decrease_params['collateral_address'],
            index_token_address=decrease_params['index_token_address'],
            is_long=decrease_params['is_long'],
            size_delta=decrease_params['size_delta'],
            initial_collateral_delta_amount=decrease_params['initial_collateral_delta'],
            slippage_percent=decrease_params['slippage_percent'],
            swap_path=[],
            debug_mode=decrease_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": decrease_params}

    #OK
    def swap(self, swap_request: GMXSwapRequest):
        """Endpoint to create a swap order on GMX."""
        swap_order_parameters = OrderArgumentParser(
            self.gmx_config, is_swap=True
        ).process_parameters_dictionary(
            swap_request.dict(exclude={"debug_mode"})
        )

        swap_order = SwapOrder(
            config=self.gmx_config,
            market_key=swap_order_parameters['swap_path'][-1],
            start_token=swap_order_parameters['start_token_address'],
            out_token=swap_order_parameters['out_token_address'],
            collateral_address=swap_order_parameters['start_token_address'],
            index_token_address=swap_order_parameters['out_token_address'],
            is_long=False,
            size_delta=0,
            initial_collateral_delta_amount=(
                swap_order_parameters['initial_collateral_delta']
            ),
            slippage_percent=swap_order_parameters['slippage_percent'],
            swap_path=swap_order_parameters['swap_path'],
            debug_mode=swap_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": swap_order_parameters}

    # OK
    def deposit(self, deposit_request: GMXDepositRequest):
        """Endpoint to create a deposit order on GMX."""
        deposit_params = LiquidityArgumentParser(
            self.gmx_config, is_deposit=True
        ).process_parameters_dictionary(
            deposit_request.dict(exclude={"debug_mode"})
        )

        deposit_order = DepositOrder(
            self.gmx_config,
            market_key=deposit_params["market_key"],
            initial_long_token=deposit_params["long_token_address"],
            initial_short_token=deposit_params["short_token_address"],
            long_token_amount=deposit_params["long_token_amount"],
            short_token_amount=deposit_params["short_token_amount"],
            debug_mode=deposit_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": deposit_params}

    # OK
    def withdraw(self, withdraw_request: GMXWithdrawRequest):
        """Endpoint to create a withdraw order on GMX."""
        withdraw_params = LiquidityArgumentParser(
            self.gmx_config, is_withdrawal=True
        ).process_parameters_dictionary(
            withdraw_request.dict(exclude={"debug_mode"})
        )

        withdraw_order = WithdrawOrder(
            config=self.gmx_config,
            market_key=withdraw_params["market_key"],
            out_token=withdraw_params["out_token_address"],
            gm_amount=withdraw_params["gm_amount"],
            debug_mode=withdraw_request.debug_mode
        )

        # In debug mode, you might not want to execute the order but just see the parameters.
        return {"status": "success", "order_details": withdraw_params}
