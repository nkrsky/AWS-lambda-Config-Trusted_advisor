# Shopping Cart

This is a simple shopping cart project that demonstrates how a shopping cart application might be implemented in Python.

## Requirements

- Python 3.x
- Poetry (dependency management tool)

## Setup

1. Clone the repository
   git clone https://github.com/kara-sky/shopping_cart

2. Install Poetry (if you haven't already)
   pip install poetry

3. Install dependencies and create a virtual environment
   poetry install


## Running the Application

1. Activate the virtual environment
   poetry shell

2. Run the main script
   python main.py


## Running the Tests

1. Activate the virtual environment
   poetry shell

2. Run the tests
   python -m unittest discover -s tests/ -p "test_*.py"


## Project Structure

The project is structured as follows:

- `models/` - contains the classes for the various objects used in the shopping cart application (e.g. `Product`, `Cart`, `Order`, `Payment`, `Customer`, `Store`, `Discount`)
- `tests/` - contains the unit tests for each class
- `main.py` - the entry point for the application
- `README.md` - this file

## Dependencies

This project depends on the following libraries:
- unittest

## Limitations
This is a simple example of a shopping cart, in a real-world scenario, you would have to integrate with the payment gateway and other external services, also you may want to handle  different exception, add more functionality and attributes to the classes, and so on.