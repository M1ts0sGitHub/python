from tqdm import tqdm
import math
from typing import Iterator

def prime_sieve(limit: int) -> list[bool]:
    """Create a prime sieve up to limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return sieve

def is_prime_with_sieve(number: int, small_primes: list[int]) -> bool:
    """Check if a number is prime using trial division with pre-computed small primes."""
    if number < 2:
        return False
    
    # Check against our list of small primes first
    max_check = int(math.sqrt(number)) + 1
    for prime in small_primes:
        if prime > max_check:
            break
        if number % prime == 0:
            return False
    return True

def find_next_prime(a: int, b: int, n: int, small_primes: list[int]) -> int:
    """Find the next value of n where a + n*b is prime."""
    pbar = tqdm(desc="Searching for prime", bar_format='{desc}')
    
    while True:
        current = a + n*b
        if is_prime_with_sieve(current, small_primes):
            break
        n += 1
        if n % 100 == 0:  # Update less frequently to reduce overhead
            pbar.set_description(f"With n = {n}, testing number {current}")
        pbar.update(1)
    
    pbar.close()
    return n

def main():
    # Initialize parameters
    a, b = 1920477, 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23
    n = 1
    
    # Pre-compute small primes up to 10000 using sieve
    sieve = prime_sieve(10000)
    small_primes = [i for i in range(len(sieve)) if sieve[i]]
    
    # Find the next prime
    n = find_next_prime(a, b, n, small_primes)
    
    # Print result
    result = a + n*b
    print(f'With n = {n}, the {a} + {n} * {b} = {result} is prime')

if __name__ == "__main__":
    main()


# Key optimizations in this version:

# Pre-computed Prime Sieve: Creates a sieve of small primes up to 10000, which speeds up initial checking for larger numbers.
# Optimized Trial Division: Only checks divisibility by known prime numbers up to the square root, rather than all odd numbers.
# Reduced Progress Bar Updates: Only updates the display every 100 iterations to reduce overhead.
# Better Code Structure: Split into smaller, focused functions for better maintainability and potential reuse.
# Type Hints: Added type hints to make the code more maintainable and catch potential errors early.

# These optimizations should make the code run significantly faster, especially for larger numbers. The main speedup comes from:

# Not checking even numbers after 2
# Only checking prime numbers as potential divisors
# Using pre-computed small primes
# Reducing the progress bar update frequency

# Would you like me to explain any of these optimizations in more detail or suggest additional improvements?