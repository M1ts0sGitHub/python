from gmpy2 import is_prime
from math import gcd
from tqdm import tqdm
import os

def helping_data(how_many_prime_numbers: int):
    temp_prime_numbers = [2, *[n for n in range(3, 100, 2) if is_prime(n)]]

    h1 = 1
    for i in range(how_many_prime_numbers):
        h1 *= temp_prime_numbers[i]
    h2 = [i for i in tqdm(range(h1), desc='Generating Helping Data', leave=True) if gcd(i,h1)==1]
    h3 = len(h2)
    
    return h1, h2, h3
    

############ Main Code ################
# scripts folders 
root_folder = os.path.dirname(os.path.abspath(__file__))
helping_data_path = os.path.join(root_folder, 'helping_data.txt')
last_row_scanned = os.path.join(root_folder, 'last_row_scanned.txt')
prime_numbers_path = os.path.join(root_folder, 'prime_numbers.txt')
os.chdir(root_folder)
# clear console
os.system('cls')

# Helping Data
if os.path.exists(helping_data_path):
    with open(helping_data_path) as f:
        h1 = int(f.readline())
        h2 = [int(num) for num in f.readline()[1:-1].strip(']').split(',')]
        h3 = int(f.readline())
else:
    h1, h2, h3 = helping_data(8)
    with open(helping_data_path, 'w') as f:
        f.write(f'{h1}\n')
        f.write(f'{h2}\n')
        f.write(f'{h3}\n')

# Prime Numbers
if os.path.exists(prime_numbers_path):
    with open(prime_numbers_path) as f:
        prime_numbers = [int(num) for num in f.readlines()]
else:
    prime_numbers =  [2] + [num for num in range(3, 50, 2) if is_prime(num, 0)]
    for num in tqdm(range(51, h1, 2),desc=f'Row 0000'):
        if is_prime(num):
            prime_numbers.append(num)
    with open(prime_numbers_path, 'w') as f:
        for prime_number in prime_numbers:
            f.write(f'{prime_number}\n')
    with open(last_row_scanned, 'w') as f:
        f.write(f'0')

# Last Row Scanned
if os.path.exists(last_row_scanned):
    with open(last_row_scanned) as f:
        row = int(f.read())+1
else:
    row = 1


# Checking Numbers
while True:
    prime_numbers_part = []
    for i in tqdm(range(0, h3),desc=f'Row {row:04}'):
      num = h2[i] + row * h1
      if is_prime(num):
        prime_numbers_part.append(num)
    
    with open(prime_numbers_path, 'a') as f:
        for prime_number in prime_numbers_part:
            f.write(f'{prime_number}\n')
    with open(last_row_scanned, 'w') as f:
        f.write(f'{row}')
    
    prime_numbers.extend(prime_numbers_part) 
    row += 1

# lots of ram is used
# I should keep only the prime numbers i need (sqrt(n))