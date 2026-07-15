from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

# Type hint : str means file_path should be a string.
# Return type ["numpy","pandas",]
def get_requirements(file_path: str) -> List[str]:
    """
    This function returns the list of required libraries.
    """  
    requirements = []
    
    try:
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.replace("\n","") for req in requirements]

            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
    
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirements       



setup(
    name="networksecurity_mlops",
    version="0.0.1",
    author="Mahfujur Rahman",
    author_email="rmahfuzur818@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)


"""
WHAT IS setup.py:
A packaging config file that turns this project folder into an installable 
Python package (same mechanism used for pandas, numpy, etc.)

WHY WE NEED IT:
So our own files can import from each other cleanly, from anywhere in the 
project — e.g. from networksecurity.exception.exception import CustomException
Without it, these internal imports break depending on which folder you run from.

HOW IT GETS TRIGGERED:
1. requirements.txt has "-e ." as its last line
2. Running `pip install -r requirements.txt` installs all normal packages,
   then hits "-e ." and automatically runs THIS setup.py file to install
   our own project as an editable, importable package
3. Proof: terminal shows "Running setup.py develop for <package_name>"
   during that install

KEY FUNCTIONS:
- setup(): registers the package (name, version, dependencies, which 
  folders belong to it) into Python's installed-packages list
- find_packages(): auto-scans the project and includes every folder 
  that has an __init__.py as a sub-package (so we don't list them manually)

get_requirements() removes "-e ." before passing the list to install_requires,
because "-e ." is a pip command flag, not a real package name — it belongs 
in requirements.txt, not inside setup.py's own dependency list.
"""


"""
pip install -r requirements.txt:
1. pip reads requirements.txt -> installs pandas/numpy/scikit-learn 
   directly, and sees "-e ." -> triggers setup.py
2. setup.py runs -> calls get_requirements("requirements.txt") which 
   reads the SAME file again, strips "-e ." (it's a pip flag, not a 
   package name), returns clean list to install_requires
3. setup() registers our project as an installable package using 
   find_packages() (auto-includes every folder with __init__.py)
4. pip merges its own list + setup.py's install_requires, dedupes, 
   installs each package once

Note: "-e ." triggers setup.py in step 1, BEFORE our code runs. 
Removing it in step 2 is too late to matter for the trigger — it only 
keeps it out of install_requires.
"""