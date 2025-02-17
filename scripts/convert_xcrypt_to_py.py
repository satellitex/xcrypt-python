import os
import glob
import openai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def xcrypt_to_python(xcrypt_code: str) -> str:
    """
    Convert Xcrypt (Perl-based) code into Python using OpenAI's API.
    :param xcrypt_code: The Xcrypt source code as a string.
    :return: The equivalent Python code as a string.
    """
    prompt = f"""
    Convert the following Xcrypt (Perl-based) code into an equivalent Xcrypt-Python program. 
    Ensure that:
    - The output contains only valid Python code.
    - Use `from xcrypt_python.lib import Xcrypt` for imports.
    - Define a function with `@Xcrypt` that encapsulates the logic.
    - Convert Perl hashes (`%`) to Python dictionaries.
    - Convert Perl array (`@`) to Python lists.
    - Convert Perl function calls to Python equivalent calls.
    - Maintain logical equivalency and formatting.
    
    Xcrypt Code:
    {xcrypt_code}
    """
    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a translator that converts Perl-based Xcrypt code into Python."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def convert_xcrypt_files(input_dir: str, output_dir: str):
    """
    Convert all Xcrypt (.xcr) files from input_dir to Python equivalents in output_dir using OpenAI API.
    
    :param input_dir: Directory containing Xcrypt (.xcr) files.
    :param output_dir: Directory to save the converted Python files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    xcrypt_files = glob.glob(os.path.join(input_dir, "*.xcr"))
    
    for xcrypt_file in xcrypt_files:
        with open(xcrypt_file, "r", encoding="utf-8") as f:
            xcrypt_code = f.read()
        
        python_code = xcrypt_to_python(xcrypt_code)
        
        output_file = os.path.join(output_dir, os.path.basename(xcrypt_file).replace(".xcr", ".py"))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(python_code)
        
        print(f"Converted {xcrypt_file} -> {output_file}")

if __name__ == "__main__":
    input_directory = "sample/xcrypt"
    output_directory = "sample/xcryptpy"
    convert_xcrypt_files(input_directory, output_directory)
