from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pyembedded',
    version='3.5',
    description='Python library to get data from embedded modules like RFID, GPS, GSM, Raspberry Pi',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abhinav Rawat',
    author_email='abhinavrawat92@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='embedded, rfid, gsm, gps, lcd, motor, raspberry pi',
    packages=find_packages(),
    install_requires=['pyserial']
)