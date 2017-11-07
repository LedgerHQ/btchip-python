#from distribute_setup import use_setuptools
#use_setuptools()

from setuptools import setup, find_packages
from os.path import dirname, join

here = dirname(__file__)
setup(
    name='btchip-python',
    version='0.1.23',
    author='BTChip',
    author_email='hello@ledger.fr',
    description='Python library to communicate with Ledger Nano dongle',
    long_description=open(join(here, 'README.md')).read(),
    url='https://github.com/LedgerHQ/btchip-python',
    packages=find_packages(),
    install_requires=['hidapi>=0.7.99'],
    extras_require = {
	'smartcard': [ 'python-pyscard>=1.6.12-4build1', 'ecdsa>=0.9' ]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
	'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
	'Operating System :: MacOS :: MacOS X'
    ]
)

