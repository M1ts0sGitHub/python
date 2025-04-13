import timeit

def check_chars_set(a, b):
    return set(a).issubset(b)

def check_chars_set2(a, b):
    return set(a).issubset(set(b))

def check_chars_all(a, b):
    return all(char in b for char in set(a))

def check_chars_all2(a, b):
    return all(char in b for char in a)

def mycheck(a, b):
    set_a = sorted(set(a))
    set_b = sorted(set(b))
    for char in set_a:
        for char2 in set_b:
            if char == char2:
                break
            elif char > char2:
                return False
    return True

a = "this is a test string, with some punctuation, nothing more, nothing less. only a fucking test string. i cannot understand the point of this test string. i think that it is only a test string. how much more testing string you want to beleave this is a simple fucking test string."
# a = "test string"
b = "abcdefghijklmnopqrstuvwxyz0123456789 ."

print(mycheck(a, b))

# for i in range(20):
#     set_time = timeit.timeit(lambda: check_chars_set(a, b), number=200000)
#     set_time2 = timeit.timeit(lambda: check_chars_set2(a, b), number=200000)
#     all_time = timeit.timeit(lambda: check_chars_all(a, b), number=200000)
#     all_time2 = timeit.timeit(lambda: check_chars_all2(a, b), number=200000)
#     my_time2 = timeit.timeit(lambda: mycheck(a, b), number=200000)


#     print(f"Set: {set_time:.6f}, Set2: {set_time2:.6f}, All: {all_time:.6f} All2: {all_time2:.6f} My: {my_time2:.6f}")
