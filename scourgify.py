import os
import subprocess

# add to .bashrc or .bash_profile (gitbash):
# alias scourgify='python "...\styler\scourgify.py"'

# source: https://ascii.co.uk/art/wizard
ascii_banner = r"""
   (\.   .      ,/)
    \(   |\     )/
    //\  | \   /\      SCOURGIFY!
   (/ /\_#oo#_/\ \)
    \/\  ####  /\/
         `##'
"""
print(ascii_banner)


def get_pyscript_dir() -> str:
    """find where this script is located, for executing subprocess"""
    pyscript_dir = os.path.dirname(os.path.abspath(__file__))

    return pyscript_dir

scourgify_dir = get_pyscript_dir()
scourgify_path = os.path.join(scourgify_dir, "scourgify.py")

def execute_command(command, the_library):
    """where
    - check = if command fails (exits with a non-zero status code), raises CalledProcessError exception.
    which provides info about the command that failed, exit status, and any output.
    - text = ensures captured output and error streams return as strings.
    """

    print(f"\n~~~Scourgify {the_library}~~~")
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = result.communicate()
    if stdout:
        print(f"{the_library} stdout:\n{stdout}")
    if stderr:
        print(f"{the_library} stderr:\n{stderr}")

# if no such files, there's no need to use related functionality
dir_contains_py = any(filtered_files.get("python"))
print(f"dir_contains_py: {dir_contains_py}")

dir_contains_r = any(filtered_files.get("r"))
print(f"dir_contains_r: {dir_contains_r}")


def get_wanted_files_in_pwd():
    """these are files which can be formatted with black or styler."""

    extensions = {
    "python": [".py",],
    "r": [".R", ".Rmd",],
    }

    filtered_files = {
        "python": [],
        "r": [],
    }

    # determine which files exist in present working directory
    pwd = os.getcwd()
    print(f"pwd:  {pwd}")
    pwd_files = os.listdir(pwd)

    # if any wanted extensions found, return dict containing these filepaths
    for pwd_file in pwd_files:
        for lang, exts in extensions.items():  # python, .py
            for extension in exts:  # .r, .rmd
                if pwd_file.endswith(extension):
                    print(f"script found: {pwd_file}")
                    file_path = os.path.join(pwd, pwd_file)
                    filtered_files[lang].append({
                        "file_path": file_path,
                    })

    return filtered_files

filtered_files = get_wanted_files_in_pwd()

def check_pytest_tests_exist():
    """Determine if the present working directory contains a subdir called 'test', and if it contains 'test_*.py' files (for pytest)."""
    pwd = os.getcwd()
    test_path_py = os.path.join(pwd, "test")

    if os.path.exists(test_path_py) and os.path.isdir(test_path_py):
        test_files = os.listdir(test_path_py)
        for file in test_files:
            if file.startswith("test_") and file.endswith(".py"):
                print("subdir 'test' exists and contains test_*.py files.")
                return True

        print("No subdir 'test/' or no test_*.py file exist.")
    return False


def check_testthat_tests_exist():
    """Determine if the present working directory contains a subdir called 'tests', and if it contains 'test_*.r' files (for testthat)."""
    pwd = os.getcwd()
    test_path_r = os.path.join(pwd, "tests")

    if os.path.exists(test_path_r) and os.path.isdir(test_path_r):
        test_files = os.listdir(test_path_r)
        for file in test_files:
            if file.startswith("test_") and file.endswith(".r"):
                print("Subdir 'tests' exists and contains test_*.r files.")
                return True

        print("No subdir 'tests/' or no test_*.r files exist.")
    return False

testthat_tests_exist = check_testthat_tests_exist()
print(f"testthat_tests_exist: {testthat_tests_exist}")

def check_git_dir_exists():
    """this isnt so smart. if you run this on any code dir, what are chances it actually contains git? you may run on subdir"""
    pwd = os.getcwd()
    git_path = os.path.join(pwd, ".git")

    if os.path.exists(git_path) and os.path.isdir(git_path):
        return True
    else:
        return False

has_git_folder = check_git_dir_exists()
# print(has_git_folder)



if dir_contains_py:
    """
    Note on why this command outputs to stderr instead of stdout:
    By writing output to stderr, Black follows a common convention where tools generally print
    diagnostic or error messages to the standard error stream. This separation allows users to
    redirect the actual formatted code (stdout) to a file or a different process while still
    seeing any diagnostic messages (stderr) in the terminal or capturing them separately.
    """
    the_library = "black"
    command = ["black", "."]
    execute_command(command, the_library)

if dir_contains_r:
    # r styler reformatter on current dir
    the_library = "styler"
    formattr_dir = os.path.join(scourgify_dir, "formattr.R")
    command = ["Rscript", formattr_dir, "."]
    execute_command(command, the_library)

pytest_tests_exist = check_pytest_tests_exist()
print(f"pytest_tests_exist: {pytest_tests_exist}")
if pytest_tests_exist:
    # run pytest tests
    the_library = "pytest"
    command = ["pytest", "."]
    execute_command(command, the_library)

if testthat_tests_exist:
    # run testthat tests
    the_library = "testthat"
    command = ["Rscript", "-e", 'library(testthat); test_dir(".")']
    execute_command(command, the_library)

print("Scourgify complete")
