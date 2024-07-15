import numpy as np
import timeit

from math import sqrt

VECS = (
    (1.5, ),
    (1.5, 4.4),
    (1.5, 4.4, 434.1),
    #(1.5, 4.4, 2.4, 434.1),
    #(1.5, 4.4, 2.4, 434.1, 5.5, 2.2, 5.5, 2.2),
    )

def method_numpy():
    return tuple(
        float(np.linalg.norm(vec))
        for vec in VECS
        )

def _method_py(*vec):
    return sum((coord ** 2 for coord in vec)) ** (1 / 2)

def method_py():
    return tuple(
        _method_py(*vec)
        for vec in VECS
        )

def _method_py_2(vec):
    return sum((coord ** 2 for coord in vec)) ** (1 / 2)

def method_py_2():
    return tuple(
        _method_py_2(vec)
        for vec in VECS
        )

def _method_py_hardcode(vec):
    if len(vec) == 0:
        return 0

    if len(vec) == 1:
        return vec[0]

    if len(vec) == 2:
        return (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)

    if len(vec) == 3:
        return (vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2) ** (1 / 2)

    return _method_py_hardcode((
        _method_py_hardcode((
            vec[0],
            vec[1],
            )),
        *vec[2:]
        ))

def method_py_hardcode():
    return tuple(
        _method_py_hardcode(vec)
        for vec in VECS
        )

def _method_py_hardcode_alt(vec):
    if len(vec) == 0:
        return 0

    if len(vec) == 1:
        return vec[0]

    if len(vec) == 2:
        return (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)

    if len(vec) == 3:
        return (vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2) ** (1 / 2)

    return sum((coord ** 2 for coord in vec)) ** (1 / 2)

def method_py_hardcode_alt():
    return tuple(
        _method_py_hardcode_alt(vec)
        for vec in VECS
        )

def _method_py_hardcode_sqrt(vec):
    if len(vec) == 0:
        return 0

    if len(vec) == 1:
        return vec[0]

    if len(vec) == 2:
        return sqrt(vec[0] ** 2 + vec[1] ** 2)

    if len(vec) == 3:
        return sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)

    return sqrt(sum((coord ** 2 for coord in vec)))

def method_py_hardcode_sqrt():
    return tuple(
        _method_py_hardcode_sqrt(vec)
        for vec in VECS
        )

def _method_py_hardcode_half(vec):
    if len(vec) == 0:
        return 0

    if len(vec) == 1:
        return vec[0]

    if len(vec) == 2:
        return (vec[0] ** 2 + vec[1] ** 2) ** 0.5

    if len(vec) == 3:
        return (vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2) ** 0.5

    return (sum((coord ** 2 for coord in vec))) ** 0.5

def method_py_hardcode_half():
    return tuple(
        _method_py_hardcode_half(vec)
        for vec in VECS
        )

def main():
    number = 10000000
    #numpy_time = timeit.timeit(method_numpy, number=number)
    #py_time = timeit.timeit(method_py, number=number)
    #py_2_time = timeit.timeit(method_py_2, number=number)
    #py_hc_time = timeit.timeit(method_py_hardcode, number=number)
    py_hc_2_time = timeit.timeit(method_py_hardcode_alt, number=number)
    py_hc_sqrt_time = timeit.timeit(method_py_hardcode_sqrt, number=number)
    py_hc_half_time = timeit.timeit(method_py_hardcode_half, number=number)

    #print(f"NumPy method: {numpy_time:.6f} seconds")
    #print(f"Pure python method: {py_time:.6f} seconds")
    #print(f"Pure python (variant 2) method: {py_2_time:.6f} seconds")
    #print(f"Hardcoded python method: {py_hc_time:.6f} seconds")
    print(f"Hardcoded python (variant 2) method: {py_hc_2_time:.6f} seconds")
    print(f"Hardcoded python (sqrt) method: {py_hc_sqrt_time:.6f} seconds")
    print(f"Hardcoded python (half) method: {py_hc_half_time:.6f} seconds")

    #numpy_result = method_numpy()
    #py_result = method_py()
    #py_2_result = method_py_2()
    #py_hc_result = method_py_hardcode()
    py_hc_2_result = method_py_hardcode_alt()
    py_hc_sqrt_result = method_py_hardcode_sqrt()
    py_hc_half_result = method_py_hardcode_half()

    #print(numpy_result)
    #print(py_result)
    #print(py_2_result)
    #print(py_hc_result)
    print(py_hc_2_result)
    print(py_hc_sqrt_result)
    print(py_hc_half_result)

if __name__ == '__main__':
    main()

