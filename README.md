# Roller Coaster Plotter

This project is a Python program that generates an SVG image of a roller coaster based on a sequence of formulas that describe its segments. The program takes input from a CSV file that defines each segment of the roller coaster and produces a smooth plot showing the entire coaster path.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Input File Format](#input-file-format)
  - [Running the Program](#running-the-program)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [License](#license)

## Project Overview

The Roller Coaster Plotter reads a CSV file containing mathematical formulas and boundaries, and checks that:
1. Each formula is valid and uses only the allowed variable (`x`).
2. The segments are continuous and connected smoothly.
3. All transitions between segments are differentiable, ensuring the roller coaster has smooth transitions.

If all checks are successful, the program generates an SVG file visualizing the roller coaster.

## Features
- **Formula Validation**: Ensures all formulas are valid and adhere to the required format.
- **Continuity Check**: Validates that each segment starts where the previous one ends.
- **Smooth Transition Check**: Verifies the derivative continuity between segments to ensure a smooth ride.
- **SVG Output**: Generates an SVG image of the roller coaster path.

## Installation

To run this project locally, you need Python 3.x installed. Clone the repository and install the required dependencies.

1. Clone the repository:
    ```sh
    git clone https://github.com/your_username/roller_coaster_plotter.git
    cd roller_coaster_plotter
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Input File Format

The input CSV file should have the following columns:
- `formula`: The mathematical formula for a segment (e.g., `x**2 + 1`, `cos(x)`).
- `start_x`: The starting value of `x` for the segment. This can be a number or an expression (e.g., `-2`, `pi + 3`).
- `end_x`: The ending value of `x` for the segment.

Example CSV file (`sample.csv`):
```csv
formula,start_x,end_x
x**2+1,-2,0
cos(x),0,3*pi
-1,3*pi,5*pi
cos(x),5*pi,7*pi
```

### Running the Program

To run the program, execute the following command:

```sh
python roller_coaster.py
```

The program will prompt you for:
1. The name of the input CSV file (e.g., `sample.csv`).
2. The name of the output SVG file to save the roller coaster plot (e.g., `output.svg`).

Make sure the CSV file is in the correct format, as described above.

## Testing

The project uses `pytest` for testing various functionalities of the code. The tests ensure that the input file is validated, the segments are connected properly, and transitions are smooth.

### Running Tests

To run the tests, ensure you have `pytest` installed:

```sh
pip install pytest
```

Then, run the tests:

```sh
python -m pytest
```

### Test Coverage

The following aspects of the program are tested:

1. **Input Validation**: Verifies that the input file has the correct format and required headers.
2. **Output Validation**: Checks if the output file has the correct `.svg` extension.
3. **Formula Validity**: Ensures that all formulas are valid mathematical expressions.
4. **Boundary Conditions**: Tests if segments properly match at their boundaries.
5. **Smooth Transition**: Validates smoothness by ensuring matching derivatives between segments.

These tests are located in `roller_coaster_test.py`.

## Dependencies

The following Python libraries are required:
- `pandas`: For handling CSV input files.
- `sympy`: For mathematical expression parsing and symbolic differentiation.
- `pytest`: For running unit tests.

To install these dependencies, run:

```sh
pip install -r requirements.txt
```

### Sample `requirements.txt`:
```
pandas
sympy
pytest
```

## License

Feel free to use, modify, and distribute this project as you wish.
