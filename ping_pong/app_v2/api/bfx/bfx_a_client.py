import os
from bfxapi import Client

def get_bfx_client():
    """
    Returns a pre-configured Bitfinex Client instance.
    """
    return Client(api_key=os.getenv("BFX_API_KEY"), api_secret=os.getenv("BFX_SECRET"))
