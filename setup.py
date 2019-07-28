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


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='aiobook',
     version=get_version(),
     packages=setuptools.find_packages(),
     author="Valentyn Vaityshyn",
     author_email="valenook.ua@gmail.com",
     requires_python=">=3.6",
     description="Async framework for build messenger application in facebook",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Valenookua/aiobook",
     install_requires=get_requirements(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Development Status :: 2 - Pre-Alpha",
         "Operating System :: OS Independent",
         "Topic :: Software Development :: Libraries :: Application Frameworks",
     ],)

