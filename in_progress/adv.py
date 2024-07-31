# >>> # List Comprehensions

# Example: Create a dictionary with numbers and their squares
squares_dict = {x: x**2 for x in range(10)}
print(squares_dict)

# Example: Filter a dictionary based on a condition
filtered_dict = {k: v for k, v in squares_dict.items() if v % 2 == 0}   # Only keep even squares
print(filtered_dict)

# Example: Create a set of squares
squares_set = {x**2 for x in range(10)}
print(squares_set)

# Example: List comprehension with conditional logic
numbers = [1, 2, 3, 4, 5]
squared_evens = [x**2 for x in numbers if x % 2 == 0]  # Square of even numbers


# >>> # Lambda Functions

# Example: Define a lambda function to square a number
square = lambda x: x**2
print(square(5))  # Output: 25

# Example: Use a lambda function with the `map` function
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2, numbers))
print(squared_numbers)  # Output: [1, 4, 9, 16, 25]

# Example: Use a lambda function with the `filter` function
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # Output: [2, 4]

# Example: Use a lambda function with the `reduce` function
from functools import reduce
sum_numbers = reduce(lambda x, y: x + y, numbers)
print(sum_numbers)  # Output: 15

# >>> # Generators

# Example: Create a generator function to generate squares of numbers
def square_generator(n):
    for i in range(n):
        yield i**2

# Use the generator to get squares of numbers
squares = square_generator(5)
for num in squares:
    print(num)  # Output: 0, 1, 4, 9, 16

# Example: Generator expression
squares = (x**2 for x in range(5))
for num in squares:
    print(num)  # Output: 0, 1, 4, 9, 16

# >>> # Decorators

# Example: Define a decorator function
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

# Example: Apply the decorator to a function
@my_decorator
def say_hello():
    print("Hello!")

say_hello()

# Example: Decorator with arguments
def repeat(num_times):
    def decorator_repeat(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")

greet("Alice")

# Example: Class-based decorators
class DecoratorClass:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Something is happening before the function is called.")
        self.func(*args, **kwargs)
        print("Something is happening after the function is called.")

@DecoratorClass
def say_hi(name):
    print(f"Hi {name}")

say_hi("Bob")

# Example: Timing decorator
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    print("Function executed")

#slow_function()

# Example: Logging decorator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def log_execution(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Starting {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__}")
        return result
    return wrapper

@log_execution
def process_data(data):
    # Simulate data processing
    return [d * 2 for d in data]

# Using the decorated function
data = [1, 2, 3, 4, 5]
processed_data = process_data(data)
print('logging decorator', processed_data)








# >>> # Error Handling

# Example: Basic try-except block
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")

# Example: Handling multiple exceptions
try:
    result = 10 / 'a'
except ZeroDivisionError as e:
    print(f"Error: {e}")
except TypeError as e:
    print(f"Error: {e}")

# Example: Handling all exceptions
try:
    result = 10 / 0
except Exception as e:
    print(f"Error: {e}")

# Example: Using `else` block
try:
    result = 10 / 2
except ZeroDivisionError as e:
    print(f"Error: {e}")
else:
    print("No error occurred")

# Example: Using `finally` block
try:
    result = 10 / 2
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Execution completed")

# Example: Raising exceptions
def divide_numbers(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

try:
    result = divide_numbers(10, 0)
except ValueError as e:
    print(f"Error: {e}")

# >>> # Context Managers
"""
- Automatic Resource Management: Ensures resources are properly cleaned up.
- Error Handling: Simplifies error handling and cleanup code.
- Readability: Makes the code more readable and maintainable.
"""

# Example: Using `with` statement for file handling
with open('example.txt', 'w') as file:
    file.write("Hello, this is an example file.")

# Example: Creating a custom context manager
class CustomContextManager:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")

with CustomContextManager() as manager:
    print("Inside the context")

# Example: Using contextlib for context managers
from contextlib import contextmanager

@contextmanager
def custom_context():
    print("Entering the context")
    yield
    print("Exiting the context")

with custom_context():
    print("Inside the context")

# >>> # Threading and Multiprocessing

# Example: Using threading to run multiple tasks concurrently
import threading

def print_numbers():
    for i in range(5):
        print(f"Thread 1: {i}")

def print_letters():
    for letter in 'abcde':
        print(f"Thread 2: {letter}")

thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

thread1.start()
thread2.start()



# >>> # Unit Testing

# Example: Writing a simple unit test
import unittest

def add_numbers(a, b):
    return a + b

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)


# >>> # Packaging and Distribution

# Example: complex package structure with classes and functions

# mypackage/
# ├── mypackage/
# │   ├── __init__.py
# │   ├── module1.py
# │   ├── module2.py
# │   └── subpackage/
# │       ├── __init__.py
# │       ├── module3.py
# │       └── module4.py
# ├── README.md
# ├── LICENSE
# ├── setup.py
# └── requirements


# Example: Creating a distribution package

# Create a source distribution
# python setup.py sdist

# Create a wheel distribution
# python setup.py bdist_wheel

# Example: Installing a package from a distribution

# Install from source distribution
# pip install dist/mypackage-1.0.0.tar.gz

# Install from wheel distribution
# pip install dist/mypackage-1.0.0-py3-none-any.whl

# >>> # Type Hints
"""Type hints in Python are a way to indicate the expected data types of variables, 
function parameters, and return values. 
"""

# Example: Using type hints in function definitions
def greet(name: str) -> str:
    return f"Hello, {name}"

result = greet("Alice")
print(result)
"""
name: str indicates that the name parameter should be a string.
-> str indicates that the function returns a string.
"""

# Example: Type hints for lists
from typing import List

def process_numbers(numbers: List[int]) -> int:
    return sum(numbers)

result = process_numbers([1, 2, 3, 4])
print(result)

# Example: Type hints for dictionaries
from typing import Dict

def get_value(data: Dict[str, int], key: str) -> int:
    return data.get(key, 0)

result = get_value({'a': 1, 'b': 2}, 'b')
print(result)




# Example: Type hints for variables




