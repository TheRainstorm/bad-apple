import sys
import time

def play(txt_path):
    with open(txt_path) as fp:
        total_frame = int(fp.readline().split(':')[1])
        FPS = int(fp.readline().split(':')[1])
        width, height = map(int, fp.readline().split(':')[1].split('x'))

        cnt = 0
        while cnt < total_frame:
            cnt += 1

            line_num = int(fp.readline())
            frame = ''
            for i in range(height):
                frame += (fp.readline())
            
            sys.stdout.write(frame)
            time.sleep(1/FPS)

if __name__ == "__main__":
    play('bad apple.char.txt')
