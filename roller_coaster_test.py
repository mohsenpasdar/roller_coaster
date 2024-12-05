import pytest
import pandas as pd
from roller_coaster import *

def test_validate_input_file():
    # Test if valid CSV file passes validation
    # Here we assume that 'sample.csv' exists in the same directory:
    assert validate_input_file('sample.csv') == 'Validation successful'
    
    # Test if non-CSV file raises error
    with pytest.raises(SystemExit) as info:
        validate_input_file('sample.csd')
    assert str(info.value) == 'The input file must be a CSV.'
    
    # Test if non-existent file raises error
    with pytest.raises(SystemExit) as info:
        validate_input_file('nonexistent.csv')
    assert str(info.value) == "File 'nonexistent.csv' not found."

def test_validate_output_file():
    # Test if valid SVG file passes validation
    assert validate_output_file('output.svg') == 'Validation successful'

    # Test if non-SVG file raises error
    with pytest.raises(SystemExit) as info:
        validate_output_file('output.png')
    assert str(info.value) == 'The output file must be a SVG.'

# Define valid test data with formulas, start_x, and end_x values for testing
valid_data = {
    'formula': ['x**2+1', 'cos(x)', '-1', 'cos(x)'],
    'start_x': ['-2', '0', '3*pi', '5*pi'],
    'end_x': ['0', '3*pi', '5*pi', '7*pi']
}

# Create a DataFrame from valid test data for use in testing the helper functions
dataframe_valid = pd.DataFrame(valid_data)

def test_are_formulas_valid():
    # Test if all formulas in the valid DataFrame are correct
    assert are_formulas_valid(dataframe_valid) is True

    # Test if incorrect variable in formula causes failure
    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[1, 'formula'] = 'cos(xx)'
    assert are_formulas_valid(dataframe_invalid) is False

    # Test if presence of additional variable 'y' causes failure
    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'formula'] = 'y * cos(x)'
    assert are_formulas_valid(dataframe_invalid2) is False

    # Test if an empty formula fails
    dataframe_invalid3 = dataframe_valid.copy()
    dataframe_invalid3.at[0, 'formula'] = ''
    assert are_formulas_valid(dataframe_invalid3) is False

    # Test if non-mathematical string formula fails
    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[0, 'formula'] = 'not_a_formula'
    assert are_formulas_valid(dataframe_invalid2) is False

def test_is_end_larger_than_start():
    # Test if all end_x values are larger than start_x values in valid DataFrame
    assert is_end_larger_than_start(dataframe_valid) is True

    # Test if start_x == end_x causes failure (row 0)
    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[0, 'end_x'] = '-2'
    assert is_end_larger_than_start(dataframe_invalid) is False

    # Test if start_x > end_x causes validation failure (row 0)
    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[0, 'start_x'] = '1'
    assert is_end_larger_than_start(dataframe_invalid2) is False

    # Test if end_x <= start_x causes validation failure (row 3)
    dataframe_invalid3 = dataframe_valid.copy()
    dataframe_invalid3.at[3, 'end_x'] = '5*pi'
    assert is_end_larger_than_start(dataframe_invalid3) is False

def test_do_ends_match_starts():
    # Test if start_x matches previous row's end_x for valid DataFrame
    assert do_ends_match_starts(dataframe_valid) is True

    # Test if changing end_x causes mismatch (row 2)
    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[2, 'end_x'] = '4*pi'
    assert do_ends_match_starts(dataframe_invalid) is False

    # Test if changing start_x causes mismatch (row 1)
    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'start_x'] = '-1'
    assert do_ends_match_starts(dataframe_invalid2) is False

def test_do_formulas_meet():
    # Test if all formulas meet properly at boundaries in valid DataFrame
    assert do_formulas_meet(dataframe_valid) is True

    # Test if changing the formula to disrupt continuity at boundaries with adjacent rows causes failure (row 2)
    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[2, 'formula'] = '1.5'
    assert do_formulas_meet(dataframe_invalid) is False

    # Test if changing the formula to disrupt continuity at boundaries with adjacent rows causes failure (row 1)
    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[1, 'formula'] = 'sin(x)'
    assert do_formulas_meet(dataframe_invalid2) is False

def test_is_smooth_transition():
    # Test if valid DataFrame has smooth transitions between segments
    assert is_smooth_transition(dataframe_valid) is True

    # Test if derivative mismatch causes failure (row 1)
    dataframe_invalid = dataframe_valid.copy()
    dataframe_invalid.at[1, 'formula'] = 'cos(x)+x'
    assert is_smooth_transition(dataframe_invalid) is False

    # Test if derivative mismatch causes failure (row 2)
    dataframe_invalid2 = dataframe_valid.copy()
    dataframe_invalid2.at[2, 'formula'] = '(x-3*pi)-1'
    assert is_smooth_transition(dataframe_invalid2) is False

    # Test if transitioning between constant functions is smooth
    dataframe_invalid3 = dataframe_valid.copy()
    dataframe_invalid3['formula'] = '1'
    assert is_smooth_transition(dataframe_invalid3) is True

