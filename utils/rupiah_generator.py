import locale

def rupiah_format(angka, desimal=2, prefix=True):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if prefix:
        return "Rp. {}".format(rupiah)
    return "{}".format(rupiah)