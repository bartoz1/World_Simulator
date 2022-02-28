import os
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
   name='worldsimulator',
   version='0.9',
   description='Simulator of the world in which there are plants and animals, including human with special ability.',
   author='RushKappa',
   author_email='bartoszzylwis@gmail.com',
   install_requires=required,
   package_data={'assets': ["*.png","*.ttf","*.otf","*.bmp"]},
   include_package_data=True,
   packages=find_packages(),
   
)