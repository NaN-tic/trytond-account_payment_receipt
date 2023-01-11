# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012-2014 NaN Projectes de Programari Lliure, S.L.
#                         All Rights Reserved.
#                         http://www.NaN-tic.com
#
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
##############################################################################

from decimal import Decimal
import math

SUPPORTED_LANGS = ('en', 'es', 'ca')

TENS_UNITS_SEP = {
    'en': "-",
    'es': " y ",
    'ca': "-",
}
CURRENCY_DECIMALS_SEP = {
    'en': "with",
    'es': "con",
    'ca': "amb",
}
NOT_CURRENCY_DECIMALS_SEP = {
    'en': "dot",
    'es': "coma",
    'ca': "coma",
}

CURRENCY_INTEGER_NAME = {
    0: {'en': "Euros", 'es': "Euros", 'ca': "Euros"},
    1: {'en': "Euro", 'es': "Euro", 'ca': "Euro"},
    2: {'en': "Euros", 'es': "Euros", 'ca': "Euros"},
}
CURRENCY_DECIMALS_NAME = {
    0: {'en': "Cents", 'es': "Céntimos", 'ca': "Cèntims"},
    1: {'en': "Cent", 'es': "Céntimo", 'ca': "Cèntim"},
    2: {'en': "Cents", 'es': "Céntimos", 'ca': "Cèntims"},
}

TENS = {
    20: {'en': "Twenty", 'es': "Venti", 'ca': "Vint"},
    30: {'en': "Thirty", 'es': "Treinta", 'ca': "Trenta"},
    40: {'en': "Forty", 'es': "Cuarenta", 'ca': "Quaranta"},
    50: {'en': "Fifty", 'es': "Cincuenta", 'ca': "Cinquanta"},
    60: {'en': "Sixty", 'es': "Sesenta", 'ca': "Seixanta"},
    70: {'en': "Seventy", 'es': "Setenta", 'ca': "Setanta"},
    80: {'en': "Eighty", 'es': "Ochenta", 'ca': "Vuitanta"},
    90: {'en': "Ninety", 'es': "Noventa", 'ca': "Noranta"},
}

HUNDREDS = {
    100: {'en': "One Hundred", 'es': "Ciento", 'ca': "Cent"},
    200: {'en': "Two Hundred", 'es': "Doscientos", 'ca': "Dos-cents"},
    300: {'en': "Three Hundred", 'es': "Trescientos", 'ca': "Tres-ents"},
    400: {
        'en': "Four Hundred",
        'es': "Cuatrocientos",
        'ca': "Quatre-cents"},
    500: {'en': "Five Hundred", 'es': "Quinientos", 'ca': "Cinc-cents"},
    600: {'en': "Six Hundred", 'es': "Seiscientos", 'ca': "Sis-cents"},
    700: {'en': "Seven Hundred", 'es': "Setecientos", 'ca': "Set-cents"},
    800: {'en': "Eight Hundred", 'es': "Ochocientos", 'ca': "Vuit-cents"},
    900: {'en': "Nine Hundred", 'es': "Novecientos", 'ca': "Nou-cents"},
}

GREATER = {
    1000: {'en': "One Thousand", 'es': "Mil", 'ca': "Mil"},
    1000000: {'en': "One Million", 'es': "Millones", 'ca': "Milions"},
}

UNITS = TENS.copy()
UNITS.update(HUNDREDS)
UNITS.update(GREATER)
UNITS.update({
    0: {'en': "Zero", 'es': "Cero", 'ca': "Zero"},
    1: {'en': "One", 'es': "Un", 'ca': "Un"},
    2: {'en': "Two", 'es': "Dos", 'ca': "Dos"},
    3: {'en': "Three", 'es': "Tres", 'ca': "Tres"},
    4: {'en': "Four", 'es': "Cuatro", 'ca': "Quatre"},
    5: {'en': "Five", 'es': "Cinco", 'ca': "Cinc"},
    6: {'en': "Six", 'es': "Seis", 'ca': "Sis"},
    7: {'en': "Seven", 'es': "Siete", 'ca': "Set"},
    8: {'en': "Eight", 'es': "Ocho", 'ca': "Vuit"},
    9: {'en': "Nine", 'es': "Nueve", 'ca': "Nou"},
    10: {'en': "Ten", 'es': "Diez", 'ca': "Deu"},
    11: {'en': "Eleven", 'es': "Once", 'ca': "Onze"},
    12: {'en': "Twelve", 'es': "Doce", 'ca': "Dotze"},
    13: {'en': "Thirteen", 'es': "Trece", 'ca': "Tretze"},
    14: {'en': "Fourteen", 'es': "Catorce", 'ca': "Catorze"},
    15: {'en': "Fifteen", 'es': "Quince", 'ca': "Quinze"},
    16: {'en': "Sixteen", 'es': "Dieciséis", 'ca': "Setze"},
    17: {'en': "Seventeen", 'es': "Diecisiete", 'ca': "Disset"},
    18: {'en': "Eighteen", 'es': "Dieciocho", 'ca': "Divuit"},
    19: {'en': "Nineteen", 'es': "Diecinueve", 'ca': "Dinou"},
    # When the values is exactly '20', is so called
    20: {'es': "Veinte", 'ca': "Vint"},
    21: {'es': "Veintiún", 'ca': "Vint-i-un"},
    22: {'es': "Veintidós", 'ca': "Vint-i-dos"},
    23: {'es': "Veintitrés", 'ca': "Vint-i-tres"},
    24: {'es': "Veinticuatro", 'ca': "Vint-i-quatre"},
    25: {'es': "Veinticinco", 'ca': "Vint-i-cinc"},
    26: {'es': "Veintiséis", 'ca': "Vint-i-sis"},
    27: {'es': "Veintisiete", 'ca': "Vint-i-set"},
    28: {'es': "Veintiocho", 'ca': "Vint-i-vuit"},
    29: {'es': "Veintinueve", 'ca': "Vint-i-nou"},
    # When the values is exactly '100', is so called
    100: {'en': "Hundred", 'es': "Cien", 'ca': "Cent"},
    1000: {'en': "Thousand", 'es': "Mil", 'ca': "Mil"},
    1000000: {'en': "Million", 'es': "Un Millón", 'ca': "Un Milió"},
})


