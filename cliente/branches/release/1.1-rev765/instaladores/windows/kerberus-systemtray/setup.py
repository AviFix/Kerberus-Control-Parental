import sys
from cx_Freeze import setup, Executable

setup(
    name = "Kerberus System Tray",
    version = "1.1",
    description = "Kerberus Control Parental",
    executables = [Executable("../../../systemTray.py",
                            base = "Win32GUI",
                            targetName = "kerberusTray.exe")])
