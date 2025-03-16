from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path, 'r') as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        
        return requirements

setup(
    name='ds_project-1',
    version='0.1',
    author='Author Name',
    author_email='0MwJU@example.com',
    packages=find_packages(),
    # install_requires=[
    #     'numpy',
    #     'pandas',
    # ],
    install_requires=get_requirements('requirements.txt'),
)