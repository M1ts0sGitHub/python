import math
import timeit

def are_coprimes(a, b):
    if max(a, b) % min(a, b) == 0 and min(a,b) != 1:
        return False
    for i in range(2, min(a,b)):
        if a % i == 0 and b % i == 0:
            return False
    return True

def are_coprimes2(a, b):
    return math.gcd(a, b) == 1

def are_coprimes3(a, b):
    while b:
        a, b = b, a % b
    return a == 1

a,b = 7787 , 317

def test_speed():
    times = []
    for func in [are_coprimes,are_coprimes2,are_coprimes3]:
        start = timeit.default_timer()
        for _ in range(10000):
            func(a,b)
        stop = timeit.default_timer()
        times.append(stop-start)
    print(f'are_coprimes: {times[0]:.3f} seconds')
    print(f'are_coprimes2: {times[1]:.3f} seconds')
    print(f'are_coprimes3: {times[2]:.3f} seconds')

test_speed()

