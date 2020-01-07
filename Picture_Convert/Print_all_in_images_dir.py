# -*- coding: utf-8 -*-
from skimage import io,transform,color

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
def img2char_pic_and_print(img_path,window_height=44):
    '''
    把指定图片转化成字符画
    Inputs:
        window_height:命令行窗口全屏时能显示的最多行数，默认情况下是48，可通过右键命令行窗口
                调节字体大小来改变该值
    '''
    gray=io.imread(img_path,as_gray=True)

    img_height=gray.shape[0]
    img_width=gray.shape[1]
    #依据图片的分辨率调增图像大小，由于命令行窗口行距为一个字符，故还要乘于2
    size=( window_height , int( img_width/img_height*window_height*2 ))
    gray=transform.resize(gray,size)

    char_pic=img2char_pic(gray)
    print(char_pic)
def print_all_picture_in_dir(window_height=44):
    '''
    从工作目录的images文件夹下读取所有图片转换输出
    Inputs:
        window_height:命令行窗口全屏时能显示的最多行数，默认情况下是48，可通过右键命令行窗口
                调节字体大小来改变该值
    '''
    coll=io.ImageCollection('images/*')
    for i in range(len(coll)):
        gray=color.rgb2gray(coll[i])

        img_height=gray.shape[0]
        img_width=gray.shape[1]
        #依据图片的分辨率调增图像大小，由于命令行窗口行距为一个字符，故还要乘于2
        size=( window_height , int( img_width/img_height*window_height*2) )
        gray=transform.resize(gray,size)

        char_pic=img2char_pic(gray)
        print('--------------------第%2d幅图--------------------'%(i+1))
        print(char_pic)

if __name__ == "__main__":
    print_all_picture_in_dir()