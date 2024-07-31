from setuptools import setup, find_packages

setup(
   name='parallel_load',
   version='0.1.0',
   packages=find_packages(),
   install_requires=[],
   author='nigma',
   author_email='nigma.st@gmail.com',
   description='Библиотека позволяет загружать данные из ClickHouse и сохранять их в Parquet',
   url='https://github.com/nNigma/my_libos',
)
