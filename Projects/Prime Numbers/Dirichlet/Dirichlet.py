from tqdm import tqdm
import math

def is_prime(number: int) -> bool:
    max_d = math.floor(math.sqrt(number)) + 1
    for d in (2, *range(3, max_d, 2)):
        if number % d == 0 and number != d:
            # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
            return False
    return True

a,b,n = 82799,2 * 3 * 5 * 7 * 11 * 13* 17* 19 * 23,1

pbar = tqdm(desc="Searching for prime", bar_format='{desc}')
while not is_prime(a+n*b):
    n += 1
    pbar.set_description(f"With n = {n}, testing number {a+n*b}")
    pbar.update(1)
pbar.close()
print(f'With n = {n}, the {a} + {n} * {b} = {a+n*b} is prime')