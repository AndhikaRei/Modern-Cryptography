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

    def encrypt(self, plain_text: str, e: int, n: int) -> str:
        max_length = (len(str(plain_text)) - 1) // 3
        messages_int =  utils.plaintextToArrInt(plain_text, max_length)

        res = []
        for message in messages_int:
            temp = pow(message, e, n)
            res.append(str(temp).rjust(len(str(n)), '0'))

        return "".join(res)

    
    def decrypt(self, cipher_text: str, d: int, n: int) -> str:
        max_length = len(str(n))
        num_alphabet = (len(str(n))-1)//3
        messages_int = utils.ciphertextToArrInt(cipher_text, max_length)
        
        res = []
        for message in messages_int:
            temp = pow(message, d, n)
            res.append(str(temp).rjust(num_alphabet*3, "0"))

        plaintext = utils.ArrStrToPlaintext(res, num_alphabet)

        return plaintext

if __name__ == "__main__":
    rsa = RSA_Crypt()
    e, d, n = rsa.generate_rsa_key(32)
    cipher_text = rsa.encrypt('hello world', e, n)
    rsa.decrypt(cipher_text, d, n)
