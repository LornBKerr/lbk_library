# command --> pytest --cov-report term-missing --cov=lbk_library ../tests/

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
print(src_path)
if src_path not in sys.path:
    sys.path.append(src_path)
print(sys.path)

import pytest

from lbk_library import Validate


@pytest.fixture
def open_validate():
    validate = Validate()
    return validate


def test_01_integer_field(open_validate):
    # Test the validation function 'validate.integer_field()'
    validate = open_validate
    number = 10  # good number
    result = validate.integer_field(number, validate.REQUIRED, 1, 30)
    assert result["valid"]
    assert result["entry"] == number

    result = validate.integer_field(number, validate.OPTIONAL, 1, 30)
    assert result["valid"]
    assert result["entry"] == number

    result = validate.integer_field(number, validate.OPTIONAL, 1, 5)
    assert not result["valid"]
    assert result["entry"] == number

    result = validate.integer_field(number, validate.OPTIONAL, 20, 30)
    assert not result["valid"]
    assert result["entry"] == number

    result = validate.integer_field(None, validate.REQUIRED)
    assert not result["valid"]
    assert result["entry"] is None

    result = validate.integer_field("", validate.OPTIONAL)
    assert result["valid"]
    assert result["entry"] == 0

    result = validate.integer_field("", validate.REQUIRED)
    assert not result["valid"]
    assert result["entry"] == ""

    result = validate.integer_field(None, validate.OPTIONAL)
    assert not result["valid"]
    assert result["entry"] is None

    number = "10"  # good number
    result = validate.integer_field(number, validate.REQUIRED, 1, 30)
    assert result["valid"]
    assert result["entry"] == int(number)

    result = validate.integer_field(number, validate.OPTIONAL, 1, 30)
    assert result["valid"]
    assert result["entry"] == int(number)


def test_03_float_field(open_validate):
    validate = open_validate
    number = None
    result = validate.float_field(number, validate.REQUIRED)
    assert not result["valid"]
    result = validate.float_field(number, validate.OPTIONAL)
    assert not result["valid"]
    number = ""
    result = validate.float_field(number, validate.REQUIRED)
    assert not result["valid"]
    result = validate.float_field(number, validate.OPTIONAL)
    assert result["valid"]
    number = "10"
    result = validate.float_field(number, validate.REQUIRED)
    assert result["valid"]
    number = -10.0
    result = validate.float_field(number, validate.REQUIRED)
    assert result["valid"]
    assert result["entry"] == -10.0
    result = validate.float_field(number, validate.OPTIONAL)
    assert result["valid"]
    assert result["entry"] == -10.0
    result = validate.float_field(number, validate.OPTIONAL, 0.0)
    assert not result["valid"]
    assert result["entry"] == -10.0
    number = 20.0
    result = validate.float_field(number, validate.REQUIRED)
    assert result["valid"]
    assert result["entry"] == 20.0
    result = validate.float_field(number, validate.OPTIONAL)
    assert result["valid"]
    assert result["entry"] == 20.0
    result = validate.float_field(number, validate.OPTIONAL, 0.0, 10.0)
    assert not result["valid"]
    assert result["entry"] == 20.0


def test_04_text_field(open_validate):
    # Test the validation function 'validate_text_field()'#
    validate = open_validate
    text = None  # required, 1 <= len(text) <=255
    result = validate.text_field(text, validate.REQUIRED)
    assert not result["valid"]

    text = None  # not required, 1 <= len(text) <=255
    result = validate.text_field(text, validate.OPTIONAL)
    assert not result["valid"]

    text = ""  # required, 1 <= len(text) <=255
    result = validate.text_field(text, validate.REQUIRED)
    assert not result["valid"]

    text = "This is text"  # required, 1 <= len(text) <=255
    result = validate.text_field(text, validate.REQUIRED)
    assert result["valid"]

    text = "This is text"  # not validate.REQUIRED, 1 <= len(text) <=255
    result = validate.text_field(text, validate.OPTIONAL)
    assert result["valid"]

    text = "This is text"  # too long, 1 <= len(text) <=10
    result = validate.text_field(text, validate.REQUIRED, 1, 10)
    assert not result["valid"]

    text = "This is text"  # too short, 20 <= len(text) <=255
    result = validate.text_field(text, validate.OPTIONAL, 20)
    assert not result["valid"]


def test_05_boolean(open_validate):
    # Test the validation function 'validate.boolean()'
    validate = open_validate
    # ON values
    assert validate.boolean(True)["valid"]
    assert validate.boolean(True)["entry"]
    assert validate.boolean("true")["valid"]
    assert validate.boolean("true")["entry"]
    assert validate.boolean("on")["valid"]
    assert validate.boolean("on")["entry"]
    assert validate.boolean("1")["valid"]
    assert validate.boolean("1")["entry"]
    assert validate.boolean(1)["valid"]
    assert validate.boolean(1)["entry"]
    # OFF values
    assert validate.boolean(False)["valid"]
    assert not validate.boolean(False)["entry"]
    assert validate.boolean("false")["valid"]
    assert not validate.boolean("false")["entry"]
    assert validate.boolean("off")["valid"]
    assert not validate.boolean("off")["entry"]
    assert validate.boolean("0")["valid"]
    assert not validate.boolean("0")["entry"]
    assert validate.boolean(0)["valid"]
    assert not validate.boolean(0)["entry"]
    # invalid value
    assert not validate.boolean(2)["valid"]


def test_06_date_field(open_validate):
    # Test the validate function 'validate_date_field()'#
    validate = open_validate
    # Valid date
    assert validate.date_field("02/28/2020", validate.REQUIRED)["valid"]
    assert validate.date_field("2020-02-28", validate.REQUIRED)["valid"]
    assert not validate.date_field("", validate.OPTIONAL)["valid"]
    # Invalid Dates
    assert not validate.date_field(None, validate.REQUIRED)["valid"]
    assert not validate.date_field("", validate.REQUIRED)["valid"]
    assert not validate.date_field("02/29/2021", validate.REQUIRED)["valid"]
    assert not validate.date_field("02/20", validate.REQUIRED)["valid"]
    assert not validate.date_field("2021-02-29", validate.REQUIRED)["valid"]


# end test_01_validate.py
