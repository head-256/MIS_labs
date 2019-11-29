from md5 import md5

BLOCK_SIZE = 512


def bin_to_hex(binary_string):
    return '%0*X' % ((len(binary_string) + 3) // 4, int(binary_string, 2))


def hex_to_bin(hex_number, size=8):
    return bin(hex_number)[2:].zfill(size)


def str_to_bin(text):
    return ''.join(format(ord(char), 'b').zfill(8) for char in text)


def b_xor(u, v):
    return '{0:b}'.format(int(u, 2) ^ int(v, 2)).zfill(512)


def hmac(key, message):
    if len(key) > BLOCK_SIZE:
        key = md5(key)
    if len(key) < BLOCK_SIZE:
        key += "0" * (BLOCK_SIZE - len(key))

    ipad = hex_to_bin(0x36) * (BLOCK_SIZE // 8)
    opad = hex_to_bin(0x5c) * (BLOCK_SIZE // 8)

    ikeypad = b_xor(ipad, key)
    okeypad = b_xor(opad, key)

    return md5(okeypad + md5(ikeypad + message))


if __name__ == "__main__":
    key = "key"
    text = "The quick brown fox jumps over the lazy dog"
    result = bin_to_hex(hmac(str_to_bin(key), str_to_bin(text)))
    print(f"HMAC('{key}', '{text}') = {result}")
    text = "The quick brown fox jumps over the lazy dog."
    result = bin_to_hex(hmac(str_to_bin(key), str_to_bin(text)))
    print(f"HMAC('{key}', '{text}') = {result}")
    text = "md5"
    result = bin_to_hex(hmac(str_to_bin(key), str_to_bin(text)))
    print(f"HMAC('{key}', '{text}') = {result}")
    text = ""
    result = bin_to_hex(hmac(str_to_bin(key), str_to_bin(text)))
    print(f"HMAC('{key}', '{text}') = {result}")
