rem 使用cx_freeze进行exe可执行程序打包

rd /s /q build
rd /s /q dist

rem 调试编译
python setup.py build

rem 安装包发布编译
python setup.py bdist_msi