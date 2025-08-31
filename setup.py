import sys
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    requirement_list = []
    with open('requirements.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            requirement = line.strip()
            if requirement and requirement!='-e .':
                requirement_list.append(requirement)

    return requirement_list


setup(
    name='Network Security',
    version = '0.0.1',
    author='Raghavendra Kumar',
    packages=find_packages(),
    install_requires=get_requirements()
)
