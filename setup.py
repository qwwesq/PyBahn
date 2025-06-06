from setuptools import setup, find_packages

setup(
    name='pybahn',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    author='qwwesq',
    author_email='qwwesq.dev@gmail.com',
    description='A Python library for interacting with Deutsche Bahn data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
