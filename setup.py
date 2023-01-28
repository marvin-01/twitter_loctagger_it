from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(name='twitter_loctagger_it',
      version='0.0.1',
      description='map Italian Twitter users to a specific city or region in Italy',
      long_description=long_description,
	packages=['twitter_loctagger_it'],
      install_requires=['pandas'],
	license="MIT",
	author='Marvin Pappalettera',
	author_email='marvinpappalettera@yahoo.com',
      zip_safe=False)
