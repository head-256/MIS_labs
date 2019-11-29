import csv
import itertools
import math
import random
from sympy.ntheory.residue_ntheory import primitive_root

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


def get_primitive_root(modulo):
    # g^phi(m) = 1 mod m
    return primitive_root(modulo)


def generate_keys(size):
    p = generate_random_prime(size)
    g = get_primitive_root(p)
    while True:
        x = random.randint(1, p - 1)
        if math.gcd(x, p - 1) == 1:
            break
    y = pow(g, x, p)
    return (g, p, y), x


def encrypt(number, key):
    g, p, y = key
    while True:
        k = random.randint(1, p - 1)
        if math.gcd(k, p - 1) == 1:
            break
    a = pow(g, k, p)
    b = number * pow(y, k, p)
    return a, b


def decrypt(number, key, p):
    a, b = number
    x = key
    return b * pow(pow(a, x, p), p - 2, p) % p


def encrypt_text(message, key):
    x = [encrypt(ord(a), key) for a in message]
    return x


def decrypt_text(message, key, p):
    x = [decrypt(a, key, p) for a in message]
    return ''.join(chr(a) for a in x)


if __name__ == '__main__':
    FIRST_PRIMES_10K = get_first_primes()

    public_key, private_key = generate_keys(128)
    print("Public key: {}".format(public_key))

    with open("data.txt") as file:
        text = file.read()

    print("Initial text: {}".format(text))
    encrypted = encrypt_text(text, public_key)
    print("Encrypted array: {}".format(encrypted))
    decrypted = decrypt_text(encrypted, private_key, public_key[1])
    print("Decrypted text: {}".format(decrypted))
