from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


package_name = "dbtbt"
package_version = "0.0.1"
description = "Command-line tools to make deploying dbt models easier"

setup(
    name=package_name,
    version=package_version,
    author="Calogica, LLC",
    author_email="info@calogica.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # download_url
    # url="https://<>.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.sql', '*.yml', '*.md', '*.html'],
    },
    scripts=['bin/dbtbt'],
    python_requires='>=3.6',
    install_requires=[
        'colorama>=0.3.9',
        'PyYAML>=5.1',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
