import math , time
from tqdm import tqdm

class Helpful:
    def __init__(self):
        columns_number = 2 * 3 * 5 * 7 * 11 * 13 * 17  # 9699690
        c = 0
        columns = []
        max_n = 0
        max_i = 0
        # Create a tqdm progress bar
        with tqdm(total=columns_number, desc="Loading...") as pbar:
            with open("./Riddles/PrimeNumbers/output.csv", 'w') as csv_file:
                for n in range(1, columns_number + 1):
                    if not is_prime(n, 0) or n <= 13:
                        pbar.set_postfix(max_n=max_n, max_i=max_i)
                        pbar.update(1)
                        continue
                    for i in range(1, 18):
                        if is_prime(n + columns_number * i, 0):
                            csv_file.write(f"{n};{i}\n")
                            if max_i < i:
                                max_i = i
                                max_n = n
                                #save to file
                            c += 1
                            columns.append(n)
                            break
                    if n not in columns:
                        print(n, "not found")
                    pbar.set_postfix(max_n=max_n, max_i=max_i)
                    pbar.update(1)
        print(f"{c},{c/n:.6f}%")
        # print(columns)

def is_prime(number: int, method: int = 0) -> bool:
    if method == 0:
        max_d = math.floor(math.sqrt(number)) + 1
        for d in (2, *range(3, max_d, 2)):
            if number % d == 0 and number != d:
                # return False, d , int(number/d), is_prime(int(number/d),0) #Analysis
                return False
        return True
    else:
        pass

h = Helpful()

# print(is_prime(521))