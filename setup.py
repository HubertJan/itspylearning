from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='itspylearning',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version = '0.2.6',
    python_requires='>=3.8.2,',
    description='An itslearning api python library.',
    author='Hubert Jan Tomaszczak',
    license='MIT',
    url = 'https://github.com/HubertJan/itspylearning',
    download_url = 'https://github.com/HubertJan/itspylearning/archive/refs/tags/v0.2.3.tar.gz',
    install_requires=[
          'aiohttp>=3.6.3',
      ],
)


