# Not only Bad-Apple

本文件夹下包含能将视频转换成字符画并播放的python程序。**可以做到音画同步。**

## 要求

- python 3.x
  - opencv-python
  - curses
- ffmpeg

## 使用
1. 在video_convert_multiprocess.py中指定:
   - video_path: 需要转换的视频路径
   - widow_height: 窗口能输出的最大行数，也为最终输出的字符画的一边分辨率。
   - have_color: 是否需要颜色
   - cvt_num: 转换程序的进程数，设置为电脑的最大进程数（超线程数）
2. 运行上面的程序，生成<video_name>.char.color.txt的文件
3. 在play_color.py中指定:
   - txt_path: 上面生成文件的路径
   - video_path: 同上（用于播放声音）

## 实现

