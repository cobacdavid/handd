from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='handd',
    version='0.1',
    description='HAND-Drawn module for pycairo',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/cobacdavid/handd",
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    license='CC-BY-NC-SA',
    keywords=['hand-drawn',
              'pycairo',
              'realistic',
              'drawing'],
    packages=find_packages(),
    install_requires=["pycairo"],
    python_requires='>3.6'
)
