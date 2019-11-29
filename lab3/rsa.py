import itertools
import math
import random
import csv

FIRST_PRIMES_10K = []


def get_first_primes():
    primes = []
    with open("10000.txt") as file:
        reader = csv.reader(file, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            for elem in row:
                if isinstance(elem, float):
                    primes.append(int(elem))
    return primes


def generate_random_prime(size):
    p = (random.getrandbits(size) | (1 << size)) | 1
    for i in itertools.count(1):
        if is_prime(p):
            return p
        else:
            if i % (size * 2) == 0:
                p = (random.getrandbits(size) | (1 << size)) | 1
            else:
                p += 2


def is_prime(n):
    is_prime = is_prime_simple(n, 256)
    if is_prime is not None:
        return is_prime

    return is_prime_rabin_miller(n)


def is_prime_simple(number, first_primes_number):
    for p in FIRST_PRIMES_10K[:first_primes_number]:
        if number % p == 0:
            return number == p
    return None


def is_prime_rabin_miller(number):
    rounds = int(math.log2(number))
    t = number - 1
    s = 0
    # n - 1 = 2^s*t
    while t % 2 == 0:
        s += 1
        t //= 2
    generated_numbers = set()
    for _ in range(rounds):
        a = random.randint(2, number - 2)
        while a in generated_numbers:
            a = random.randint(2, number - 2)
        generated_numbers.add(a)
        x = pow(a, t, number)
        if x == 1 or x == number - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, number)
            if x == 1:
                return False
            elif x == number - 1:
                break
        else:
            return False
        continue
    return True


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


def generate_keys(size):
    p = generate_random_prime(size // 2)
    q = generate_random_prime(size // 2)
    while q == p:
        q = generate_random_prime(size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(17, phi - 1)
        # e = 65537
        if math.gcd(e, phi) == 1:
            break
    # d * e = 1 mod phi
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def rsa_encrypt(message, key):
    e, n = key
    x = [pow(ord(a), e, n) for a in message]
    return x


def rsa_decrypt(message, key):
    d, n = key
    x = [pow(a, d, n) for a in message]
    return ''.join(chr(a) for a in x)


if __name__ == '__main__':
    FIRST_PRIMES_10K = get_first_primes()

    public_key, private_key = generate_keys(256)
    print("Public key: {}".format(public_key))

    with open("data.txt") as file:
        text = file.read()

    print("Initial text: {}".format(text))
    encrypted = rsa_encrypt(text, public_key)
    print("Encrypted array: {}".format(encrypted))
    decrypted = rsa_decrypt(encrypted, private_key)
    print("Decrypted text: {}".format(decrypted))
