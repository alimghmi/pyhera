from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'pyhera',
  packages = ['pyhera'],
  version = '0.5',
  license='MIT',
  description = 'Hera is an optimized in-memory database',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Ali Moghimi',
  author_email = 'thisisjavid@gmail.com',
  url = 'https://github.com/lastill/pyhera',
  keywords = ['dbms', 'database', 'nosql', 'hera', 'heradb', 'pyhera'],
  classifiers=[
    'Development Status :: 4 - Beta',      # "3 - Alpha" | "4 - Beta" | "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License'
  ],
)
