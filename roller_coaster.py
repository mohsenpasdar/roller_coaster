import sys
import pandas as pd
import sympy as sp

def validate_input_file(input_file: str) -> str:
    """
    Validates the input file name and content.

    This function checks if the given input file:
    1. Has a .csv extension.
    2. The first row contains the required headers: 'formula', 'start_x', and 'end_x'.

    Args:
    input_file (str): Path to the CSV file containing the roller coaster segment information.
    """
    # Check if the file name has a .csv extension.
    if not input_file.lower().endswith('.csv'):
        sys.exit('The input file must be a CSV.')

    # Open the file and read the first row to check for required headers.
    try:
        with open(input_file) as my_file:
            first_row = my_file.readline().strip().split(',')
            
            # Check if all required headers are present in the first row.
            if 'formula' not in first_row or 'start_x' not in first_row or 'end_x' not in first_row:
                sys.exit("The input file must contain headers: 'formula', 'start_x', and 'end_x'.")
    except FileNotFoundError:
        # File is not found.
        sys.exit(f"File '{input_file}' not found.")
    
    # If no errors are raised, the file is valid.
    return 'Validation successful'

def are_valid_formula(df: pd.DataFrame) -> bool:
    """
    This function checks if all formulas in the DataFrame are valid mathematical expressions with 'x' as the only variable.

    Args:
    df (pd.DataFrame): DataFrame containing roller coaster segment information, with a column named 'formula'.

    Returns:
    bool: True if all formulas are valid and only use 'x' as a variable, otherwise False.
    """
    try:
        for i in range(len(df)):
            # Convert formula string to a symbolic expression.
            formula = sp.sympify(df.loc[i, "formula"])
            
            # Define allowed variables (only 'x' is allowed here).
            allowed_vars = {sp.symbols('x')}
            
            # Check if the formula contains only allowed variables.
            if not formula.free_symbols.issubset(allowed_vars):
                return False
    except Exception:
         # If any error occurs during the conversion, return False.
        return False
    
    # If all formulas are valid, return True.
    return True

def end_larger_than_start(df: pd.DataFrame) -> bool:
    """
    This function checks if the ending value of 'x' in each row is larger than the starting value of 'x' for that row.

    Args:
    df (pd.DataFrame): DataFrame containing roller coaster segment information, with 'start_x' and 'end_x' columns.

    Returns:
    bool: True if each 'end_x' is greater than its corresponding 'start_x', otherwise False.
    """
    for i in range(len(df)):
        # Convert 'start_x' and 'end_x' from string representation to symbolic values.
        if sp.sympify(df.loc[i, "start_x"]) >= sp.sympify(df.loc[i, "end_x"]):
            # If the end value is not greater than the start value, return False.
            return False
    
    # If all checks pass, return True.
    return True

def match_end_start(df: pd.DataFrame) -> bool:
    """
    This function checks if the starting value of 'x' for each segment (except the first one) matches the ending value of 'x' from the previous segment.

    Args:
    df (pd.DataFrame): DataFrame containing roller coaster segment information, with columns 'start_x' and 'end_x'.

    Returns:
    bool: True if all consecutive segments match at their boundaries, otherwise False.
    """
    for i in range(1, len(df)):
        # Convert 'start_x' of current row and 'end_x' of previous row to symbolic values and compare them.
        if sp.sympify(df.loc[i, "start_x"]) != sp.sympify(df.loc[i - 1, "end_x"]):
            # If the values do not match, return False.
            return False
    
    # If all start and end values match properly, return True.
    return True

def are_formulas_meet(df: pd.DataFrame) -> bool:
    """
    This function checks if the end value of each formula in a row meets the start value of the formula in the next row.

    Args:
    df (pd.DataFrame): DataFrame containing roller coaster segment information with columns 'formula', 'start_x', and 'end_x'.

    Returns:
    bool: True if the end value of each formula matches the start value of the next formula, otherwise False.
    """
    # Define the symbolic variable 'x' to be used for substitution in formulas.
    x = sp.symbols("x")
    for i in range(1, len(df)):
        # Substitute 'end_x' of the previous row into the previous formula.
        # Substitute 'start_x' of the current row into the current formula.
        if sp.sympify(df.loc[i - 1, "formula"]).subs(x, df.loc[i - 1, "end_x"]) != \
           sp.sympify(df.loc[i, "formula"]).subs(x, df.loc[i, "start_x"]):
            
            # If the end value of the previous formula does not match the start value of the current formula, return False.
            return False
    
    # If all formulas meet properly at their endpoints, return True.
    return True

