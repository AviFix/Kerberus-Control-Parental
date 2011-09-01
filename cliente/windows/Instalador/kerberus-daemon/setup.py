from distutils.core import setup

import py2exe, sys

sys.path.append('../../../')
sys.path.append('../../../clases')
sys.path.append('../../../conf')
sys.path.append('../../../password')
setup(windows=['../../../cliente.py'],
      options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"],
            "includes":["sip"]
        }
    },
)
