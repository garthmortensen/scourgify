import os
import subprocess


ascii_banner = fr"""
   (\.   .      ,/)
    \(   |\     )/
    //\  | \   /\      SCOURGIFY!
   (/ /\_#oo#_/\ \)    {os.getcwd()}
    \/\  ####  /\/
         `##'
"""
print(ascii_banner)


def get_pyscript_dir() -> str:
    """find where this script is located, for executing subprocess"""
    pyscript_dir = os.path.dirname(os.path.abspath(__file__))

    return pyscript_dir


def get_wanted_files_in_pwd():
    """these are files which can be formatted with black or styler."""

    extensions = {
        "python": [
            ".py",
        ],
        "r": [
            ".R",
            ".Rmd",
        ],
        "sql": [
            ".sql",
        ]
    }

    filtered_files = {
        "python": [],
        "r": [],
        "sql" : [],
    }

    # determine which files exist in present working directory
    pwd = os.getcwd()
    pwd_files = os.listdir(pwd)

    # flag to print if any scripts were found
    script_found = False

    # if any wanted extensions found, return dict containing these filepaths
    for pwd_file in pwd_files:
        for lang, exts in extensions.items():  # python, .py
            for extension in exts:  # .r, .rmd
                if pwd_file.endswith(extension):
                    if not script_found:  # print only once as section header
                        print(f"Relevant scripts found:")
                        script_found = True
                    print(f"- {pwd_file}")
                    file_path = os.path.join(pwd, pwd_file)
                    filtered_files[lang].append(
                        {
                            "file_path": file_path,
                        }
                    )

    return filtered_files


def check_pytest_dir_exist():
    """Determine if the present working directory contains a subdir called 'test', and if it contains 'test_*.py' files (for pytest)."""
    pwd = os.getcwd()
    test_path_py = os.path.join(pwd, "test")

    if os.path.exists(test_path_py) and os.path.isdir(test_path_py):
        test_files = os.listdir(test_path_py)
        for file in test_files:
            if file.startswith("test_") and file.endswith(".py"):
                # print("subdir 'test' exists and contains test_*.py files.")
                return True

        # print("No subdir 'test/' or no test_*.py file exist.")
    return False


def check_testthat_dir_exist():
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


def execute_command(command, the_library, capture_output=False):
    """where
    - check = if command fails (exits with a non-zero status code), raises CalledProcessError exception.
    which provides info about the command that failed, exit status, and any output.
    - text = ensures captured output and error streams return as strings.
    """

    print(f"\n~~~{the_library}~~~")
    try:
        result = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = result.communicate()
        if stdout:
            print(f"{the_library} stdout:\n{stdout}")
        if stderr:
            print(f"{the_library} stderr:\n{stderr}")
        
        if capture_output:
            return stdout, stderr
        else:
            return None, None

    except FileNotFoundError as e:
        # probably tied to missing git repo
        print(f"FileNotFoundError: {e}")
        if capture_output:
            return None, None
        else:
            return None, None


def check_for_uncommitted_scripts():
    """Per styler library authors, you should use version control or backup code.
    As such, check to see if any uncommitted .py or .r files exist.
    If so, do not run formatters.
    """

    uncommitted_scripts_dict = {
        "uncommitted_scripts": {
            "python": [],
            "r": [],
            "sql": [],
        },
        "no_git_repo_found": False,
    }

    # git porcelain produces fixed output for parsing. v1 is minimial
    the_library = "git status"
    command = ["git", "status", "--porcelain=1"]
    stdout, stderr = execute_command(command, the_library, capture_output=True)

    if stdout:
        # for joining fullpath to uncommited files
        pwd = os.getcwd()

        uncommitted_scripts = {
            "python": [],
            "r": [],
            "sql": [],
        }

        # ' M README.md\n M scourgify.py\n'
        stdout_lines = stdout.split("\n")
        script_found = False  # flag to print header only once

        for stdout_line in stdout_lines[
            :-1
        ]:  # trim out last line due to \n in stdout output
            git_file_status = stdout_line[:2].strip().lower()
            git_file_name = stdout_line[3:].strip().lower()

            # porcelain does not output commited files, but i dont have internet and i dont know what else might show up. #preinternetdays
            # TODO: does black format .ipynb?
            if git_file_name.endswith((".py",)):
                uncommitted_script_file_path = os.path.join(pwd, git_file_name)
                if not script_found:
                    print("Before running formatter, please commit scripts:")
                    script_found = True
                print(f"- file: {uncommitted_script_file_path}")
                # print(f"  status: {git_file_status}")
                uncommitted_scripts["python"].append(uncommitted_script_file_path)

            if git_file_name.endswith(
                (
                    ".r",
                    ".rmd",
                )
            ):
                uncommitted_script_file_path = os.path.join(pwd, git_file_name)
                if not script_found:
                    print("Before running formatter, please commit scripts:")
                    script_found = True
                print(f"- file: {uncommitted_script_file_path}")
                # print(f"  status: {git_file_status}")
                uncommitted_scripts["r"].append(uncommitted_script_file_path)

            if git_file_name.endswith((".sql",)):
                uncommitted_script_file_path = os.path.join(pwd, git_file_name)
                if not script_found:
                    print("Before running formatter, please commit scripts:")
                    script_found = True
                print(f"- file: {uncommitted_script_file_path}")
                # print(f"  status: {git_file_status}")
                uncommitted_scripts["sql"].append(uncommitted_script_file_path)


        uncommitted_scripts_dict["uncommitted_scripts"] = uncommitted_scripts

    if stderr:
        # error thrown from dir not being a git repo:
        # fatal: not a git repository (or any of the parent directories): .git
        if "not a git repository" in stderr:
            print("This directory is not version controlled with git.")
            uncommitted_scripts_dict["no_git_repo_found"] = True

    return uncommitted_scripts_dict


