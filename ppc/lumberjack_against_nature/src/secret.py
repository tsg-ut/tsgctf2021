from mpmath import mp, mpf, power, ln, exp
import json

mp.dps = 2000

fs_cache = {
    0: '101100010111001000010111111101111101000111001111011110011010101111001001111000111011001110011000000000111111001011110110101011110100000011110011010000110010011001110010100110001011011000101101100010100000110100010111010110111000101110101010111110100010101111100111101110000111011000100000011011011110101110101100100110000101010110010101010100101111101101001010111110100001101100010000111011010010111010101110001101011100000100111000001000010100010000100111010101110011101100101001000100010110100110111000001001010011111010010110110010100001011000100010010010101110100011000101000110101100101111011010000100010011000101111100001110000111111010111001111010101001101111000011101100010011011001100000001110110010010101101111101000001110110001110110010101111111011101001011011100101100111010000111101100011001110101100101010010001100101011110101110111111010011010111101001110000011000000110010010010000110010101011111101000011000011100101111001000001110001110100010110110100010110110010111110001010000111100111111110101011100011000000111111101001100101000010001111110110101101111111011100100000110000100001101001100001111100010001111111001010101000110100010111011100101011010011101011011011111110000011110111110100001010101111101001011100010001111011110000101000000000010110011100101100001011101000110000001110111010111011011100010011001000011100101110010010100001111100111001100101011010001111001110011010011001111001100110011000100111001100101100100111001001101010001010011000100110000011010000111100000101111010001110101100000100101011101001001010110011010011011001100110011010101100100101000110011011101101010100111000111111110001010010111100001010010001110100000100000011101001101101101100000000101011100111111100111101010100011000011000100100000001010010101000001011100110101000011010010110010010101010111010101000101111001101100011110000101111011100111011010111000110001001111001101101101101100011000000110110010110001000001111000111101110011010111010001101100101101101100110001101101011111010100001011010100011000010100000110010011000001100010110100110100010110001011011011001110110011011001011000010100111101011101011001100010100001100101010001101011100010011100111110111001010101011100001011011011000110100011111001011010011000001101001001011011010100111001101101001100110000101011111000100010011011010001001010000000100101010101000111001100011100110111001000111010100001011100101001001111010001001000101000101001001110111110011000110101101111010100010111011111111011110011110000011101010101001001101000101001011100000111111001010100111000101110011000001001100001101011111111110101000100011010110001110010100011110011110101111010010010001000101011100010001100011001101101001111000101010000100010000110000011111011011100100110010100001000010000100100001011101110110001011011111010111100111101100101001001111100100011011011100000001010110010000011001110111010001000011010111001000001011100000100101000110101010011110100001011110100101111100101100010000100110110001100011001011010101111010100000011000000100000000001100000111001001001100100001000001110010001101000001100010101110011001110011011101000101011111010111010011111010000010100101010110001011011011000011100110001001110100100100000011111001110111100101111000011001110001011010111001101110011100101011000110101110110001000100110010110001001000000011110011001000110101010010101000110000100010001100000110111000100111001110100100001110001010101101110000011000010100100100100000100111101010111100011011000011100000101101001011011011101001001001010101011101011110101000111001110000010011011111101101000001100001000111000101110010000101010110001000100011011101110111101011001111100011100100100100101110010110011010001100010111111101110111101100111010100001001101100010001110010000010010110111001110110000100010101110000000101111101101111011111001110101110101100100111110100010110101110110011101100101101110010111100011001110000111000001100111001110110001111011010000010011000100101000011011110101010001001000111101111000001111010111111111111001110101000100100100011011101001110000101110101111010110100101011111100100011011010101011011101100010000101110110110110101010110000001110100100100110111101000011011100000010110001101100110001110110001010000011100010001111111010110001011110010101110110011111011111100101011000100001001110000001100100001001011010010000010101001001101111101011000101000111000011111010101000010001001001111111101000111101110000111011011101000001100010101100011010011000111010011011000100110001100000110001010010101010110011001100010110000111100010001110000100001110001000100101111010001110011100111001111000101101100011110010011111001101100100111101011011100010101110111100100010111011000010111111101110011011100000100001010000111011001010010000101101000001101111101100001100011101011101111101010100100101111110000000001100010101010100101100000011110101111101001010000111010010100000000000001100101010001111010110001101100101001111000000110100000111001011111000101110110010010010000101010110110010011111100101001001110110110100101010010011000101101111001010000001010100000001111001010011110110101110110000111111011001001111000110110111100000110001010101001100011000000011001000001110001011111111011110010011001100111100111000110101011100111111101011001100010111111101110011110001000101111000010110010000001100010101010110111011110110010000111100000010001110110010001000000010001001001111110011011000010001110001101111110100111101000100010111110000101010001000101000010100111100001100110110010111011011101010001101010100101110110010000011001101101101011100110010110011110110110010001110010010100010001101010110000110010101010100111000101010000011101000101001101111111001010001101010001100111110101010011100101110111100101010110110001010010000111101110001000010000100101011001000010000101101110111100111011111111001001001110101110011000001111100110010000100011001010011001011100100101110010110100101001110110110101101000101100010101011110000010100111011000101110101000111110011101000111101000010010001111101100101010100001000001',
    13371330: '000010010111101010101110011000111010001101000001010111110110010011011010001100001100000100110000101111000100011101000100001111011011101010100101001101010001010011011010000001010100110011111001001110100001011110110011001110001111000110000001011110001000011111100110010000100101100010111101000111100100101011111000111100001000011011001010110111010011101010001000111000001110110101110000101001111100011110110111000110100000001110111110000000001011000001011111110011000001100101110100001100001011100000001111000111011100010011011100100000101100011010100011010010111000110110010011111000100000100100101010010101110111010010011101101100101111010000010011011010001100101000001101010000010000101111000011100010110100110001111000001110111110110001001001111110000001111101100100001001001010111111101111001010101010011001100111000110011000011100000001011101011111000100110110001110111101011100111000000110100011100111010001111100101101010001111100111010000110001110101110000111000010101111010000110010011111010011000011100011111110010101110010010001011000101110010110110110100111001100110000011101111001100110101100010110111110110010101011011101010000010000011101001110101011010111101101110010111110000000100000111101100111000010011011011101101000011010111000000000111011000100111011001010011100001110001100111110000111000111011001101111110100010100101111010100100111100110111111110110010000111011111000000101000001000111101000000111010001001011010101101111001110010011100111101111100010100101001010110110110100100111000011101111011010110001001001100111011011110001000000111011001001100011010011110100101100010000111111111110001001101111010000100001000000010010110010111011000111100011110110001111111001111111100010001110011110001011110011011001100111111010010011011111001100111011110011010000011011101101011101111110110101000110101110011101000110010100100100110011000111110001001000101011011011010001100110010101000001000010111101111111100010100010011110010111110010101000001010110101010010101111110011001111110001011010001010001000010011100010101100010100111011001000001100000010110111010110010000000000101010110011110101101110101001010100010011111111111101110100111111001001011101100000011000011100110100011000110111100110110110101100010101101010000100000001100001000010101011000111000111001110101000100110010000001110010010000100010110101011000001100001000001110011000111110011010000110111101001100110011011100111001110000100110111001100110111000101001010111000101010111110100111100110101001011011011011000000111101101101010100110011101100010111100001011110000001111000001100111011111110110010110001110101000110000101100011011111011111110011001111001010100010011111100011110100101101010110001010100000101001010011010111001101100111000111111011000111101100110110101010110111111011111110001011011011000001000010011001000100111011000110001010101110101100111100000001000100000110000110101011110100100000001010111111100101110001111011111100111011111011001111111001110101111000100001111010010001011110101110101110100100100101011000001111010000011000111111011001000000100111100100010100111000011010111100100110011100100100010011100101111001111111001011010110111011101101100101111101011001001101100110011110011100111100001001110101000000011010000101001011101101100011101010000101011001100110001110011110001000111100000110100001110011110101010010001110001100011110010111001110111111001011010100001001101110001011111001111100001010010111111101100001110011110110101101100101010101100110111100110010110000011110101000111001010001100010010101010111001001001110001001000101101110001011010010010010010010010111110011001000101101001110011111001101001001111101101100110011010110010000011001110100011111011011111100111011001011101110001001100001001000101001111010000011000010010111111111110011010100011110000011101110010011000011001110010010011100111001110000100110111011001010111000111100100110010010101111101011000011101100000100111111001101000011010001010101000011111010110000100110011000100011010001000111110110101000011111000000110100111111011011110100001101100110111110100001101110010101000101010000001111100011100101100111000110101110010100101100100010000011000101000100100000100001100101100110010111111101011110111011011000010010100010110100110001101010110010111011000101011111000001001010011010101010101001100001001110001011100001101110110111001001010000100011111010000010001001000000000111001011000101111001100111001100011110111110000100101001000001101011011110110010000000001001100100001110010100010100000100110100001010010010000101001101010111110101101011001101010001101000001000010111010000111100101000111010111100111111110100001011101101011010001010100001111111001111010011001101110010000001001011011111011000101011110000011111011011110100001100000000011010111001010001101001101010001100111110110100001001011101110111100110001000100100110011111111111011011100110100011001110001100001010010111101111110101100101001100111000011010010000010010001000100110101100011011101110101000010011100001010110111100100110001111000110001000110111001101111001010101111000110101110010000001001100100100011110110001011001111000001101100111011000000110001101110101011110100000011010101010111100110010011001001001101011111010010000111010100000101011111100110110000100100000101001000100111101010001100001011111110010001011010010110000000101011100011000011111100101001100111010000000010111011110100101001000000001100011101011011011110001110000001111000011100011110011001011110011000100011001001110001000010011110101101000000110010100101000001001111111001110000000101000000101110111100101101011111111111000101110111010100111111100011001000011101001000010000001101010001011001111001101111110110000111110011000011111111100010010111001110011100000011111100001010100001010111011111110100101110000110110011000111001000010000110110000011101101100100001000000011100010001000101010001011110010110000000111111011000100010101010110001110101000000111111100010000110110001000110001010011101010110001011010101110100110101100101011001001111101001110',
    123456780: '001111011010011010011101100101010100101110110010011111000111010111110001001110001011101101000011110000010000111110101100001010001000111001001011101100001100011100110111011101010001000101110001010000001100000100000100111011011111110111001111100011111000101010000110110100100100000101111000000010001100111110011011110011011011001110000100101101101100111000100101000011011111011100111100010111101110001111110110000111101010100100100111100100101011000100100000011010001000111011011011010101000110111011001100000000111001101101001110111011110010000010110100101001101100011000001011010001010000101100100110011010001001010011101001001110001101011100010101101110011101000110001100010011111111101101111000001001000011101111000000110101100001010001001100001100001111011111000010110000100110100111101100101100011000111000001111110111000000100100100100000100000110001010010010001000010111111001001110011010101001001110010100110000101101100001101011110100100000000111101101001110010100001110101001101100110001001110100000100101010111101011111100010101110000011101010100000011001010011010100101010011111110101111000011101110100001101010010101100001001101000000010011110100100010000001101111000000010110110001111001011010000010010111010001000011101000101011010100000111101110001010110000001111101101111010100011111111100111000101010011011001000111010000110110110000001010101010000010000001011101000110111101111101010111111100001000011011101011001010011100111001010101100111010110101111000100010011001000000010001001101011101100010110001000100011011001111011110001000010010010101000101010011101010100010101100110101000010001110000111010101110111011101010110111100000011100010110010100111011010100111110011010000100100111001110100111101001101111011000000101110001001011110110111011000001001110100101010010101100000101001001100001000100101011111111101110011010000100010000111010001000001000110111000011000000001100100010111011101001000001010110100010011111010001001111111001010100001101111100101100111000000111110010011101110110101110111100010000001010111010010011101100011010110101100000100001110110110111100011110110010001000100010011100001011101001110011000011110110100100100110110010001100110111010010110100100101000000111011000111100100011100111101110111010010010111100010011110000011001000111000110101001100100100001100111001011011110111110010000011010001010010010001000011000001011011001100111001011111011101100010000010101011000110100111011110111000110110000010110011011011001001001010110111001010110011100010110011010001001001111010011001010100011010011000101000001100010101110111111011111011111010111001111000101000110100011001111111111101110100011011101110000011010001001001111100111110111010101110010000011000011110100010101110001010110101100000100000101011010101010000010100111110100101110100011111100000011111000111110100110010101011000010001101111101001111010110010101011100000011011001110101110101000011011100010010000101000000100001110000011101110000010110000111100111100010110110000011110001010100010101100011110101010101000010000011101111001110001010000011011010000111101101011100010011001000000011010000000111110100000100010001100011000001000010100101100010110001010010011001000010100110001001100000010000000001101010010011000001100101111011101101110001000001101111111010011110101101001101110110100111101101111010101111101000100001000010101111000100101100010100001101000001001011011110111001100010101111100010011010001010001011100011100011100001110011100110000010000110001010110011011110101110010100010000111001000000000100011010110101100111100000000100010010111111101011101011000111011011010001000110101110101101011111001111101011100101010010110110001101001011101110100110010010001110101011000001110100111000100111110100111111000110111100010011001010001000010001100011011001011100100000001000001100111010101000011000101110000110011001000010011101110000111010111000010110011011100010101111111111001101100010100101000101111100010111010110100111100011111101010010001111111001100110110101000000101010110111100110101001111100010011101001001001010110001100100100011000010000010100100001110000000111110111001010011100111111010110110100000111000010001010010011100010111100001101000010011001100111100000010111010110001100100111000101010111011000011000110101001000110010100011010111001011110000101101011010001001110110110110001101111000101000000001101111110001010011001110010100001001010010000001000110010111000011011100011100000011010101001100110010000101010111101101111000110011110000001010101111110001011001111100001110000001110101111000100111110100011111100000110011110000100010100001011010101101100000000010011101000000111010101101011001001000001011010101111110111100100101110011001001000100010000101010000011001001110000110011111001100101111111110101011011110010000010001000100101010000110000100011100110001110011110000001100100011101111111001110110011011000100101010111011101100110001100010010101000111101010001000010110101101010010011010101011101010001000101010010011100111101100010111100110111001111110010101110110111101000010101110010111001111011001001101001010111100001111100001101011101101011111011000010001011010010010010110111100100000111010001011100000111110001011110101001101101011001110100000101000010011100001000000001000001001110111100110010111100100000000101110100101001101101111101110110000100101111001011000100101110000000111000111001110101101001011010110011100010001011101001100000111111111001000001101011110111000010110100100001101011111001110010100111111110011001001111010000101000011111110000011110001011101001100011010100110010001000000100111011011010100110100101011000110111100100010110100110101110111100011110000110010001000011111100011000000101101111100011111000011101011101011001001111010111000000011101101000000001000001010101011000110110101101101101110101100110001110000101100001000001011111000100100101011011100001001101101001101001101101101001100011101010011001110111010111111011011011100110100000111001001101001011101010111110001100111011101001000100110100101100010110111',
}

def to_string(number):
    return number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')[:74]

def decode_fast(s, e):
    for k in fs_cache:
        if k + 3 < e and e < k + 100:
            fs = fs_cache[k][(e - k - 3):]

    if fs is not None:
        f = int(fs, 2)
        size = len(fs) - 3
        sf = (s * f) % (1 << size)
        lsb = (s * f // (1 << size)) % 8
        p = mpf(sf) / mpf(1 << size) * ln(2)
        return to_string(int(exp(p) * mpf(1 << (74 * 8 + lsb))))

    p = mpf(0)
    for i in range(1, e + 1):
        p += (pow(2, e - i, 8 * i) * s % (8 * i)) / mpf(i)
    for i in range(1, mp.prec + s.bit_length()):
        p += s / mpf((e + i) << i)
    return to_string(int(power(2, p - int(p - 2000) // 8 * 8)))

flag = "TSGCTF{1t's_all_Sh4mik0's_faUlt_hoW_my_cRypt0_to0l_do3sn't_ou7put_f1ag5...}"