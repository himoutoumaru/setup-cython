# cython-setup

* 能够把Python项目Cython化
* 使用PyInstaller打包Cython化的Python项目
* 使用StaticX把PyInstaller打包成一个独立的二进制包

# 使用方法

把`setup.py`拷贝到项目的根目录下，执行
```
python setup.py build
```
会在根目录下生成build文件夹，并且会生成对应的pyd/so文件。既可以加速Python执行的性能，又可以保护源码安全

会在根目录下生产dist文件夹，这个文件夹是PyInstaller打包后的软件包，可以直接打包拷贝走部署