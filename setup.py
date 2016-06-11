from setuptools import setup

setup(
    name='quickgist',
    version='0.1.0',
    packages=['quickgist'],
    url='https://github.com/astocko/quickgist',
    license='MIT',
    author='Alexander Stocko',
    author_email='as@coder.gg',
    description='Command line tool for creating gists',
    entry_points={
        'console_scripts': [
            'quickgist = quickgist.quickgist:_quickgist']}
)