# def get_sql_dialect():
    """user must select the sql dialect"""

    # ordered by stackoverflow dev survey
    dialects = {
        1: "mysql",
        2: "postgres",
        3: "tsql (ms sql server)",
        4: "sqlite",
        5: "oracle",
    }

    print("select the script's sql dialect:")
    for num, dialect in dialects.items():
        print(f"{num}: {dialect}")

    # while True:
    #     try:
    # choice = int(input("Input the number: "))
    choice = 2
            # if choice in dialects:
    return dialects[choice]
        #     else:
        #         print("Enter a valid number (e.g. 3)")
        # except ValueError:
        #     print("Enter a valid number (e.g. 3)")

# create root for relative links ("./formattr.R")
scourgify_dir = get_pyscript_dir()
scourgify_path = os.path.join(scourgify_dir, "scourgify.py")

# if no .py/.r files, there's no need to run formatters
filtered_files = get_wanted_files_in_pwd()

dir_contains_py = any(filtered_files.get("python"))
# print(f"dir_contains_py: {dir_contains_py}")

dir_contains_r = any(filtered_files.get("r"))

dir_contains_sql = any(filtered_files.get("sql"))

# before formatting, all code should be committed
uncommitted_scripts_dict = check_for_uncommitted_scripts()

def process_uncommitted_scripts(uncommitted_scripts_dict):
    no_git_repo_found = uncommitted_scripts_dict["no_git_repo_found"]
    uncommitted_scripts_python = bool(uncommitted_scripts_dict["uncommitted_scripts"]["python"])
    uncommitted_scripts_r = bool(uncommitted_scripts_dict["uncommitted_scripts"]["r"])
    uncommitted_scripts_sql = bool(uncommitted_scripts_dict["uncommitted_scripts"]["sql"])
    
    return no_git_repo_found, uncommitted_scripts_python, uncommitted_scripts_r, uncommitted_scripts_sql

no_git_repo_found, uncommitted_scripts_python, uncommitted_scripts_r, uncommitted_scripts_sql = process_uncommitted_scripts(uncommitted_scripts_dict)

if not dir_contains_py:
    print("This directory contains no python to format")

if not dir_contains_r:
    print("This directory contains no r to format")

if not dir_contains_sql:
    print("This directory contains no sql to format")

if dir_contains_py and not uncommitted_scripts_python:
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

if dir_contains_r and not uncommitted_scripts_r:
    # r styler reformatter on current dir
    the_library = "styler"
    formattr_dir = os.path.join(scourgify_dir, "formattr.R")
    command = ["Rscript", formattr_dir, "."]
    execute_command(command, the_library)

# if dir_contains_sql and not uncommitted_scripts_sql:
#     # NOTE: this is setup to run one dialect fix on all .sql files in dir. You cannot specify dialect per file
#     the_library = "sqlfluff"
#     print(the_library)

#     # user must specify which dialect to format with, unfortuantely
#     selected_dialect = get_sql_dialect()
#     print(f"Selected: {selected_dialect}\n")

#     # check which sql files are in dir
#     sql_files = filtered_files["sql"]
#     for sql_file in sql_files:
#         # sqlfluff fix --dialect=postgres '/.../eeeeee.sql'
#         command = ["sqlfluff", "fix", f"--dialect={selected_dialect}", f"{sql_file['file_path']}"]  # need to drill down to key
#         execute_command(command, the_library)

# avoid unwanted terminal output by first checking if pytest files exist
pytest_tests_exist = check_pytest_dir_exist()
if pytest_tests_exist:
    # run pytest tests
    print("subdir './test/' exists and contains test_*.py files.")
    the_library = "pytest"
    command = ["pytest", "."]
    execute_command(command, the_library)
else: print("this directory contains no ./test/ to run pytest on.")

# avoid unwanted terminal output by first checking if testthat files exist
testthat_dir_exist = check_testthat_dir_exist()
if testthat_dir_exist:
    # run testthat tests
    # TODO: test this functionality
    print("subdir './tests/' exists and contains test_*.r files.")
    the_library = "testthat"
    command = ["Rscript", "-e", 'library(testthat); test_dir(".")']
    execute_command(command, the_library)
else: print("this directory contains no ./tests/ to run testthat on.")

print("\n\n~~~Scourgify complete~~~")
