from setuptools import setup

setup(
    name='ocs-led-daemon',
    version='1.0.0',
    description='Alarm-driven LED control daemon for SONiC - Molex OCS 68x68 Platform',
    license='Apache 2.0',
    author='SONiC OTN Team',
    author_email='lu.mao@molex.com',
    url='https://github.com/Azure/sonic-buildimage',
    maintainer='Lu Mao',
    maintainer_email='lu.mao@molex.com',
    packages=[],  # No Python packages, only scripts
    scripts=[
        'scripts/ocs-ledd',
    ],
    install_requires=[
        'sonic-py-common',
    ],
    setup_requires=[
        'wheel'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware',
    ],
    keywords='sonic SONiC LED daemon alarm molex ocs platform',
)
