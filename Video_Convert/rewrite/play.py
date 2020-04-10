import sys
import time
import curses as cu
from curses import wrapper
import threading as td
import os

def play(txt_path):
    with open(txt_path) as fp:
        total_frame = int(fp.readline().split(':')[1])
        FPS = int(fp.readline().split(':')[1])
        width, height = map(int, fp.readline().split(':')[1].split('x'))

        # print(total_frame, FPS, width, height)
        cnt = 0
        while cnt < total_frame:
            cnt += 1
            line_num = fp.readline()
            if not have_color: # no color
                frame = ''
                for i in range(height):
                    frame += (fp.readline()[:width]+'\n')
                sys.stdout.write(frame)
                time.sleep(1/FPS)
    
def play2(stdscr, txt_path):
    cu.start_color()
    cu.use_default_colors()
    cu.noecho()
    cu.cbreak()
    cu.curs_set(0)
    stdscr.keypad(True)

    # init color pair
    for i in range(1, 16): # 16 color
        cu.init_pair(i, i, -1)
    
    with open(txt_path) as fp:
        total_frame = int(fp.readline().split(':')[1])
        FPS = int(fp.readline().split(':')[1])
        width, height = map(int, fp.readline().split(':')[1].split('x'))

        # print(total_frame, FPS, width, height)
        cnt = 0
        while cnt < total_frame:
            cnt += 1
            line_num = fp.readline()

            stdscr.clear()
            stdscr.addstr(str(cnt)+', '+line_num+', '+str(total_frame)+'\n')
            # cu.setsyx(0, 0)
            line_cnt = 0
            while line_cnt < height:
                line_cnt += 1
                line = fp.readline()
                line_char = line[:width]
                line_clr = line[width:-1]

                col_cnt = 0
                while col_cnt < width:
                    char = line_char[col_cnt]
                    clr_num = ord(line_clr[col_cnt])-32
                    stdscr.addstr(char, cu.color_pair(clr_num))
                    col_cnt += 1
                stdscr.addstr('\n')
            stdscr.refresh()
            time.sleep(1/FPS)

def play_audio(video_path):
    os.system("ffplay -nodisp " + video_path + " >ffplay.log 2>&1")

if __name__ == "__main__":
    txt_path = 'RWBY-RedRose.char.color.txt'
    have_color = True

    video_path = txt_path.split('.')[0]+'.flv'
    td1 = td.Thread(target=play_audio, args=(video_path, ))
    td1.start()
    if have_color:
        wrapper(play2, txt_path)
    else:
        play(txt_path)
    td1.join()
