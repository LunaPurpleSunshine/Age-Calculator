import age
import pytest
from datetime import date 


def test_calculate_age():
    assert age.calculate_age(date(1994, 7, 1)) == 26
    assert age.calculate_age(date(2050, 7, 1)) == -30
