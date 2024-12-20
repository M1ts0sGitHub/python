import math

def is_prime(number: int) -> bool:
    max_d = math.floor(math.sqrt(number)) + 1
    for d in (2, *range(3, max_d, 2)):
        if number % d == 0 and number != d:
            # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
            return False
    return True