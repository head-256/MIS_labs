SHIFTS = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

CONSTANTS = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]


def hex_to_bin(hex_number, size=32):
    return bin(hex_number)[2:].zfill(size)


def bin_to_hex(binary_string):
    return '%0*X' % ((len(binary_string) + 3) // 4, int(binary_string, 2))


def str_to_bin(text):
    return ''.join(format(ord(char), 'b').zfill(8) for char in text)


def b_xor(u, v):
    return '{0:b}'.format(int(u, 2) ^ int(v, 2)).zfill(32)


def b_or(u, v):
    return '{0:b}'.format(int(u, 2) | int(v, 2)).zfill(32)


def b_and(u, v):
    return '{0:b}'.format(int(u, 2) & int(v, 2)).zfill(32)


def b_not(u):
    return '{0:b}'.format(int(u, 2) ^ 0xFFFFFFFF).zfill(32)


def plus_32(u, v):
    return '{0:b}'.format((int(u, 2) + int(v, 2)) % 2 ** 32).zfill(32)


def left_rotate(u, r):
    return u[r:] + u[:r]


def chunks(string, size):
    for i in range(0, len(string), size):
        yield string[i:i + size]


def to_le(string, size=8):
    return "".join(list(chunks(string, size))[::-1])


def md5(data):
    message = data
    orig_len = len(message)
    message += "1"
    while True:
        if len(message) % 512 == 448:
            break
        message += "0"
    r = "{0:b}".format(orig_len % (2 ** 64)).zfill(64)
    r1, r2 = r[:32], r[len(r) - 32:]
    message += to_le(r2) + to_le(r1)

    a0 = hex_to_bin(0x67452301)
    b0 = hex_to_bin(0xefcdab89)
    c0 = hex_to_bin(0x98badcfe)
    d0 = hex_to_bin(0x10325476)

    for chunk in chunks(message, 512):
        M = [to_le(c) for c in chunks(chunk, 32)]

        A, B, C, D = a0, b0, c0, d0

        for i in range(64):
            F = ""
            g = 0
            if 0 <= i <= 15:
                F = b_or(b_and(B, C), b_and(b_not(B), D))
                g = i
            elif 16 <= i <= 31:
                F = b_or(b_and(D, B), b_and(b_not(D), C))
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = b_xor(b_xor(B, C), D)
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = b_xor(C, b_or(B, b_not(D)))
                g = (7 * i) % 16

            F = plus_32(plus_32(plus_32(A, F), M[g]), hex_to_bin(CONSTANTS[i]))
            A = D
            D = C
            C = B
            B = plus_32(B, left_rotate(F, SHIFTS[i]))

        a0 = plus_32(A, a0)
        b0 = plus_32(B, b0)
        c0 = plus_32(C, c0)
        d0 = plus_32(D, d0)

    return to_le(a0) + to_le(b0) + to_le(c0) + to_le(d0)


if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog"
    result = bin_to_hex(md5(str_to_bin(text)))
    print(f"MD5('{text}') = {result}")
    text = "The quick brown fox jumps over the lazy dog."
    result = bin_to_hex(md5(str_to_bin(text)))
    print(f"MD5('{text}') = {result}")
    text = "md5"
    result = bin_to_hex(md5(str_to_bin(text)))
    print(f"MD5('{text}') = {result}")
    text = ""
    result = bin_to_hex(md5(str_to_bin(text)))
    print(f"MD5('{text}') = {result}")
