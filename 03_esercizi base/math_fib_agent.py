def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


class MathAgent:
    @staticmethod
    def fibonacci_recursive(n):
        return fibonacci_recursive(n)

    @staticmethod
    def fibonacci_iterative(n):
        return fibonacci_iterative(n)


math_agent = MathAgent()

print(
    "Iterative Fibonacci:",
    math_agent.fibonacci_iterative(10)
)

print(
    "Recursive Fibonacci:",
    [MathAgent.fibonacci_recursive(i) for i in range(10)]
)
