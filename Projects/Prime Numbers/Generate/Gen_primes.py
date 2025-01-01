import math, tqdm

def is_prime(number: int, method: int = 1) -> bool:
    global prime_numbers
    if method == 0: #Checking with all odd numbers up to the square root of the number
        max_d = math.floor(math.sqrt(number)) + 1
        for d in (2, *range(3, max_d, 2)):
            if number % d == 0 and number != d:
                return False
        return True
    else: #Checking only with prime numbers up to the square root of the number
        ind , max_d = 0, math.floor(math.sqrt(number)) + 1
        while prime_numbers[ind] < max_d:
            if number % prime_numbers[ind] == 0:
                return False
            ind += 1
        return True

def helpful_primes(how_many_prime_numbers:int):
    # if file exists
    try:
        with open(f'./Projects/Prime Numbers/Generate/helping_numbers_{how_many_prime_numbers}.txt', 'r') as f:
            h1 = int(f.readline())
            h2 = [int(num) for num in f.readline()[1:-1].strip(']').split(',')]
            h3 = int(f.readline())
            print('Helping numbers loaded from file')
        return h1, h2, h3
    except Exception as e:
        print(f"Failed to read the file: {e}")

    global prime_numbers

    #Initializing Prime Numbers
    prime_numbers = [2] + [num for num in range(3,50,2) if is_prime(num,0)]

    #Generating Helping Numbers 
    h1 = 1
    for i in range(how_many_prime_numbers):
        h1 *= prime_numbers[i]
    
    print('Generating Prime Numbers for Helping in next step')
    for i in tqdm.tqdm(range(prime_numbers[-1]+2,h1,2),desc='Generating primes'):
        if is_prime(i):
            prime_numbers.append(i)
    
    h2 = prime_numbers
    for i in range(how_many_prime_numbers):
        h2.remove(prime_numbers[i])
    h2.insert(0,1)

    h3 = len(h2)

    with open(f'./Projects/Prime Numbers/Generate/helping_numbers_{how_many_prime_numbers}.txt', 'w') as f:
        f.write(f'{h1}\n')
        f.write(f'{h2}\n')
        f.write(f'{h3}\n')

    return h1,h2,h3




#initializing prime numbers list
prime_numbers = []
h1, h2, h3 = helpful_primes(3)
print(h1,h3)

print(h2)

#write to file h1, h2, h3

# row = 1
# while True:
#     for i in tqdm.tqdm(range(0,h3),desc=f'Generating primes with row {row}'):
#         num = h2[i]+row*h1
#         if is_prime(num):
#             prime_numbers.append(i)
#     row += 1
#     print(num)


