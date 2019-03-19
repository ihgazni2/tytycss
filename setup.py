from setuptools import setup, find_packages
setup(
      name="tytycss",
      version = "0.5",
      description="search css file by selector-string/prelude-string",
      author="dapeli",
      url="https://github.com/ihgazni2/tytycss",
      author_email='terryinzaghi@163.com', 
      license="MIT",
      long_description = "refer to .md files in https://github.com/ihgazni2/tytycss",
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      packages= find_packages(),
      py_modules=['tytycss'], 
      )


# python3 setup.py bdist --formats=tar
# python3 setup.py sdist

