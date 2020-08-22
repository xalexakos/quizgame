from decimal import Decimal


def calculate_perc(subtotal, total):
    """ Calculates the percentage between 2 given numbers. """
    if not total:
        return '0'

    rat = Decimal((subtotal / total) * 100).quantize(Decimal('.01'))
    return str(rat).rstrip('0').rstrip('.') if '.' in str(rat) else str(rat)
