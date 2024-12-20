import math

def are_coprimes(a, b):
    if max(a, b) % min(a, b) == 0:
        return False
    for i in range(2, math.floor(math.sqrt(min(a, b))) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True

print(are_coprimes(1, 3))