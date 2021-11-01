from typing import Tuple

class Math:
    def gcd(self, x: int, y: int) -> int:
        while(y):
            x, y = y, x % y
        return x

    def egcd(self, x: int, y: int) -> Tuple[int, int, int]:
        if x == 0:
            return y, 0, 1

        gcd, x_hat, y_hat = self.egcd(y % x, x)

        x_res = y_hat - (y // x) * x_hat
        y_res = x_hat

        return gcd, x_res, y_res

    def modinv(self, x: int, y: int) -> int:
        gcd, x, _ = self.egcd(x, y)
        if gcd != 1:
            return Exception('Failed to compute modinv')
        return x % y
    
    def isCoprime(self, x: int, y: int) -> bool:
        return self.gcd(x, y) == 1

    def totient(self, x: int, y: int) -> int:
        return (x - 1) * (y - 1)
    
    def isPrime(self, a:int) -> bool:
        for n in range(2,int(a**1/2)+1):
            if a % n == 0:
                return False
        return True