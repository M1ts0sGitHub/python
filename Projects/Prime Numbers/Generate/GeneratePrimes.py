import math , time
from tqdm import tqdm
import math

class prime_numbers_generator():
    def __init__(self,from_num: int,to_num: int):
        self.prime_numbers = []
        self.initiate()
        self.generate(51,to_num)
               
    def is_prime(self, number: int, method: int = 1) -> bool:
        if method == 0:
            max_d = math.floor(math.sqrt(number)) + 1
            for d in (2, *range(3, max_d, 2)):
                if number % d == 0 and number != d:
                    # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
                    return False
            return True
        elif method == 1:
            max_d = math.floor(math.sqrt(number)) + 1

            total_primes = [prime for prime in self.prime_numbers if prime < max_d]
            for d in range(len(total_primes)):
                if number % self.prime_numbers[d] == 0:
                    # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
                    return False
            return True
        else:
            max_d = math.floor(math.sqrt(number)) + 1
            total_primes = [prime for prime in self.prime_numbers if prime < max_d]
            for d in tqdm(range(len(total_primes)),desc=f'Checking number {number}'):
                if number % self.prime_numbers[d] == 0:
                    # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
                    return False
            return True
    
    
    def initiate(self):
        for i in range(2,50):
            if self.is_prime(i,0):
                self.prime_numbers.append(i)

    def generate(self,from_num: int,to_num: int):
        for i in range(from_num,to_num,2):
            if self.is_prime(i): 
                self.prime_numbers.append(i)

png = prime_numbers_generator(99,120000)
print(png.prime_numbers)