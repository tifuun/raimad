import numpy as np
import timeit

A = (
    (1.1, 2.2, 3.3),
    (1.1, 2.2, 3.3),
    (1.1, 2.2, 3.3),
    )

B = (
    (4.4, 5.5, 6.6),
    (1.1, 2.2, 3.3),
    (9.1, 8.2, 7.3),
    )

C = (
    (9.1, 5.2, 7.3),
    (5.1, 0.0, 5.3),
    (4.4, 5.5, 6.6),
    )


def method_numpy():
    return tuple(map(tuple, np.array(A) @ np.array(B) @ np.array(C)))

def _method_comprehension_2x(m1, m2):
    return (
        (
            sum(a * b for a, b in zip(A_row, B_col))
            for B_col in zip(*m2)
            )
        for A_row in m1
        )

def method_comprehension():
    mat = _method_comprehension_2x(
        _method_comprehension_2x(
            A, B
            ),
        C
        )
    return tuple(map(tuple, mat))

def _method_hardcoded(*arrays):
    if len(arrays) == 1:
        return arrays[0]

    if len(arrays) == 2:
        a, b = arrays
        return (
            (
                a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0],
                a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1],
                a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2]
                ),
            
            (
                a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0],
                a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1],
                a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2]
                ),
                
            (
                a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0],
                a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1],
                a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2]
                )
            )

    return _method_hardcoded(_method_hardcoded(arrays[0], arrays[1]), *arrays[2:])

def method_hardcoded():
    return _method_hardcoded(A, B, C)

def main():
    number = 100000
    numpy_time = timeit.timeit(method_numpy, number=number)
    comprehension_time = timeit.timeit(method_comprehension, number=number)
    hardcoded_time = timeit.timeit(method_hardcoded, number=number)

    print(f"NumPy method: {numpy_time:.6f} seconds")
    print(f"Comprehension method: {comprehension_time:.6f} seconds")
    print(f"Hardcoded method: {hardcoded_time:.6f} seconds")

    numpy_result = method_numpy()
    comprehension_result = method_comprehension()
    hardcoded_result = method_hardcoded()

    print(numpy_result)
    print(comprehension_result)
    print(hardcoded_result)

    print("\nAll methods produce the same result:", 
          np.isclose(numpy_result, comprehension_result) and 
          np.isclose(numpy_result, hardcoded_result))

if __name__ == '__main__':
    main()

