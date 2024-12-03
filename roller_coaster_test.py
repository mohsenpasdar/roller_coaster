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
    'start_x': ['-2', '0', 'pi+pi+pi', '5*pi'],
    'end_x': ['0', '3*pi', '5*pi', '7*pi']
}

def test_are_valid_formula():
    dataframe_valid = pd.DataFrame(valid_data)
    assert are_valid_formula(dataframe_valid) is True

    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[1, 'formula'] = 'cos(xx)'
    assert are_valid_formula(dataframe_invalid) is False

    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'formula'] = 'y * cos(x)'
    assert are_valid_formula(dataframe_invalid2) is False





    