def is_smooth_transition(df: pd.DataFrame) -> bool:
    """
    This function hecks if the transition between each pair of consecutive formulas is smooth by comparing their derivatives.

    Args:
    df (pd.DataFrame): DataFrame containing roller coaster segment information with columns 'formula', 'start_x', and 'end_x'.

    Returns:
    bool: True if the derivative of each formula at the end of the previous segment matches the derivative of the next formula at the start of the current segment, ensuring a smooth transition. Otherwise, False.
    """
    # Define the symbolic variable 'x' to be used for differentiation and substitution in formulas.
    x = sp.symbols("x")
    for i in range(1, len(df)):
        # Calculate the derivative of the previous formula (to the current row) and substitute 'end_x' value.
        previous_derivative = sp.diff(sp.sympify(df.loc[i - 1, "formula"]), x).subs(x, df.loc[i - 1, "end_x"])
        
        # Calculate the derivative of the current formula (in a row) and substitute 'start_x' value.
        current_derivative = sp.diff(sp.sympify(df.loc[i, "formula"]), x).subs(x, df.loc[i, "start_x"])
        
        # Check if the derivatives at the transition point are equal.
        if previous_derivative != current_derivative:
            # If derivatives do not match, return False.
            return False

    # If all transitions are smooth, return True.
    return True


def roller_coaster(df: pd.DataFrame, drawing_file: str):
    """
    This function generates a plot of the roller coaster using the formulas from the DataFrame and saves it as an SVG file.

    Args:
    df (pd.DataFrame): DataFrame containing roller coaster segment information with columns 'formula', 'start_x', and 'end_x'.
    drawing_file (str): The name of the SVG file to save the roller coaster plot.

    Returns:
    None
    """
    # Define the symbolic variable 'x' for plotting the formulas.
    x = sp.symbols("x")
    
    # Create the initial plot for the first formula with its corresponding range.
    p1 = sp.plot(sp.sympify(df.loc[0, 'formula']), (x, sp.sympify(df.loc[0, "start_x"]), sp.sympify(df.loc[0, "end_x"])), 
                 show=False, xlabel='Horizontal Position', ylabel='Vertical Height')
    
    # Loop through the remaining rows of the DataFrame and extend the plot with each formula.
    for i in range(1, len(df)):
        p1.extend(sp.plot(sp.sympify(df.loc[i, 'formula']), (x, sp.sympify(df.loc[i, "start_x"]), sp.sympify(df.loc[i, "end_x"])), show=False))
    
    # Save the final plot to the specified SVG file.
    p1.save(drawing_file)

def generate_roller_coaster():
    """
    This function prompts the user to enter input and output file names, validates the input data, and generates a roller coaster drawing.

    This function reads the roller coaster segment information from a CSV file provided by the user, 
    validates the formulas and transitions, and then generates an SVG image of the roller coaster.

    Args:
    None

    Returns:
    None
    """
    # Prompt user for the input CSV file path containing formulas.
    formulas_file_path = input('Enter the input file name (including the extention) corresponding ' +
                               'to the CSV file with the formulas to be used for the roller coaster: ')
    
    # Validate the input CSV file to ensure it has the correct format and includes required headers.
    validate_input_file(formulas_file_path)
    
    # Load the CSV data into a DataFrame.
    formulas_df = pd.read_csv(formulas_file_path)
    
    # Validate if all formulas in the DataFrame are valid.
    if not are_valid_formula(formulas_df):
        sys.exit('At least, one of the formulas is not valid!')

    # Validate if the end value of 'x' is greater than the start value for each row.  
    if not end_larger_than_start(formulas_df):
        sys.exit('At least, the ending value of x in one of the rows is not larger ' + 
                 'than the start value of x for the same row!')
    
    # Validate if the start value of 'x' matches the end value of 'x' in the previous row (except the first row).
    if not match_end_start(formulas_df):
        sys.exit('At least, the starting value of x in one of the rows (other than the first one) ' + 
                 "doesn't match the ending value of x in its previous row!")    
    
    # Validate if the end value of one formula matches the start value of the next formula.
    if not are_formulas_meet(formulas_df):
        sys.exit('At least, for an x between two consecutive rows, the corresponding formulas (e.g.: f and g) ' +
                 'do not meet at the same location (i.e.: f(x) != g(x))!')
    
    # Validate if the transition between consecutive formulas is smooth (i.e., their derivatives match).
    if not is_smooth_transition(formulas_df):
        sys.exit('At least, for an x between two consecutive rows, one of the formulas does not provide ' +
                 "a smooth transition (i.e.: f'(x) != g'(x))!")
    # Prompt user for the output file name for the SVG drawing.
    output_file = input('Enter the file name (including the extention) corresponding to the SVG ' +
                        'file to be created, containing the final drawing of the roller coaster: ')
    
    # Check if the file name has a .csv extension.
    if not output_file.lower().endswith('.svg'):
        sys.exit('The output file must be a SVG.')
    
    # Generate and save the roller coaster drawing.
    roller_coaster(formulas_df, output_file)

# Execute the main function to generate the roller coaster by getting user input, validating it, and creating an SVG drawing.
if __name__ == "__main__":
    generate_roller_coaster()
