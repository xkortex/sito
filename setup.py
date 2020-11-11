from setuptools import setup, find_namespace_packages

"""
Note: I am currently trying and struggling to get package namespaces to 
work with setuptools_scm. However, I cannot seem to find the happy path that
setuptools_scm, pip, pip -e, and achieve the correct behavior. 
For now, sito-sci will be a separate namespace. 
"""
pkgname = 'sito'

deps = [
    'pydantic',
]

deps_test = ['xdoctest']

deps_hashing = [
    'blake3',
    'wrapt',
]

deps_sci = deps_hashing + ['numpy', 'pandas', 'sklearn']

deps_all = list(set(deps + deps_sci))

packages = find_namespace_packages(include=['sito'])
print(packages)

setup(
    name=pkgname,
    use_scm_version={
        'write_to': 'sito/_version.py',
        'write_to_template': '__version__ = "{version}"',
    },
    script_name='setup.py',
    python_requires='>3.6',
    zip_safe=True,
    setup_requires=['setuptools_scm'],
    install_requires=deps,
    extras_require={'hashing': deps_hashing, 'sci': deps_sci, 'test': deps_test, 'all': deps_all},
)
