from setuptools import setup, find_packages

setup(
    name="crivo-cli",
    version="1.0.0",
    description="Crivo Thalam CLI - Device Management",
    author="Crivo Thalam",
    py_modules=["crivo_cli"],
    install_requires=[
        "requests>=2.31.0",
        "click>=8.1.7",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "crivo-thalam=crivo_cli:cli",
        ],
    },
    python_requires=">=3.7",
)
