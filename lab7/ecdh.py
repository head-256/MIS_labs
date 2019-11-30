import random
import des


class Point:
    def __init__(self, a, b, p, n, x, y):
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.x = x
        self.y = y

    def __add__(self, other):
        if (self.x, self.y) == (0, 0):
            return other
        if (other.x, other.y) == (0, 0):
            return self
        if self.x == other.x and (self.y != other.y or self.y == 0):
            return Point(self.a, self.b, self.p, self.n, 0, 0)
        if self.x == other.x and self.y == other.y:
            m = (3 * self.x ** 2 + self.a) * multiplicative_inverse(2 * self.y, self.p)
        else:
            m = (self.y - other.y) * multiplicative_inverse(self.x - other.x, self.p)

        x_r = (m ** 2 - self.x - other.x) % self.p
        y_r = (m * (self.x - x_r) - self.y) % self.p

        return Point(self.a, self.b, self.p, self.n, x_r, y_r)

    def __mul__(self, number):
        result = Point(self.a, self.b, self.p, self.n, 0, 0)
        addend = self

        for bit in bits(number):
            if bit == 1:
                result += addend
            addend += addend
        return result


def bits(number):
    while number:
        yield number & 1
        number >>= 1


def get_bezout_coeffs(a, b):
    # ax + by = gcd(a, b)
    x, x_, y, y_ = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, x_ = x_, x - x_ * q
        y, y_ = y_, y - y_ * q
    return x, y


def multiplicative_inverse(a, b):
    x, y = get_bezout_coeffs(a, b)
    if x < 0:
        return b + x
    return x


def generate_keys(n, G):
    d = random.randint(1, n - 1)
    H = G * d
    return d, H


if __name__ == '__main__':
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    a = 0x0
    b = 0x7
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    G = Point(a, b, p, n, x, y)

    d1, H1 = generate_keys(n, G)
    print(f"First private key: {d1:x}")
    print(f"First public key: (x={H1.x:x}, y={H1.y:x})")

    d2, H2 = generate_keys(n, G)
    print(f"Second private key: {d2:x}")
    print(f"Second public key: (x={H2.x:x}, y={H2.y:x})")

    S1 = H2 * d1
    S2 = H1 * d2

    print(f"Shared key: {S1.x:x}")

    with open("data.txt", 'r') as file:
        t = file.read()
    k = str(S1.x)
    print(f"Initial text: {t} ({des.str_to_hex(t)})")
    encrypted = des.encrypt(k, t)
    print(f"Encrypted text: {des.str_to_hex(encrypted)}")
    decrypted = des.decrypt(k, encrypted)
    print(f"Decrypted text: {decrypted} ({des.str_to_hex(decrypted)})")
