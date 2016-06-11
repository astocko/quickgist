from setuptools import setup

setup(
    name='quickgist',
    version='0.1.2',
    packages=['quickgist'],
    url='https://github.com/astocko/quickgist',
    license='MIT',
    author='Alexander Stocko',
    author_email='as@coder.gg',
    description='Command line tool for creating gists',
    keywords=['gist', 'github'],
    entry_points={
        'console_scripts': [
            'quickgist = quickgist.quickgist:_quickgist']},
    install_requires=['orderedset >= 2.0', 'requests >= 2.10.0',
                      'six >= 1.10.0']
)
