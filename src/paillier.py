import utils
import sympy
import random
import typing

class Paillier_Crypt():
    def __init__(self):
        self.math = utils.Math()
    
    def set_public_key(self, g: int, n: int):
        self.g = g
        self.n = n

    def set_private_key(self, lmd: int, miu: int):
        self.lmd = lmd
        self.miu = miu

    def generate_paillier_key(self, key_size) -> typing.Tuple[int, int, int, int]:
        # Create two prime number, p and q such as pq coprime with totient(p, q).
        finish = False
        while(not(finish)):
            p = sympy.randprime(pow(2, key_size - 1) + 1, pow(2, key_size) - 1)
            q = sympy.randprime(pow(2, key_size - 1) + 1, pow(2, key_size) - 1)
            if(self.math.isCoprime(p * q, (p - 1) * (q - 1))):
                finish = True

        # Calculate n and lambda.
        n = p * q
        lmd = self.math.lcm(p - 1, q - 1)

        # Generate random integer
        g = n
        while(self.math.gcd(g, pow(n, 2)) != 1):
            g = random.randint(n + 1, pow(n, 2) - 1)

        # Calculate miu
        L = lambda x : x - 1 // n
        miu = self.math.modinv(L(pow(g, lmd, pow(n, 2))), n)

        # Return g, n, lambda, miu.
        return g, n, lmd, miu

    # TODO: implement encrypt function, implement plaintext to block
    def encrypt(self, plain_text: str, e: int, n: int) -> str:
        pass
    
    # TODO: implement encrypt function, implement ciphertext to block
    def decrypt(self, cipher_text: str, d: int, n: int) -> str:
        pass

if __name__ == "__main__":
    paillier = Paillier_Crypt()
    paillier.generate_paillier_key(128)