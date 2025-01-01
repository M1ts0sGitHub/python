import timeit
import math


def func(num):
    for i in range(3, int(num), 2):
        _ = num**2 % i
    return

def calibrate_speed(target_duration):
    num = 1000
    elapsed_time = 0.0001
    while math.fabs(target_duration - elapsed_time) / target_duration > 0.005:
        times = [timeit.timeit(lambda: func(int(num)), number=1) for _ in range(100)]
        elapsed_time = sum(times) / len(times)
        num *= target_duration / elapsed_time
    return int(num)


if __name__ == "__main__":
    wanted_time = 0.1
    num = calibrate_speed(wanted_time)
    print(num)