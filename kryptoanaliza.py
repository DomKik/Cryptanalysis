import math
import numpy as np

DIVISORS_LEN = 100

divisors = np.empty(DIVISORS_LEN, dtype=int)

# 100 pierwszych liczb pierwszych
divisors[0]=2;divisors[1]=3;divisors[2]=5
divisors[3]=7;divisors[4]=11;divisors[5]=13
divisors[6]=17;divisors[7]=19;divisors[8]=23
divisors[9]=29;divisors[10]=31;divisors[11]=37
divisors[12]=41;divisors[13]=43;divisors[14]=47
divisors[15]=53;divisors[16]=59;divisors[17]=61
divisors[18]=67;divisors[19]=71;divisors[20]=73
divisors[21]=79;divisors[22]=83;divisors[23]=89
divisors[24]=97;divisors[25]=101;divisors[26]=103
divisors[27]=107;divisors[28]=109;divisors[29]=113
divisors[30]=127;divisors[31]=131;divisors[32]=137
divisors[33]=139;divisors[34]=149;divisors[35]=151
divisors[36]=157;divisors[37]=163;divisors[38]=167
divisors[39]=173;divisors[40]=179;divisors[41]=181
divisors[42]=191;divisors[43]=193;divisors[44]=197
divisors[45]=199;divisors[46]=211;divisors[47]=223
divisors[48]=227;divisors[49]=229;divisors[50]=233
divisors[51]=239;divisors[52]=241;divisors[53]=251
divisors[54]=257;divisors[55]=263;divisors[56]=269
divisors[57]=271;divisors[58]=277;divisors[59]=281
divisors[60]=283;divisors[61]=293;divisors[62]=307
divisors[63]=311;divisors[64]=313;divisors[65]=317
divisors[66]=331;divisors[67]=337;divisors[68]=347
divisors[69]=349;divisors[70]=353;divisors[71]=359
divisors[72]=367;divisors[73]=373;divisors[74]=379
divisors[75]=383;divisors[76]=389;divisors[77]=397
divisors[78]=401;divisors[79]=409;divisors[80]=419
divisors[81]=421;divisors[82]=431;divisors[83]=433
divisors[84]=439;divisors[85]=443;divisors[86]=449
divisors[87]=457;divisors[88]=461;divisors[89]=463
divisors[90]=467;divisors[91]=479;divisors[92]=487
divisors[93]=491;divisors[94]=499;divisors[95]=503
divisors[96]=509;divisors[97]=521;divisors[98]=523
divisors[99]=541

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

def prime_divisors(number):
    result = []
    number = int(abs(number))

    for i in range(DIVISORS_LEN):
        if number % divisors[i] == 0:
            result.append(int(divisors[i]))
            number //= divisors[i]

        while number % divisors[i] == 0:
            number //= divisors[i]
            
        if divisors[i] ** 2 > number:
            break

    if number > 1:
        result.append(int(number))
    return result

def divisors_power_count(number, divs):
    divs_count = len(divs)
    result = [0] * (divs_count+1)
    number = int(number)

    if number < 0:
        result[0] = 1
        number = -number

    for i, div in enumerate(divs):
        if i >= divs_count:
            break
        while number % div == 0:
            number //= div
            result[i+1] += 1

    if number > 1:
        return [-1] * divs_count
    return np.array(mod2_array(result))

def jacobi_base(n):
    divs_base = []

    for div in divisors:
        if div ** 2 > n:
            break
        if div == 2 or jacobi(n, div) == 1:
            divs_base.append(div)

    return np.array(divs_base)

def mod2_array(arr):
    for i in range(len(arr)):
        arr[i] %= 2
    return arr

def add_mod2(array1: np.array, array2: np.array):
    return mod2_array(array1 + array2)

def mul_array(array):
    r = 1
    for a in array:
        r *= a
    return r

def find_square(start_n, n):
    divs_base = jacobi_base(n)

    iter = start_n
    i = 1
    all_sums = []
    numbers_added_count = 0
    
    while True:
        i = iter - start_n
        if i > 5000:
            print("Nie znaleziono rozwiazania przez 5000 iteracji, przerywam.")
            break
        all_sums_len = len(all_sums)
        diff = iter ** 2 - n
        prime_divs_count: np.array = divisors_power_count(diff, divs_base)
        if prime_divs_count[0] == -1:
            iter += 1
            continue
        if sum(prime_divs_count) == 0:
            print(f"Rozwiazanie znaleziono w {i+1} iteracji, liczb dodanych do zbioru (czynniki pierwsze nalezace do bazy): {numbers_added_count + 1}")
            return diff

        for i in range(all_sums_len):
            suma = add_mod2(all_sums[i][0], prime_divs_count)
            numbers_mul = all_sums[i][1] + [diff]
            if sum(suma) == 0:
                print(f"Rozwiazanie znaleziono w {i+1} iteracji, liczb dodanych do zbioru (czynniki pierwsze nalezace do bazy): {numbers_added_count+1}")
                return mul_array(numbers_mul)
            
            new = [suma, numbers_mul]
            all_sums.append(new)
        
        all_sums.append([prime_divs_count, [diff]])
        numbers_added_count += 1

        iter += 1

n_tab = [29*61,37*89, 41*113, 67*139, 109*233, 151*353, 251*521, ]

for n in n_tab:
    n_square = int(math.sqrt(n))

    bin_len = len(bin(n)) - 2

    print(f"n = {n} sqrt n = {n_square}, dlugosc bitowa: {bin_len}")

    divs = jacobi_base(n)

    print("divs:", divs)

    print("szukany kwadrat:", find_square(n_square-1, n))


