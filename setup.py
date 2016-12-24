from setuptools import setup


VERSION='0.1.0.alpha-1'


setup(
name='wood',
version=VERSION,
license='http://www.apache.org/licenses/LICENSE-2.0',
description='A faster way to build web app by tornado',
author='thislight',
url='https://github.com/thislight/wood',
install_requires=['tornado'],
classifiers=[
'License :: OSI Approved :: Apache Software License',
],
packages=['wood']
)

