import ast
import unittest
from xcrypt_python.transformer import XcryptTransformer

# Test Python function definitions
PYTHON_CODE = """
def simple_function():
    print("This is a simple function")
    return "hello"

def function_with_args(arg1, arg2):
    result = arg1 + arg2
    print(f"Result: {result}")
    return result

def function_with_defaults(name, greeting="Hello"):
    message = f"{greeting}, {name}!"
    print(message)
    return message

def complex_function(a, b=10, c="test"):
    if a > b:
        print("a is greater than b")
    else:
        print("b is greater than or equal to a")
    
    for i in range(3):
        print(f"Iteration {i}: {c}")
    
    return a * b
"""

class TestFunctionConversion(unittest.TestCase):
    
    def setUp(self):
        self.transformer = XcryptTransformer()
    
    def test_simple_function(self):
        # Parse just the simple function
        tree = ast.parse("""
def simple_function():
    print("This is a simple function")
    return "hello"
""")
        result = self.transformer.transform(tree)
        self.assertIn("sub simple_function {", result)
        self.assertIn("print('This is a simple function');", result)
        self.assertIn("return 'hello';", result)
    
    def test_function_with_args(self):
        # Parse function with arguments
        tree = ast.parse("""
def function_with_args(arg1, arg2):
    result = arg1 + arg2
    print(f"Result: {result}")
    return result
""")
        result = self.transformer.transform(tree)
        self.assertIn("sub function_with_args {", result)
        self.assertIn("my ($arg1, $arg2) = @_;", result)
        self.assertIn("my $result = $arg1 + $arg2;", result)
        self.assertIn("return $result;", result)
    
    def test_function_with_defaults(self):
        # Parse function with default arguments
        tree = ast.parse("""
def function_with_defaults(name, greeting="Hello"):
    message = f"{greeting}, {name}!"
    print(message)
    return message
""")
        result = self.transformer.transform(tree)
        self.assertIn("sub function_with_defaults {", result)
        self.assertIn("my ($name, $greeting) = @_;", result)
        self.assertIn("$greeting = 'Hello' unless defined $greeting;", result)
    
    def test_complex_function(self):
        # Parse complex function with control flow
        tree = ast.parse("""
def complex_function(a, b=10, c="test"):
    if a > b:
        print("a is greater than b")
    else:
        print("b is greater than or equal to a")
    
    for i in range(3):
        print(f"Iteration {i}: {c}")
    
    return a * b
""")
        result = self.transformer.transform(tree)
        self.assertIn("sub complex_function {", result)
        self.assertIn("my ($a, $b, $c) = @_;", result)
        self.assertIn("$b = 10 unless defined $b;", result)
        self.assertIn("$c = 'test' unless defined $c;", result)
        self.assertIn("if ( ($a > $b) ) {", result)
        self.assertIn("} else {", result)
        self.assertIn("foreach my $i ([ 0..2 ]) {", result)
        self.assertIn("return $a * $b;", result)

if __name__ == "__main__":
    unittest.main()
