import secrets


def secret_token(nbytes: int = 16):
    """
    Generates a secret token with nbytes num of bytes.

    :param nbytes: The token number of bytes
    """
    return secrets.token_hex(nbytes)

# print(secret_token(16))
