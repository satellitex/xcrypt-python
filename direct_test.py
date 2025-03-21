import sys
import os

# Add the project root to the path
sys.path.insert(0, os.getcwd())

from xcrypt_python.visitors.base_visitor import BaseVisitor

# Create a simple subclass that implements _is_sample_or_standard_func
class TestVisitor(BaseVisitor):
    def _is_sample_or_standard_func(self, func_name):
        # Just use a simple string instead of an AST node to test
        if func_name in self.standard_functions:
            return f"{func_name} is a standard function"
        elif func_name in self.xcrypt_functions:
            return f"{func_name} is an xcrypt function" 
        else:
            return f"{func_name} is not recognized"

# Instantiate and test
visitor = TestVisitor()
print("Standard functions:", visitor.standard_functions)
print("Xcrypt functions:", visitor.xcrypt_functions)

# Test the recognition
print("\nTesting function recognition:")
for func in ['print', 'list', 'range', 'prepare', 'bulk', 'initialize', 'unknown_func']:
    result = visitor._is_sample_or_standard_func(func)
    print(f"- {result}")
