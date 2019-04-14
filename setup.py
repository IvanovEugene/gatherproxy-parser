from setuptools import setup, find_packages


setup(
    name="gatherparser",
    version="0.0.1",
    packages=find_packages(exclude=['examples', 'tools']),
    package_dir={'gatherparser': 'gatherparser'},
    install_requires=['selenium==3.141.0',
                      'requests==2.21.0',
                      'beautifulsoup4==4.6.3'
                      ],
    author="Eugene Ivanov",
    author_email="erqups@gmail.com",
    description="This is a package that parse one of the largest sites "
                "with proxies - gatherproxy.com"
)
