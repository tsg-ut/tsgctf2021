import mpmath

PREC = 100000
mpmath.mp.dps = PREC

# alpha = mpmath.mpmathify('approximation goes here')
alpha = mpmath.ln(2)

f = b"TSGCTF{sH4miKo,_muScl3_WIll_HeLp_You_wI7h_thE_pro6LeM._7r4in_YOUr_muscle.}"
f += ('X' * 2000).encode()
FLAG = int.from_bytes(f, byteorder='big')
beta = mpmath.log(mpmath.mpmathify(FLAG), 2)



def minimize_abcde(a, b, c, d, e, l, r):
    if not (0 <= c < e):
        q, c = divmod(c, e) # 0 <= c < e
        return minimize_abcde(a + b * q, b, c, d, e, l, r)

    if not (0 <= d < e):
        q, d = divmod(d, e) # 0 <= d < e
        y, x = minimize_abcde(a, b, c, d, e, l, r)
        return (y + b * q, x)

    q1, q2 = (c * l + d) // e, (c * r + d) // e

    if q1 == q2:
        if a >= 0:
            return (a * l + b * q1, l)
        else:
            return (a * r + b * q2, r)

    if a > 0:
        y1, x1 = a * l + b * q1, l
        y2, x2 = minimize_abcde(b, a, e, c - d - 1, c, q1 + 1, q2)
        x2 = (e * x2 + c - d - 1) // c
        return (y1, x1) if y1 <= y2 else (y2, x2)
    else:
        y1, x1 = a * r + b * q2, r
        y2, x2 = minimize_abcde(b, a, e, e - d - 1, c, q1, q2 - 1)
        x2 = (e * x2 + e - d - 1) // c
        return (y1, x1) if y1 < y2 else (y2, x2)

def minimize_Ax_plus_B_mod(a, b, mod, l, r):
    if mod == 1:
        return (0, l)

    a, b = a % mod, b % mod

    if a == 0:
        return (b, l)

    assert(0 <= l <= r < mod)

    y, x = minimize_abcde(a, -mod, a, b, mod, l, r)
    return (y + b, x)

def expand_to_continuous_fraction(a, b, c = 10000):
    answer = []
    next_a = a
    next_b = b
    for i in range(c):
        c_a = next_a
        c_b = next_b
        if c_b == 0:
            break
        #current_num = c_a//c_b
        current_num = mpmath.floor(c_a / c_b)

        answer.append(current_num)
        temp_next_a = c_a - current_num*c_b

        next_a = c_b
        next_b = temp_next_a
    return answer

def contract_from_continuous_fraction(list_expanded_continuous_fraction):
    l_p =[1, list_expanded_continuous_fraction[0]]
    l_q =[0, 1]
    list_expanded_continuous_fraction.pop(0)
    for ind_c_a, c_a  in enumerate(list_expanded_continuous_fraction):
        ind_pq = ind_c_a + 2
        l_p.append(c_a * l_p[ind_pq -1] + l_p[ind_pq -2])
        l_q.append(c_a * l_q[ind_pq -1] + l_q[ind_pq -2])
    answer = []
    for ind_pq in range(len(l_p)):
        answer.append( (l_p[ind_pq], l_q[ind_pq]))
    return answer

def gcd(a,b):
    if a == 0:
        return b
    while b != 0:
        a,b = b,a % b
    return a

def print_as_bytes(x):
    print(x.to_bytes((x.bit_length() + 7) // 8, byteorder='big'))

cf_n = 10000
b_cf = contract_from_continuous_fraction(expand_to_continuous_fraction(beta, 8, cf_n))
a_cf = contract_from_continuous_fraction(expand_to_continuous_fraction(alpha, 8, cf_n))

tmp_max_gcd = 1
for i, j in a_cf[-30:]:
    for k, l in b_cf[-30:]:
        if gcd(int(j), int(l)) >= tmp_max_gcd:
            tmp_max_gcd = gcd(int(j), int(l))
            tmp_denom = int(j) * int(l) // gcd(int(j), int(l))
            A, B, D = int(i) * tmp_denom // int(j), int(k) * tmp_denom // int(l), tmp_denom


import sys
import resource
sys.setrecursionlimit(2 ** 30)

y, x = minimize_Ax_plus_B_mod(A, D - B % D , D, 1, D - 1)

print(x)

test_upper_digits = int(mpmath.floor(mpmath.power(2, x * alpha - int(mpmath.floor(x * alpha - 2000)) // 8 * 8)))

print_as_bytes(test_upper_digits)
