from setuptools import setup, find_namespace_packages, find_packages

pkgname = 'sito2'

deps_test = ['xdoctest']

deps = [
    'sito',
    'blake3',
    'numpy',
    'pandas',
    'pydantic',
    'sklearn',
]


packages = find_packages(include=['sito2'])
print(packages)

setup(
    name=pkgname,
    packages=packages,
    use_scm_version=True,
    script_name='setup.py',
    python_requires='>3.6',
    zip_safe=True,
    setup_requires=['setuptools_scm'],
    install_requires=deps,
    extras_require={'test': deps_test},
)
