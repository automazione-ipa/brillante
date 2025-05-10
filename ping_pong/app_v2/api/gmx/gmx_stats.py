from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
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
from gmx_python_sdk.scripts.v2.gmx_utils import (
    ConfigManager
)
from config_manager import (
    config_manager_dependency
)
router = APIRouter()

class GetGMXv2Stats:

    def __init__(self, config: ConfigManager, to_json: bool, to_csv: bool):
        self.config = config
        self.to_json = to_json
        self.to_csv = to_csv

    def get_available_liquidity(self):
        return GetAvailableLiquidity(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_borrow_apr(self):
        return GetBorrowAPR(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_claimable_fees(self):
        return GetClaimableFees(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_contract_tvl(self):
        return ContractTVL(
            self.config
        ).get_pool_balances(
            to_json=self.to_json
        )

    def get_funding_apr(self):
        return GetFundingFee(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_gm_price(self):
        return GMPrices(
            self.config
        ).get_price_traders(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_available_markets(self):
        return Markets(
            self.config
        ).get_available_markets()

    def get_open_interest(self):
        return OpenInterest(
            self.config
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_oracle_prices(self):
        return OraclePrices(
            self.config.chain
        ).get_recent_prices()

    def get_pool_tvl(self):
        return GetPoolTVL(
            self.config
        ).get_pool_balances(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_glv_stats(self):
        return GlvStats(
            self.config
        ).get_glv_stats()

@router.post("/markets")
def fetch_gmx_stats_markets(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "available_markets": stats_object.get_available_markets() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/liquidity")
def fetch_gmx_stats_liquidity(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "available_liquidity": stats_object.get_available_liquidity() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/borrow-apr")
def fetch_gmx_stats_borrow_apr(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "borrow_apr": stats_object.get_borrow_apr()() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/claimable-fees")
def fetch_gmx_stats_claimable_fees(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "claimable_fees": stats_object.get_claimable_fees() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/contract-tvl")
def fetch_gmx_stats_contract_tvl(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "contract_tvl":  stats_object.get_contract_tvl() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/funding-apr")
def fetch_gmx_stats_funding_apr(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "funding_apr": stats_object.get_funding_apr() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/gm-prices")
def fetch_gmx_stats_gm_prices(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "gm_prices": stats_object.get_gm_price() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/open-interest")
def fetch_gmx_stats_open_interest(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "open_interest": stats_object.get_open_interest() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/oracle-prices")
def fetch_gmx_stats_oracle_prices(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "oracle_prices": stats_object.get_oracle_prices() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pool-tvl")
def fetch_gmx_stats_pool_tvl(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "pool_tvl": stats_object.get_pool_tvl() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/glv")
def fetch_gmx_stats_glv(
    config: ConfigManager = Depends(config_manager_dependency),
    to_json: bool = True,
    to_csv: bool = True
):
    """
    Fetch GMX statistics based on provided chain configuration.

    Returns a dictionary containing various GMX statistics.
    """
    try:
        stats_object = GetGMXv2Stats(
            config, to_json, to_csv
        )

        stats = { "glv_stats": stats_object.get_glv_stats() }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
