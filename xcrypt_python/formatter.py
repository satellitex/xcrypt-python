import subprocess
import tempfile

def format_perl_code(code: str) -> str:
    """
    Formats Perl code using perltidy.
    
    :param code: The Perl source code to format.
    :return: The formatted Perl code.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pl") as temp_file:
        temp_file.write(code.encode("utf-8"))
        temp_file_name = temp_file.name
    
    try:
        # Run perltidy to format the code
        result = subprocess.run(["perltidy", "-b", temp_file_name], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error formatting Perl code:", result.stderr)
            return code
        
        # Read the formatted code from the backup file
        formatted_file_name = temp_file_name
        with open(formatted_file_name, "r", encoding="utf-8") as formatted_file:
            formatted_code = formatted_file.read()
        
        return formatted_code
    finally:
        # Clean up temporary files
        subprocess.run(["rm", "-f", temp_file_name, formatted_file_name])
        pass
