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
        n_square = pow(n, 2)
        lmd = self.math.lcm(p - 1, q - 1)

        # Generate random integer
        g = random.randint(1, pow(n, 2) - 1)

        # Calculate miu
        L = lambda x : (x - 1) // n
        miu = self.math.modinv(L(pow(g, lmd, n_square)), n)

        # Return g, n, lambda, miu.
        return g, n, lmd, miu

    def encrypt(self, plain_text: str, g: int, n: int) -> str:
        max_length = (len(str(plain_text)) - 1) // 3
        messages_int =  utils.plaintextToArrInt(plain_text, max_length)

        res = []
        for message in messages_int:
            # Find r
            while(True):
                r = random.randint(0, n - 1)
                if(self.math.isCoprime(r, n)):
                    break
            
            n_square = pow(n, 2)
            temp = (pow(g, message, n_square) * pow(r, n, n_square)) % n_square
            res.append(str(temp).rjust(len(str(n_square)), '0'))

        return "".join(res)
    
    # TODO: implement encrypt function, implement ciphertext to block
    def decrypt(self, cipher_text: str, lmd: int, miu: int) -> str:
        max_length = len(str(pow(n, 2)))
        num_alphabet = (len(str(n))-1)//3
        messages_int = utils.ciphertextToArrInt(cipher_text, max_length)

        L = lambda x : (x - 1) // n
        
        res = []
        for c in messages_int:
            temp = (L(pow(c, lmd, pow(n, 2))) * miu) % n
            res.append(str(temp).rjust(num_alphabet*3, "0"))

        plaintext = utils.ArrStrToPlaintext(res, num_alphabet)

        return plaintext

if __name__ == "__main__":
    paillier = Paillier_Crypt()
    g, n, lmd, miu = paillier.generate_paillier_key(128)
    plain_text = paillier.encrypt('hello world', g, n)
    cipher_text = paillier.decrypt(plain_text, lmd, miu)