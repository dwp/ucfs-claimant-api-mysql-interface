"""setuptools packaging."""

import setuptools

setuptools.setup(
    name="ucfs_claimant_api_mysql_interface",
    version="0.0.1",
    author="DWP DataWorks",
    author_email="dataworks@digital.uc.dwp.gov.uk",
    description="Lambdas that query and manipulate multiple tables",
    long_description="Lambdas that query and manipulate multiple tables",
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["teardown=teardown:main"]},
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
