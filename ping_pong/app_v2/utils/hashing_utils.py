from eth_abi import encode
from web3 import Web3

def create_hash(data_type_list: list, data_value_list: list):
    byte_data = encode(data_type_list, data_value_list)
    return Web3.keccak(byte_data)

def create_hash_string(string: str):
    return create_hash(["string"], [string])
