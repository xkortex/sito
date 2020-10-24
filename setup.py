from setuptools import find_packages, setup


pkgname = 'sito'
packages = find_packages()

deps_test = ['xdoctest']
deps_sci = ['numpy', 'pandas', 'sklearn']

deps_hashing = [
    'blake3',
    'wrapt',
]

deps = [
    'pydantic',
]

setup(
    name=pkgname,
    version='0.1.0',
    script_name='setup.py',
    python_requires='>3.6',
    zip_safe=True,
    packages=packages,
    install_requires=deps,
    extras_require={'hashing': deps_hashing, 'sci': deps_sci, 'test': deps_test},
)
