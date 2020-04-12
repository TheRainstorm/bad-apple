# -*- coding: utf-8 -*-
import time
import os
import invoke
from threading import Thread

import cv2

'''
API
'''
#gotoer=ctypes.cdll.LoadLibrary('goto.dll')
#gotoer=ctypes.CDLL('goto.dll')#[WinError 193] %1 不是有效的 Win32 应用程序。

pixel2char=list(" -:+=o108#%$")
length=len(pixel2char)
def img2char_pic(img):
    '''
    把一张灰度图片转化成字符画
    Inputs:
        img:注意,img为灰度图像且dtype为float64，最大值为1.0
    '''
    height,width=img.shape[0],img.shape[1]

    char_pic=''
    for row in range(height):
        for col in range(width):
            percent=img[row,col]
            #两种可行：
            #   int(x*(L-1))
            #   int(x*(L-1)+1/2)
            #index=int(percent*(length-1)+1/2)
            index=int(percent*(length-1))
            char_pic+=pixel2char[index]
            #char_pic+=' '
        char_pic+='\n'
    return char_pic

def video2txt_file(video_path,video_name,size):
    '''
    视频转化成字符画存在temp目录下，名称为{video_name}_xx_xx.txt文件中,xx分别为size[0](即height),size[1](即width)
    '''
    #读取视频
    cap=cv2.VideoCapture(video_path)
    #获得视频属性
    frames_num=cap.get(7)#cv2.CV_CAP_PROP_FRAME_COUNT
    FPS=cap.get(5)#CV_CAP_PROP_FPS Frame rate.

    pic_height,pic_width=size
    #txt文件路径
    txtfile_name='temp/'+video_name+'_'+str(pic_height)+'_'+str(pic_width)+'.txt'

    with open(txtfile_name,'w') as file:
        #把总帧数写在第一行
        file.write(str(int(frames_num))+'\n')
        #把帧率写在第二行
        file.write(str(int(FPS))+'\n')
        count=1
        while(True):
            # read返回值介绍：
            #    success,表示是否成功读取
            #    frame,一帧的图像，numpy数组
            success, frame = cap.read()
            if(success):
                # 把图像转化成灰度图,dtype=uint8,最大值为255
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 调整图像大小
                gray = cv2.resize(gray,(pic_width,pic_height))

                char_pic=img2char_pic(gray/255)
                file.write(char_pic)
                print(count,frames_num)
                count+=1
            else:
                break
        cap.release()
def play_audio(video_path):
    def call():
        invoke.run(f"mpv --no-video {video_path}", hide=True, warn=True)

    # 这里创建子线程来执行音乐播放指令，因为 invoke.run() 是一个阻塞的方法，要同时播放字符画和音乐的话，就要用多线程/进程。
    p = Thread(target=call)
    p.setDaemon(True)
    p.start()
def play_video(txt_file,size):
    """
    播放字符视频(仅图像)
    """
    height,width= size
    with open(txt_file) as file:
        #从文件第一行获得总帧数
        frame_num=int(file.readline().strip())
        #从第二行获得帧率
        FPS=int(file.readline().strip())
        for f in range(frame_num):
            char_pic=''
            for row in range(height):
                char_pic+=file.readline()
            print(char_pic)
            time.sleep(1 / FPS)  # 粗略地控制播放速度。
            #gotoer.gotoxy(0,0)#失败了
            #subprocess.call("cls",shell=True)  # 调用shell命令清屏，用 cmd 的话要把 "clear"改成 "cls"
def play(video_path,txt_file,size):
    play_audio(video_path)
    play_video(txt_file,size)

'''
调用API
'''
def play_one_auto(window_height=44):
    '''
    自动播放videos/will_play/目录下的一个视频（第一个）
        Inputs:窗口中用来显示字符画的行数，一般最大44行
    '''
    root='videos/will_play/'
    #寻找root目录下的视频文件
    video_name_with_exten=os.listdir(root)[0]
    #不存在视频，程序退出
    if(video_name_with_exten==''):
        print('videos/will_play/文件夹下不存在该视频文件，请检查视频是否已放入')
        return
    video_path=os.path.join(root,video_name_with_exten)
    video_name=os.path.splitext(video_name_with_exten)[0]

    #获得视频的分辨率信息
    cap=cv2.VideoCapture(video_path)
    #frame_height=cap.get(4)#CV_CAP_PROP_FRAME_HEIGHT
    #frame_width=cap.get(3)#CV_CAP_PROP_FRAME_WIDTH
    frame_size=(cap.get(4),cap.get(3))
    cap.release()
    #计算最合适的每帧图像转化成的字符画后的尺寸
    size=(window_height,int(window_height*frame_size[1]/frame_size[0]*2))

    #构造txt文件名
    txtfile_name=video_name+'_'+str(size[0])+'_'+str(size[1])+'.txt'
    txtfile_path=os.path.join('temp/',txtfile_name)

    #判断txt文件是否存在
    if(not os.path.exists(txtfile_path)):
        #不存在则创建文件，然后再播放
        print('没有缓存,开始生成txt')
        video2txt_file(video_path,video_name,size)

    #最后播放视频和音频
    play(video_path,txtfile_path,size)

if __name__ == "__main__":
    play_one_auto(window_height=44)
