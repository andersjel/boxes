from setuptools import setup, find_packages

setup(
    name='boxes',
    version='0.1',
    description='Place boxes in a figure based on constraints.',
    url='http://github.com/andersjel/boxes',
    author='Anders Jellinggaard',
    author_email='anders.jel@gmail.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=True,
)
