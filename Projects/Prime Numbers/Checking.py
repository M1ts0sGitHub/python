import os
import tqdm

def is_prime2(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def verify_primes_in_file(file_path):
    with open(file_path, 'r') as file:
        primes_in_file = [int(line.strip()) for line in file if line.strip().isdigit()]
    all_primes = [num for num in tqdm.tqdm(range(2, max(primes_in_file) + 1)) if is_prime2(num)]
    return set(primes_in_file) == set(all_primes)


root_folder = os.path.dirname(os.path.abspath(__file__))
prime_numbers_path = os.path.join(root_folder, 'prime_numbers.txt')



if verify_primes_in_file(prime_numbers_path):
    print("All primes in the file are correct and complete.")
else:
    print("The primes in the file are not correct or incomplete.")