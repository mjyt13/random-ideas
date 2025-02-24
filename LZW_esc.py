from math import log2, ceil
from sys import getsizeof

string = 'early_to_bed_and_early_to_rise_makes_a_man_wise'
string2 = 'IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN'

# он хоть и называется словрём, но по сути это массив
# а чё, слова ищутся по номеру, который сам по себе увеличивается на 1
slovar = []
# c = len(slovar), ток зачем?

print('Шаг\tСловарь\tНомер слова\tКодовые символы\t Затраты')
def esc_code(number):
    zeroes = '0'
    zeroes *= number
    return zeroes

def LZW(enter_string):
    N = 0;
    step = 1
    n = len(enter_string)
    while N < n:
        word_num = 0
        # это часть для esc кода
        if enter_string[N] not in slovar:
            slovar.append(enter_string[N])
            # для получения количества нулей в случае отсутствия буквы в словаре
            # и соблюдения условия первого шага кусок кода
            if len(slovar) > 1:
                esc_zeros = ceil(log2(len(slovar) - 1))
                bin_dermach = format(ord(enter_string[N]), '08b')
                bin_code = esc_code(esc_zeros) + (bin_dermach)
            else:
                bin_code = format(ord(enter_string[N]), '08b')
            print(str(step) + '\t', str(enter_string[N]) + '\t', str(word_num) + '\t', str(bin_code) + '\t',
                  str(len(bin_code)) + '\t')

            N += 1
        else:
            TNT = N
            # поиск нового слова которое будет в столбце Словарь
            new_word = enter_string[TNT]
            while TNT < n - 1 and new_word in slovar:
                matched_index = slovar.index(new_word)
                TNT += 1
                new_word += enter_string[TNT]
            # столбец Номер слова
            word_num = matched_index + 1
            slovar.append(new_word)
            # к столбцу Кодовые символы
            bin_num = bin(word_num)[2:]
            diff = ceil(log2(len(slovar) - 1)) - len(bin_num)
            bin_code = esc_code(diff) + bin_num
            if len(new_word) > 1:
                N += len(new_word) - 1
                print(str(step) + '\t', str(new_word) + '\t', str(word_num) + '\t', str(bin_code) + '\t',
                      str(len(bin_code)) + '\t')
            else:
                N += 1
                print(str(step) + '\t', str(new_word) + '\t', str(word_num+1) + '\t', str(bin_code) + '\t',
                      str(len(bin_code)) + '\t')
        step += 1

LZW(string2)
# 4 вариант - НИС