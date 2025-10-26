from setuptools import setup, find_packages

setup(
    name="crc-preproc",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "pillow",
        "opencv-python",
        "openslide-python",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "crc-preproc=crc_preproc.cli:main",
        ],
    },
)
