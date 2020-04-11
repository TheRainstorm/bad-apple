import curses as cu
from curses import wrapper
import sys
import os
import time
from multiprocessing import Process, Queue, Pipe, Lock
import json

def play(win, have_color=True):
    # win.getch() don't block
    win.nodelay(1)

    total_frame, FPS, width, height = pipe_recv.recv()
    # the FPS get from flv is not correct,  the difference between 29 and 30
    # can result in a big influence
    FPS = 30
    # video's length (minutes:seconds)
    MINUTES, SECONDES = total_frame//FPS//60, (total_frame//FPS)%60

    # start play audio
    p_play_audio.start()
    # without this 
    time.sleep(0.3)
    # start record time
    tic = time.time()

    r1 = {}
    r2 = {}
    cnt = 0
    while cnt < total_frame:
        cnt += 1

        win.clear()
        # show current time and total time
        win.addstr('%02d:%02d/%02d:%02d\n'%(cnt//FPS//60, (cnt//FPS)%60, MINUTES, SECONDES))

        frame_num, frame = frame_queue.get()

        toc = time.time()
        # jump the frame
        r1[cnt] = (toc-tic)
        if cnt != int((toc - tic)*FPS)+1:
            continue
        # print one frame
        line_cnt = 0
        while line_cnt < height:
            line_cnt += 1
            line = frame[line_cnt*(width*2+1): (line_cnt+1)*(width*2+1)]
            line_char = line[:width]
            line_clr = line[width:-1]

            try:
                if have_color: # print every char
                    col_cnt = 0
                    while col_cnt < width:
                        char = line_char[col_cnt]
                        clr_num = ord(line_clr[col_cnt])-32
                        win.addstr(char, cu.color_pair(clr_num))
                        col_cnt += 1
                    win.addstr('\n')
                else: #print one line
                    win.addstr(line_char+'\n')
            except: # addstr overflow the window
                pass
        win.refresh()
        # print one frame finish

        # 花里胡哨的退出方法
        ch = win.getch()
        if ch==ord('q'):
            # 首先，获取lock，让read_file进程自己退出
            lock.acquire()
            # 然后将frame_queue清空，read_file才能真正退出
            while frame_queue.get() is not None:
                pass
            exit(0)
        
        toc = time.time()
        r2[cnt] = (toc - tic)
        delta = cnt/FPS - (toc - tic)
        time.sleep(max(0, delta))
    
    with open('record.json', 'w') as fp:
        json.dump({'r1':r1, 'r2':r2}, fp)

def read_file(txt_path, frame_queue, pipe_send, lock):
    with open(txt_path) as fp:
        # read header
        total_frame = int(fp.readline().split(':')[1])
        FPS = int(fp.readline().split(':')[1])
        width, height = map(int, fp.readline().split(':')[1].split('x'))

        pipe_send.send([total_frame, FPS, width, height])
        cnt = 0
        while cnt < total_frame:
            cnt += 1
            line_num = int(fp.readline())

            frame = ''
            line_cnt = 0
            while line_cnt < height:
                line_cnt += 1

                frame += fp.readline()
            
            frame_queue.put((line_num, frame))
            # 发现锁没了，自己退出
            if not lock.acquire(block=False):
                frame_queue.put(None)
                exit(0)
            else:
                lock.release()
    
def mainloop(stdscr):
    cu.use_default_colors()
    cu.nocbreak()
    cu.curs_set(0)

    # init color pair
    for i in range(1, 16): # 16 color
        cu.init_pair(i, i, -1)
    
    stdscr_y, stdscr_x = stdscr.getmaxyx()

    # make a subwindow, leave one line to show video name
    subwin = stdscr.subwin(stdscr_y - 2, stdscr_x - 2, 1, 0)

    stdscr.addstr(0, 0, os.path.split(video_path)[1])
    stdscr.refresh()

    play(subwin, have_color)

def play_audio(video_path):
    os.system("ffplay -nodisp \"%s\" >ffplay.log 2>&1"%video_path)

if __name__ == "__main__":
    # txt_path = 'bad apple.char.color.txt'
    # video_path = '../videos/'+txt_path.split('.')[0]+'.mp4'
    txt_path = 'RWBY-RedRose.char.color.txt'
    video_path = '../videos/'+txt_path.split('.')[0]+'.flv'

    have_color = True
    if len(sys.argv)==2:
        if sys.argv[1]=='0':
            have_color = False
    
    # multiprocess
    frame_queue = Queue(10)
    pipe_send, pipe_recv = Pipe()
    lock = Lock() # when read_file process can't acquire the lock, it exit

    p_play_audio = Process(target=play_audio, args=(video_path, ))
    p_read_file = Process(target=read_file, args=(txt_path, frame_queue, pipe_send, lock))

    p_read_file.start()
    wrapper(mainloop)
    p_read_file.join()
    # p_play_audio.join()