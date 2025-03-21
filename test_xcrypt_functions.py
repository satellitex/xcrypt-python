from xcrypt_python.visitors.expression_visitor import ExpressionVisitor

visitor = ExpressionVisitor()
print("Standard functions:", visitor.standard_functions)
print("Xcrypt functions:", visitor.xcrypt_functions)
print("Type of standard_functions:", type(visitor.standard_functions))
print("Type of xcrypt_functions:", type(visitor.xcrypt_functions)) 
print("Length of standard_functions:", len(visitor.standard_functions))
print("Length of xcrypt_functions:", len(visitor.xcrypt_functions))
print("'print' in standard_functions:", 'print' in visitor.standard_functions)
print("'list' in xcrypt_functions:", 'list' in visitor.xcrypt_functions)

# Check if a function would be recognized as a standard or xcrypt function
def check_function(name):
    # Mock AST node with an id attribute
    class MockNode:
        def __init__(self, id_value):
            self.id = id_value
    
    node = MockNode(name)
    # Check if it's in either list
    in_standard = name in visitor.standard_functions
    in_xcrypt = name in visitor.xcrypt_functions
    # Call the function directly
    is_recognized = visitor._is_sample_or_standard_func(node)
    print(f"Function '{name}': in standard={in_standard}, in xcrypt={in_xcrypt}, recognized by method={is_recognized}")

# Also print the implementation of _is_sample_or_standard_func for debugging
import inspect
print("\nThe _is_sample_or_standard_func method implementation:")
print(inspect.getsource(visitor._is_sample_or_standard_func))

# Test with some functions from our lists
for func in ['print', 'list', 'range', 'prepare', 'bulk', 'initialize']:
    check_function(func)
