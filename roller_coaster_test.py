import pytest
import pandas as pd
import numpy as np
from roller_coaster import *

def test_validate_input_file():
    # if 'sample.csv' exists:
    assert validate_input_file('sample.csv') == 'Validation successful'
    
    # if extention is not 'csv':
    with pytest.raises(SystemExit) as info:
        validate_input_file('sample.csd')
    assert str(info.value) == 'The input file must be a CSV.'
    
    # if 'nonexistent.csv' does not exist:
    with pytest.raises(SystemExit) as info:
        validate_input_file('nonexistent.csv')
    assert str(info.value) == "File 'nonexistent.csv' not found."

valid_data = {
    'formula': ['x**2+1', 'cos(x)', '-1', 'cos(x)'],
    'start_x': ['-2', '0', '3*pi', '5*pi'],
    'end_x': ['0', '3*pi', '5*pi', '7*pi']
}

dataframe_valid = pd.DataFrame(valid_data)

def test_are_formulas_valid():
    assert are_formulas_valid(dataframe_valid) is True

    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[1, 'formula'] = 'cos(xx)'
    assert are_formulas_valid(dataframe_invalid) is False

    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'formula'] = 'y * cos(x)'
    assert are_formulas_valid(dataframe_invalid2) is False


def test_is_end_larger_than_start():
    assert is_end_larger_than_start(dataframe_valid) is True

    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[0, 'start_x'] = '1'
    assert is_end_larger_than_start(dataframe_invalid) is False

    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[3, 'end_x'] = '5*pi'
    assert is_end_larger_than_start(dataframe_invalid2) is False

def test_do_ends_match_starts():
    assert do_ends_match_starts(dataframe_valid) is True

    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[2, 'end_x'] = '4*pi'
    assert do_ends_match_starts(dataframe_invalid) is False

    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'start_x'] = '-1'
    assert do_ends_match_starts(dataframe_invalid2) is False

def test_do_formulas_meet():
    assert do_formulas_meet(dataframe_valid) is True

    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[2, 'formula'] = '1.5'
    assert do_formulas_meet(dataframe_invalid) is False

    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'formula'] = 'sin(x)'
    assert do_formulas_meet(dataframe_invalid2) is False



dataframe_invalid = dataframe_valid.copy()
dataframe_invalid.at[1, 'formula'] = 'cos(x)'
print(dataframe_invalid)
print(dataframe_valid)
    


