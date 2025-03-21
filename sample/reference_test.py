def modify_scalar(value):
    """
    Modifies a scalar value (should be passed by reference in Perl)
    """
    value = value + 10
    return value

def modify_list(items):
    """
    Modifies a list (should be passed by reference in Perl)
    """
    items.append(100)
    return items

def modify_dict(data):
    """
    Modifies a dictionary (should be passed by reference in Perl)
    """
    data["new_key"] = "added value"
    return data

def process_all(scalar, my_list, my_dict):
    """
    Processes all types of data
    """
    # Modify each parameter
    scalar = modify_scalar(scalar)
    my_list = modify_list(my_list)
    my_dict = modify_dict(my_dict)
    
    # Access the modified values
    print(f"Modified scalar: {scalar}")
    print(f"Modified list: {my_list}")
    print(f"Modified dict: {my_dict}")
    
    return scalar, my_list, my_dict

# Main code
x = 5
my_array = [1, 2, 3]
my_hash = {"a": 1, "b": 2}

# This should pass all arguments by reference in Perl
result = process_all(x, my_array, my_hash)
print(f"Final result: {result}")

# Direct array access
print(f"Direct array access: {my_array[0]}")

# Direct hash access
print(f"Direct hash access: {my_hash['a']}")
