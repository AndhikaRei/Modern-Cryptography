from typing import Tuple
import math

class Math:
    def gcd(self, x: int, y: int) -> int:
        while(y):
            x, y = y, x % y
        return x
    
    def lcm(self, x: int, y: int) -> int:
        return (x * y) // self.gcd(x, y)

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
            raise Exception('Failed to compute modinv')
        return x % y
    
    def modinv2(self, x: int, y: int) -> int:
        for i in range(y):
            if (x * i) % y == 1:
                return i
        raise Exception('Failed to compute modinv')

    def isCoprime(self, x: int, y: int) -> bool:
        return self.gcd(x, y) == 1

    def totient(self, x: int, y: int) -> int:
        return (x - 1) * (y - 1)
    
    def isPrime(self, a:int) -> bool:
        for n in range(2,int(a**1/2)+1):
            if a % n == 0:
                return False
        return True
    
    def is_square(apositiveint:int):
        x = apositiveint // 2
        seen = set([x])
        while x * x != apositiveint:
            x = (x + (apositiveint // x)) // 2
            if x in seen: return False
            seen.add(x)
        return True
    
    def is_square(i: int) -> bool:
        return i == math.isqrt(i) ** 2