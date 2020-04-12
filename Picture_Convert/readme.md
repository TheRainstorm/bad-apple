# 字符画转换(Picture to ASCII character)

此文件夹包含了在终端(terminal)运行的将图片转换为字符画的python程序

## 文件说明

- `gallery/`: 一些漂亮的截图
- `images/`: 将需要转换的图片放入这里
- `old/`: 包含过去的实现，无颜色，只需要scikit-image库即可
- `Terminal_Image_Reader.py`: 输出彩色字符画，可以来回切换图片

## 要求

Terminal_Image_Reader.py

```
python 3.x

numpy
opencv-python

curses
#python标准库，但不支持windows，需要手动安装
# 1. 在https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses下载和自己python版本一致的whl文件
#	 如python3.6则下载含cp36的版本。
# 2. pip install 下载的文件
```

## 使用
1. 打开终端：shift+鼠标右键，在当前位置打开power shell。或在文件管理器打开本目录，在地址栏中输入cmd回车。也会在当前位置打开终端。
2. 输入`python Terminal_Image_Reader.py`

## 其它说明
1. shift+右键默认会有打开power shell选项（windows10)，我们也可以自行添加在当前目录打开cmd选项，方法有许多，搜索“windows 当前目录打开cmd"

2. 代码会根据当前窗口大小来调节输出字符画的分辨率，一般全屏后窗口的最大行数为44，可以更改窗口的字体大小来获得更高的分辨率。调节方法，鼠标右键命令行窗口顶部边框，选择属性>字体>大小(一般默认为12)。