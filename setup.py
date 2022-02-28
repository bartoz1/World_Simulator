import os
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
   name='world_simpulator_bartoz1',
   version='0.9',
   description='Simulator of the world in which there are plants and animals, including human with special ability.',
   author='RushKappa',
   author_email='bartoszzylwis@gmail.com',
   package_data={'':['save.txt']},
   install_requires=required,
   packages=find_packages(),
   
)