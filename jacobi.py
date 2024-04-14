def jacobi(a, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0
if __name__ == '__main__':
    p = int(input("Wprowadź wartość liczy pierwszej a:  "))
    q = int(input("Wprowadź wartość sprawdzaego modułu n: "))
    print("\nObliczam Symbol Jacobiego . . .")
    wynik = jacobi(p, q)
    if wynik == 1:
        print("\na jest resztą kwadratową modulo n : {}\n".format(wynik))
    else:
        print("\na nie jest resztą kwadratową modulo n : {}\n".format(wynik))