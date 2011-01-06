from distutils.core import setup
import py2exe, sys

sys.path.append('../')

setup(console=['../TinyHTTPProxy.py'])
