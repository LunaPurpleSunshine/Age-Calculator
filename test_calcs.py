import age
import pytest
from datetime import date


def test_calculate_age():
    assert age.calculate_age(date(1994, 7, 1)) == 26
    assert age.calculate_age(date(2050, 7, 1)) == -30


def test_calculate_next_birthday():
    assert age.calculate_next_birthday(date(1994, 7, 1)) == date(2021, 7, 1)
    # assert age.calculate_next_birthday(date(2050, 7, 1)) == date(2051, 7, 1)
    assert age.calculate_next_birthday(date.today()) == date.today()


def test_expand_year():
    assert age.expand_year(15) == 2015
    assert age.expand_year(57) == 1957
    assert age.expand_year(20) == 2020
    assert age.expand_year(21) == 2021
    assert age.expand_year(22) == 1922
