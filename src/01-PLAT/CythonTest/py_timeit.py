import timeit

# 纯 Python 代码
def fib_py(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Cython 代码
import ex1

# 测试纯 Python 代码
py_time = timeit.timeit('fib_py(1000)', globals=globals(), number=1000)

# 测试 Cython 代码
cy_time = timeit.timeit('ex1.fib(1000)', globals=globals(), number=1000)

print(f"Python 时间: {py_time}")
print(f"Cython 时间: {cy_time}")