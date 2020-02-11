from setuptools import setup
import os

with open('requirements.txt', 'rb') as f:
    install_requires = f.read().decode('utf-8').split('\n')

setup(
    name='localVariableManager',
    version=1.0,
    description="CLI tool to manage local key/certs and token.",
    author='Sid Premkumar',
    author_email='sid.premkumar@gmail.com',
    url='https://sidpremkumar.com',
    license='MIT',
    install_requires=install_requires,
    packages=[
        'localVariableManager',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "lvm=localVariableManager.main:main",
        ],
    },
)