import os
import sys

from cx_Freeze import setup, Executable

base = 'WIN32GUI' if sys.platform == "win32" else None

executables = [Executable("src/BeeTodo.py", base=base)]

packages = ["PyQt5", "sqlite3", "configparser", "win32gui"]
include_files = [
    "css",
    "src/MyWidgets.py",
    "src/MyToDo.py",
    "src/service.py",
    "src/utils.py",
    "src/StyleSheets.py"
]
options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files
    },

}

# TCL_LIBRARY,TK_LIBRARY 的路径换成本地对应版本的路径。
os.environ['TCL_LIBRARY'] = os.environ['PYTHON_HOME']+r'\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = os.environ['PYTHON_HOME']+r'\tcl\tk8.6'
setup(
    name="BeeTodo",
    options=options,
    version="0.9",
    description='',
    executables=executables, requires=['cx_Freeze', 'PyQt5', 'win32gui']
)
