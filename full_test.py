import ast
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.getcwd())

from xcrypt_python.visitors.expression_visitor import ExpressionVisitor
from xcrypt_python.transformer import XcryptTransformer

# Create a simple Python code with function calls
TEST_CODE = """
def test_function():
    # Standard functions
    print("Hello")
    push(my_list, 10)
    
    # Xcrypt functions
    list(range(5))
    prepare(template)
    bulk(jobs)
    initialize()
    
    # Other/unknown functions
    unknown_func()
"""

# Parse the code
tree = ast.parse(TEST_CODE)

# Create a transformer to convert the code
transformer = XcryptTransformer()
result = transformer.transform(tree)

print("Conversion result:")
print(result)
print("\nThis should show 'list' and 'range' as standard functions in the output.")
print("Functions like 'prepare', 'bulk', 'initialize' should also be recognized.")
print("'unknown_func' should be handled differently than the standard and Xcrypt functions.")
