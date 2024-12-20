from functools import lru_cache
import timeit

@lru_cache(maxsize=None)
def riddle(num):
    digits = sorted(str(num).zfill(4))
    next_num = int(''.join(digits[::-1])) - int(''.join(digits))
    if num == next_num:
        return [next_num]
    else:
        return [num] + riddle(next_num)
def main():
    result = []
    result.append('Number;Steps;Analysis\n')
    for i in range(1,10000):
        t = riddle(i)
        result.append(f'{i};{len(t)-1};{";".join(str(x) for x in t[1:])}\n')
    with open("./Projects/Kaprekar's Constant 6174/output.csv", 'w') as csv_file:
        csv_file.writelines(result)

if __name__ == "__main__":
    times = [timeit.timeit("main()", globals=globals(), number=1) for _ in range(10)]
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    print(f"Average time taken: {avg_time} seconds")
    print(f"Max time taken: {max_time} seconds")
    print(f"Min time taken: {min_time} seconds")