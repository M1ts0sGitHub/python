def Collatz_Tree(steps):
    tree = [1]
    step = 0

    while step + 1 < steps:
        current_step = tree[step]
        if isinstance(current_step, list):
            next_step = []
            for num in current_step:
                parents = Collatz_Parents(num)
                if isinstance(parents, list):
                    next_step.extend(parents)
                else:
                    next_step.append(parents)
            next_step = sorted(list(set(next_step)))
            tree.append(next_step)
        else:
            next_step = Collatz_Parents(current_step)
            tree.append(next_step)
        step += 1
        print(tree[step-1])
    return tree

def Collatz_Parents(n):
    if (n - 1) % 3 == 0 and ((n - 1) // 3) % 2 != 0 and ((n - 1) // 3) != 0 and ((n - 1) // 3) != 1:
        return [(n - 1) // 3, 2 * n]
    else:
        return 2 * n

Collatz_Tree(12)