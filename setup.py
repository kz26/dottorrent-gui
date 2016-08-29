from setuptools import setup, find_packages

setup(
    name="dottorrent-gui",
    version='1.0.0',
    packages=find_packages(),
    scripts=['bin/dottorrent_gui.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['dottorrent>=1.4.1', 'PyQt5>=5.7'],

    # metadata for upload to PyPI
    author="Kevin Zhang",
    author_email="kevin@kevinzhang.me",
    description="An advanced GUI torrent file creator with batch functionality, powered by PyQt and dottorrent",
    # long_description=open('README.rst').read(),
    keywords="bittorrent torrent",
    url="https://github.com/kz26/dottorrent-gui",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