def integer_to_literal(input_int, lang_code):
    assert type(input_int) == int, (
        "Invalid type of parameter. Expected 'int' "
        "but found %s" % str(type(input_int)))
    assert lang_code and lang_code in SUPPORTED_LANGS, (
        "The Language Code "
        "is not supported. The suported languages are: %s"
        % ", ".join(SUPPORTED_LANGS[:-1]) + " and " +
        SUPPORTED_LANGS[-1])

    if input_int in UNITS and lang_code in UNITS[input_int]:
        return UNITS[input_int][lang_code]

    million = int(math.floor(Decimal(str(input_int)) // 1000000))
    thousands = input_int - million * 1000000
    thousands = int(math.floor(Decimal(str(thousands)) // 1000))
    hundreds = input_int - million * 1000000 - thousands * 1000

    def __convert_hundreds(input_hundred):
        assert (input_hundred and
                type(input_hundred) == int and
                input_hundred < 1000), "Invalid Hundred input"

        if input_hundred in UNITS and lang_code in UNITS[input_hundred]:
            return [UNITS[input_hundred][lang_code]]

        res = []

        hundreds_value = (input_hundred // 100) * 100
        if hundreds_value:
            res.append(HUNDREDS[hundreds_value][lang_code])
            input_hundred -= hundreds_value
            if not input_hundred:
                return res

        if input_hundred in UNITS and lang_code in UNITS[input_hundred]:
            # values <= 30 or X0
            res.append(UNITS[input_hundred][lang_code])
            return res

        # XY; X >= 3 and y != 0
        tens_value = (input_hundred // 10) * 10
        units_value = input_hundred - tens_value
        if TENS_UNITS_SEP and lang_code in TENS_UNITS_SEP:
            res.append(TENS[tens_value][lang_code] + TENS_UNITS_SEP[lang_code]
                + UNITS[units_value][lang_code])
        else:
            res.append(TENS[tens_value][lang_code])
            res.append(UNITS[units_value][lang_code])

        return res

    converted = []
    if million:
        if million == 1:
            converted.append(UNITS[1000000][lang_code])
        else:
            converted += __convert_hundreds(million)
            converted.append(GREATER[1000000][lang_code])

        input_int -= million * 1000000

    if thousands:
        if thousands == 1:
            converted.append(UNITS[1000][lang_code])
        else:
            converted += __convert_hundreds(thousands)
            converted.append(GREATER[1000][lang_code])

    if hundreds:
        # exactly 100 is already contempleted
        converted += __convert_hundreds(hundreds)
    return " ".join(converted)


def number_to_literal(
        input_number, lang_code, rounding=0.01, is_currency=True):
    assert lang_code and lang_code in SUPPORTED_LANGS, (
        "The Language Code "
        "is not supported. The suported languages are: %s"
        % ", ".join(SUPPORTED_LANGS[:-1]) + " and " +
        SUPPORTED_LANGS[-1])

    PREC = Decimal(str(rounding))

    input_number = Decimal(str(input_number)).quantize(PREC)

    number_int = int(math.floor(input_number))
    decimals = int((input_number - number_int) * (1 / PREC))

    res = []
    res.append(integer_to_literal(number_int, lang_code))

    if is_currency:
        if (number_int in CURRENCY_INTEGER_NAME and
                lang_code in CURRENCY_INTEGER_NAME[number_int]):
            res.append(CURRENCY_INTEGER_NAME[number_int][lang_code])
        else:
            res.append(CURRENCY_INTEGER_NAME[2][lang_code])

        if decimals:
            res.append(CURRENCY_DECIMALS_SEP[lang_code])
    elif decimals:
        res.append(NOT_CURRENCY_DECIMALS_SEP[lang_code])

    if decimals:
        res.append(integer_to_literal(decimals, lang_code))
        if is_currency:
            if (decimals in CURRENCY_DECIMALS_NAME and
                    lang_code in CURRENCY_DECIMALS_NAME[decimals]):
                res.append(CURRENCY_DECIMALS_NAME[decimals][lang_code])
            else:
                res.append(CURRENCY_DECIMALS_NAME[2][lang_code])

    return " ".join(res)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
