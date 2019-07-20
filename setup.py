# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    python_requires='>3.6.0',
    name='tokencrypt',
    version='0.1.2',
    description='PKCS11 Keys classes for cryptography',
    long_description=long_description,
    url='https://github.com/rgammans/TokenCrypt',
    author='Roger Gammans',
    author_email='rgammans@gammascience.co.uk',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'Topic :: Utilities',
        'Topic :: Security',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        #Version of Python we know work.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='pkcs11 security cryptography',

    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'cryptography',
        'PyKCS11'
    ],
    extras_require={
        'dev': ['pipenv',''],
        'test': ['coverage'],
    },
    test_suite = 'tests',

)
