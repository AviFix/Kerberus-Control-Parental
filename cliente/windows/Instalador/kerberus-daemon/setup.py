from distutils.core import setup

import py2exe, sys

sys.path.append('../../../')
sys.path.append('../../../clases')
sys.path.append('../../../conf')

setup(windows=['../../../cliente.py'],)
