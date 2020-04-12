import cv2
import numpy as np
import curses as cu
from curses import wrapper
import sys
import os
import random

g_char_set = " `'^*-+x<=oa!1|?0%$@#"
def convert_picture(img):
    '''
    input:
        img: ndarray (dtype=uint8), have RGB three channel
    output:
        char_img: str
    '''
    # 16-color table
    clr16 = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),\
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)]

    char_img = ''
    for i in range(img.shape[0]):
        line_char = ''
        line_clr = ''
        for j in range(img.shape[1]):
            # get the RGB component
            R, G, B = img[i][j]
            #RGB convert to gray
            gray = int(0.299*R + 0.587*G + 0.114*B)

            #find the nearest clr
            # delta_list = [(R-clr[0])**2 + (G-clr[0])**2 + (B-clr[0])**2 for clr in clr16]
            # clr_num = delta_list.index(min(delta_list))
            clr = (int(R/256*2)*255, int(G/256*2)*255, int(B/256*2)*255)
            clr_num = clr16.index(clr)
            line_clr += chr(32+clr_num) #add 32 so that it is a printable charater

            # get the character in g_char_set
            idx = int(gray/256*len(g_char_set))
            line_char += g_char_set[idx]
            
        char_img += line_char + line_clr + '\n'
    return char_img

def show_char_picture(win, char_img, size, color_mode=1):
    '''
    show character image in specific window
    '''
    
    win.clear()
    cnt = 0
    line_cnt = 0
    while line_cnt < size[1]:
        line_cnt += 1
        line_char = char_img[cnt: cnt+size[0]]
        line_clr = char_img[cnt+size[0]: cnt+2*size[0]]
        cnt += size[0]*2 + 1

        try:
            win.move(line_cnt-1, 0)
            col_cnt = 0
            while col_cnt < size[0]:
                char = line_char[col_cnt]
                clr_num = ord(line_clr[col_cnt])-32
                if color_mode==0:   # no color
                    win.addstr(char)
                else:               # 16-color (infact 8)
                    win.addstr(char, cu.color_pair(clr_num))
                col_cnt += 1
        except:
            pass
    win.refresh()

def mainloop(stdscr):
    cu.use_default_colors()
    cu.curs_set(0)

    # init color pair
    for i in range(1, 16): # 16 color
        cu.init_pair(i, i, -1)
    
    # get the screen size
    stdscr_y, stdscr_x = stdscr.getmaxyx()
    # create a sub window for show picture
    subwin = stdscr.subwin(stdscr_y - 2, stdscr_x, 1, 0)
    win_height, _ = subwin.getmaxyx()

    # get all picture path under img_root_path
    img_root_path = 'images/'
    img_name_list = os.listdir(img_root_path)

    # to save the converted picture. key: img_name, value: (char_img, size)
    saved_dic = {}
    # the index of image to show in img_name_list
    cur_img_index = 0
    # the color mode
    color_mode = 1
    # mainloop
    while True:
        img_name = img_name_list[cur_img_index]
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, '>>')
        stdscr.addstr('%s'%img_name, cu.color_pair(random.randint(1, 15)))
        stdscr.addstr('<<')
        stdscr.addstr(stdscr_y-1, 0, 'help: (P)rev, (N)ext, (C)olor, (Q)uit')
        stdscr.chgat(stdscr_y-1, 6, 3, cu.color_pair(random.randint(1, 15)))
        stdscr.chgat(stdscr_y-1, 14,3, cu.color_pair(random.randint(1, 15)))
        stdscr.chgat(stdscr_y-1, 22,3, cu.color_pair(random.randint(1, 15)))
        stdscr.chgat(stdscr_y-1, 31,3, cu.color_pair(random.randint(1, 15)))
        stdscr.move(0, 0)
        stdscr.refresh()

        try:
            if img_name in saved_dic: # have converted
                char_img, size = saved_dic[img_name]
            else:
                # read the image and convert
                img = cv2.imdecode(np.fromfile(os.path.join(img_root_path, img_name), dtype=np.uint8), 1)
                ori_height, ori_width, channel = img.shape
                size = (int(ori_width/ori_height*win_height*2), win_height)
                img = cv2.resize(img, size)
                char_img = convert_picture(img)
                # save
                saved_dic[img_name] = (char_img, size)
            # show
            show_char_picture(subwin, char_img, size, color_mode)
        except:
            subwin.clear()
            subwin.addstr("can't open this file, try to rename it in English")
            subwin.refresh()
        
        key = stdscr.getkey()
        if key in 'qQ':
            break
        elif key in 'cC':
            color_mode = 1 - color_mode # toggle
        elif key in 'pP':
            cur_img_index = max(0, cur_img_index-1)
        else:
            cur_img_index = min(len(img_name_list)-1, cur_img_index+1)
        
    # write saved_dic to file
    with open('.charater_images.txt', 'w') as fp:
        for img_name, (char_img, size) in saved_dic.items():
            fp.write(img_name+'\n')
            fp.write('size: %dx%d\n'%size)

            no_color_char_img = ''
            for i in range(size[1]):
                no_color_char_img += char_img[i*(2*size[0]+1):(2*i+1)*size[0]+i]+'\n'
            fp.write(no_color_char_img)
            fp.write('\n')

if __name__ == "__main__":
    wrapper(mainloop)