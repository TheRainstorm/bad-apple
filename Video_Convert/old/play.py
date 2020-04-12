import sys
import time
import threading as td
import os

def play(txt_path):
    with open(txt_path) as fp:
        total_frame = int(fp.readline().split(':')[1])
        FPS = int(fp.readline().split(':')[1])
        width, height = map(int, fp.readline().split(':')[1].split('x'))
        MINUTES, SECONDES = total_frame//FPS//60, (total_frame//FPS)%60

        td1.start()
        tic = time.time()
        cnt = 0
        while cnt < total_frame:
            cnt += 1
            line_num = int(fp.readline())

            frame = ''
            for i in range(height):
                frame += (fp.readline()[:width]+'\n')

            # os.system("cls")
            # show current time and total time (minutes:seconds)
            sys.stdout.write('%02d:%02d/%02d:%02d\n'%(cnt//FPS//60, (cnt//FPS)%60, MINUTES, SECONDES))
            sys.stdout.write(frame)
    
            toc = time.time()
            
            time.sleep(max(0, (cnt+1)/FPS - (toc - tic)))

def play_audio(video_path):
    os.system("ffplay -nodisp " + video_path + " >ffplay.log 2>&1")

if __name__ == "__main__":
    txt_path = 'RWBY-RedRose.char.color.txt'
    video_path = '../videos/'+txt_path.split('.')[0]+'.flv'

    td1 = td.Thread(target=play_audio, args=(video_path, ))

    play(txt_path)
    td1.join()