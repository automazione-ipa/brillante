import requests


def retrieve_yvycrv_apy() -> float:
    """
    Retrieves the current APY for the yvyCRV vault from Yearn Finance's API.

    Returns:
        The APY as a float, or 0.0 if retrieval fails.
    """
    # The endpoint URL below is an example; adjust it to the actual Yearn API endpoint
    # that returns vaults data including yvyCRV.
    api_url = "https://ydaemon.yearn.finance/1/vaults/all"

    try:
        response = requests.get(api_url, timeout=600)
        response.raise_for_status()
        vaults = response.json()

        # Loop through the vaults to find the one corresponding to yvyCRV.
        # This logic assumes that the vault entry contains a key like "symbol" or "name".
        for vault in vaults:
            # Check if the vault is for yvyCRV; adjust key and value as needed.
            if vault.get("symbol") == "yvyCRV" or vault.get(
                    "name") == "yvCurve":
                # Extract the APY. The exact key might be 'apy' or a nested structure.
                apy = vault.get("apy", 0.0)
                # Ensure the APY is a float (some APIs might return a string)
                return float(apy)
    except Exception as e:
        print(f"Error retrieving yvyCRV APY: {e}")

    return 0.0


# Simple test when running the module directly.
if __name__ == "__main__":
    apy_value = retrieve_yvycrv_apy()
    print(f"yvyCRV APY: {apy_value:.2f}%")
