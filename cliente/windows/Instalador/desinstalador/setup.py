from distutils.core import setup

import py2exe, sys

sys.path.append('../../../password')
sys.path.append('../../../clases')
sys.path.append('../../../conf')
sys.path.append('../../../')

setup(windows=['../../../password/uninstall.py'],
     options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"],
            "includes":["sip",]
        }
    },
)

