from setuptools import setup, find_packages

setup(
    name='mfindia',
    version='1.0.0',
    url='https://github.com/anaghkanungo7/mfindia',
    author='Anagh Kanungo',
    author_email='anaghkanungo7@gmail.com',
    description='Mutual Funds India Price Data',
    packages=find_packages(),    
    install_requires=["bs4", "pandas", "requests", "sqlalchemy"],
)
