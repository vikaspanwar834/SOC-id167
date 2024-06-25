import math
from datetime import datetime

def find_interval(f, start=-10, end=10, step=0.1):
    x = start
    while x <= end:
        if f(x) * f(x + step) < 0:
            return x, x + step
        x += step
    raise ValueError("Could not find a suitable interval")

def bisection(f, a, b, epsilon, max_iter=1000):
    if f(a) * f(b) >= 0:
        a, b = find_interval(f)
    iterations = 0
    while (b - a) / 2 > epsilon and iterations < max_iter:
        c = (a + b) / 2
        if abs(f(c)) < epsilon:
            return c, iterations
        elif f(c) * f(a) < 0:
            b = c
        else:
            a = c
        iterations += 1
    return (a + b) / 2, iterations

def newton_raphson(f, df, x0, epsilon, max_iter=1000):
    x = x0
    iterations = 0
    while abs(f(x)) > epsilon and iterations < max_iter:
        if abs(df(x)) < 1e-10:
            x = x - 0.1
        else:
            x = x - f(x) / df(x)
        iterations += 1
    return x, iterations

def secant(f, x0, x1, epsilon, max_iter=1000):
    iterations = 0
    while abs(f(x1)) > epsilon and iterations < max_iter:
        if abs(f(x1) - f(x0)) < 1e-10:
            return x1, iterations
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0, x1 = x1, x2
        iterations += 1
    return x1, iterations

def regular_falsi(f, a, b, epsilon, max_iter=1000):
    if f(a) * f(b) >= 0:
        a, b = find_interval(f)
    iterations = 0
    while abs(f(b)) > epsilon and iterations < max_iter:
        c = (a * f(b) - b * f(a)) / (f(b) - f(a))
        if abs(f(c)) < epsilon:
            return c, iterations
        elif f(c) * f(a) < 0:
            b = c
        else:
            a = c
        iterations += 1
    return b, iterations

def test_function(x):
    return x**31 - 1000

def test_function_derivative(x):
    return 31 * x**30

def test_function2(x):
    return math.sin(x)**5 * math.cos(x)**3 - math.exp(x)

def test_function3(x):
    return 1 / (1 + math.exp(-x**2 - math.sin(x) - x)) - 0.5

epsilon = 1e-3

functions = [
    (test_function, test_function_derivative, "x^31 - 1000"),
    (test_function2, None, "sin(x)^5 * cos(x)^3 - e^x"),
    (test_function3, None, "1 / (1 + e^(-x^2 - sin(x) - x)) - 1/2")
]

for f, df, name in functions:
    print(f"\nTesting function: {name}")
    
    results = []

    # Find initial interval
    try:
        a, b = find_interval(f)
    except ValueError:
        print(f"Could not find a suitable interval for {name}")
        continue

    # Bisection
    root, iterations = bisection(f, a, b, epsilon)
    results.append(("Bisection", root, iterations))

    # Newton-Raphson
    if df:
        x0 = (a + b) / 2
        root, iterations = newton_raphson(f, df, x0, epsilon)
        results.append(("Newton-Raphson", root, iterations))

    # Secant
    x0, x1 = a, b
    root, iterations = secant(f, x0, x1, epsilon)
    results.append(("Secant", root, iterations))

    # Regular Falsi
    root, iterations = regular_falsi(f, a, b, epsilon)
    results.append(("Regular Falsi", root, iterations))

    # Sort results by number of iterations
    results.sort(key=lambda x: x[2])

    # Print results with rankings
    for rank, (method, root, iterations) in enumerate(results, 1):
        print(f"Rank {rank}: {method} Method - Root = {root:.6f}, Iterations = {iterations}")
