import setuptools
import re

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements


def get_version():
    with open('aiobook/__init__.py', 'r') as f:
        text = f.read()
        try:
            return re.findall(r"^__version__ = '([^']+)'\r?$", text, re.M)[0]
        except IndexError:
            raise RuntimeError('Unknown version.')


def get_requirements():
    install_reqs = parse_requirements(str('requirements.txt'), session='hack')
    return [str(ir.req) for ir in install_reqs]


setuptools.setup(
     name='aiobook',
     version=get_version(),
     packages=['aiobook'],
     author="Valentyn Vaityshyn",
     author_email="valenook.ua@gmail.com",
     requires_python=">=3.7",
     description="Async framework for build messenger application in facebook",
     url="https://github.com/Valenookua/aiobook",
     install_requires=get_requirements(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "Topic :: Software Development :: Libraries :: Application Frameworks",
     ],)

