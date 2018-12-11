import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='prombzex',
    version='0.1',
    author='Chris Jones',
    author_email='cmsj@tenshu.net',
    description='Prometheus Bugzilla Exporter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cmsj/prombzex',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/prombzex'],
    zip_safe=False
)
