import utils
import sympy
import random
import typing

class RSA_Crypt():
    def __init__(self):
        self.math = utils.Math()
    
    def set_public_key(self, e: int, n: int):
        self.e = e
        self.n = n

    def set_private_key(self, d: int, n: int):
        self.d = d
        self.n = n

    def generate_rsa_key(self, key_size) -> typing.Tuple[int, int, int]:
        # Create two prime number, p and q.
        p = sympy.randprime(pow(2, key_size - 1) + 1, pow(2, key_size) - 1)
        q = sympy.randprime(pow(2, key_size - 1) + 1, pow(2, key_size) - 1)

        # Calculate n and totient(n).
        n = p * q
        totient_n = (p - 1) * (q - 1)

        # Create e such as coprime with totient(n).
        finish = False
        while(not(finish)):
            e = random.randrange(pow(2, key_size - 1), pow(2, key_size))
            if(self.math.isCoprime(e, totient_n)):
                finish = True
        
        # Calculate d.
        d = self.math.modinv(e, totient_n)

        # Set e, d, n
        self.e = e
        self.d = d
        self.n = n

        # Return e, d, n.
        return e, d, n

    # TODO: implement encrypt function, implement plaintext to block
    def encrypt(self, plain_text: str, e: int, n: int) -> str:
        pass
    
    # TODO: implement encrypt function, implement ciphertext to block
    def decrypt(self, cipher_text: str, d: int, n: int) -> str:
        pass

if __name__ == "__main__":
    pass
