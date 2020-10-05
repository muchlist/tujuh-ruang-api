# import locale

# def rupiah_format(angka, desimal=2, prefix=True):
#     locale.setlocale(locale.LC_NUMERIC, 'IND')
#     rupiah = locale.format("%.*f", (desimal, angka), True)
#     if prefix:
#         return "Rp. {}".format(rupiah)
#     return "{}".format(rupiah)


# def rupiah_format_old(angka, desimal=2, prefix=True):
#     locale.setlocale(locale.LC_ALL, '')
#     rupiah = locale.format("%.*f", (desimal, angka), True)
#     if prefix:
#         return "Rp. {}".format(rupiah)
#     return "{}".format(rupiah)


def rupiah_format(angka: int, desimal=2, prefix=True) -> str:
    some_string = str(angka)
    some_string = some_string[::-1]
    x = 3
    res = [some_string[y-x:y] for y in range(x, len(some_string)+x, x)]

    res_join = ".".join(res)
    reverse_res = res_join[::-1]

    if prefix:
        return f"Rp. {reverse_res},00"
    return reverse_res
