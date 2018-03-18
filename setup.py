import os
import sys

from cx_Freeze import setup, Executable

base = 'WIN32GUI' if sys.platform == "win32" else None

executables = [Executable("src/main.py", base=base)]

packages = ["PyQt5", "sqlite3"]
include_files = [
    "css",
    "src/MyWidgets.py",
    "src/MyToDo.py",
    "src/controller.py",
    "src/utils.py",
    "src/StyleSheets.py",
]
options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files
    },

}
os.environ['TCL_LIBRARY'] = r'C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'
setup(
    name="prog",
    options=options,
    version="1.0",
    description='desc of program',
    executables=executables, requires=['cx_Freeze', 'PyQt5']
)
