def gcd(a:int, b:int) -> int:
    """
    Count gcd using recursive euclid algorihtm.

    Parameter.
    ----------
    a,b: int
        pair of integer used in euclid algorithm
    """
    if(b==0):
        return a
    else:
        return gcd(b, a%b)

def isPrime(a) -> bool:
    """
    Find is a number is prime or not.

    Parameter.
    ----------
    a: int
        integer you want to check
    """
    for n in range(2,int(a**1/2)+1):
        if a % n == 0:
            return False
    return True

def modularInverse(a:int, b:int) -> int:
    """
    Method to find modular inverse of two number.
    Return the modular inverse of two number or 0 if modular inverse not exist.
    Parameters
    ----------
    a : int
        Number you want to check modular inverse.
    b : int
        Number you want to check modular inverse.
    """
    a = a % b
    for i in range (b):
        if ((i*a) % b == 1):
            return i
    return 0