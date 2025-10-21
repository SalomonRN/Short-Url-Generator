BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode(number: int) -> str:
    """Encodes an integer to a base62 string.

    Args:
        number (int): Id integer.

    Returns:
        str: Decoded str base62 string.
    """
    if number == 0:
        return BASE62[0]  # → "0"
    url = str()
    while number:
        p1, p2 = divmod(number, 62)
        url += BASE62[p2]
        number = p1
    return url[::-1]

def decode(encoded: str) -> int:
    """Decodes a base62 string to an integer.

    Args:
        encoded (str): _description_

    Returns:
        int: _description_
    """
    id = 0
    length = len(encoded)
    index = 0
    for char in encoded:
        id += BASE62.index(char) * (62 ** (length - index - 1))
        index+=1
    return id
