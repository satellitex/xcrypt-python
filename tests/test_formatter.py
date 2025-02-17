from xcrypt_python.formatter import format_perl_code

# Example usage
def test_format_perl_code():
    sample_perl_code = """
use strict;
use warnings;
my $x = 10; my $y=20; print $x+$y;
"""
    formatted_code = format_perl_code(sample_perl_code)
    print(formatted_code)
    expected_code = """
use strict;
use warnings;
my $x = 10;
my $y = 20;
print $x+ $y;
"""
    print(expected_code)
    assert formatted_code == expected_code, "Code formatting did not work as expected"
    
