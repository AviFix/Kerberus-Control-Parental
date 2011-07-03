from distutils.core import setup
from glob import glob

import py2exe, sys

sys.path.append('../../../')
sys.path.append('../../../clases')
sys.path.append('../../../conf')

data_files = [("Microsoft.VC90.CRT", glob(r'../libs/x86_Microsoft.VC90.CRT/*.*'))]
setup(data_files=data_files, windows=['../../../cliente.py'],)
