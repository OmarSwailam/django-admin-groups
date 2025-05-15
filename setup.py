from setuptools import setup, find_packages

setup(
    name="django-admin-groups",
    version="1.0.0",
    description="Group Django admin models under custom sections.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Omar Swailam",
    author_email="you@example.com",
    url="https://github.com/OmarSwailam/django-admin-groups",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "Django>=3.2",
    ],
)
