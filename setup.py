from io import open

from setuptools import find_packages, setup

with open('blacklist/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = [
    'Click',
    'pyreadline',
    'future',
]

setup(
    name='blacklist',
    version=version,
    description='A command line tool used to filter, update and delete leftovers from debugging, testing or autogenerating code.',
    long_description=readme,
    author='jaimevp54',
    author_email='jaimevp54@gmail.com',
    maintainer='jaimevp54',
    maintainer_email='jaimevp54@gmail.com',
    url='https://github.com/jaimevp54/blacklist',
    license='MIT/Apache-2.0',

    keywords=[
        'filter', 'command','line','clean'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    entry_points='''
        [console_scripts]
        blacklist=blacklist:cli
    ''',
    packages=find_packages(),
)
