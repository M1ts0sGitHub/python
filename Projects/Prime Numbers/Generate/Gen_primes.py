import math, tqdm




def is_prime(number: int, method: int = 1) -> bool:
    global prime_numbers
    if method == 0: #Checking with all odd numbers up to the square root of the number
        max_d = math.floor(math.sqrt(number)) + 1
        for d in (2, *range(3, max_d, 2)):
            if number % d == 0 and number != d:
                # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
                return False
        return True
    elif method == 1: #Checking only with prime numbers up to the square root of the number
        ind, max_d = 0, math.floor(math.sqrt(number)) + 1
        while prime_numbers[ind] < max_d:
            if number % prime_numbers[ind] == 0:
                return False
            ind += 1
        return True
    else: #Checking only with prime numbers up to the square root of the number, with a progress bar
        max_d = math.floor(math.sqrt(number)) + 1
        prime_numbers_divisors = [prime for prime in prime_numbers if prime < max_d]
        for d in tqdm(range(len(prime_numbers_divisors)),desc=f'Checking number {number}'):
            if number % prime_numbers[d] == 0:
                return False
        return True








print(" Prime Number Generator")
print(" ---------------------")
# from_to = int(input("Number to start from: "))
# up_to = int(input("Number to stop at: "))
from_to = 4
up_to = 100


#initializing prime numbers list
prime_numbers = [2] + [num for num in range(3,50,2) if is_prime(num,0)]

#generate primes until from_to, no progress bar - quiet mode
#generate primes until up_to, with progress bar




# for i in range(from_to,up_to):
#     if is_prime(i,0):
#         print(i,end=" ")
# print()