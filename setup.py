from setuptools import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

dependencies = [x for x in parse_requirements('requirements.txt', session=False)]

setup(
    name='dmcb',
    version='1.0',
    long_description='Dynamic Minecraft Banner',
    packages=['dmcb'],
    include_package_data=True,
    zip_safe=False,
    dependency_links=[str(dep.url) for dep in dependencies if not dep.url == None], # The packages from PyPI doesn't have links
    install_requires=[str(dep.req) for dep in dependencies]
)
