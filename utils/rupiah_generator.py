import locale

# def rupiah_format(angka, desimal=2, prefix=True):
#     locale.setlocale(locale.LC_NUMERIC, 'IND')
#     rupiah = locale.format("%.*f", (desimal, angka), True)
#     if prefix:
#         return "Rp. {}".format(rupiah)
#     return "{}".format(rupiah)

def rupiah_format(angka, desimal=2, prefix=True):
    locale.setlocale(locale.LC_ALL, '')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if prefix:
        return "Rp. {}".format(rupiah)
    return "{}".format(rupiah)

# assume value is a decimal
# def rupiah_format(value, with_rp: bool= True):
#     str_value = str(value)
#     separate_decimal = str_value.split(".")
#     after_decimal = separate_decimal[0]
#     before_decimal = separate_decimal[1]

#     reverse = after_decimal[::-1]
#     temp_reverse_value = ""

#     for index, val in enumerate(reverse):
#         if (index + 1) % 3 == 0 and index + 1 != len(reverse):
#             temp_reverse_value = temp_reverse_value + val + "."
#         else:
#             temp_reverse_value = temp_reverse_value + val

#     temp_result = temp_reverse_value[::-1]

#     if with_rp:
#         return "Rp " + temp_result + "," + before_decimal
#     return temp_result + "," + before_decimal