import cv2
import curses as cu
from curses import wrapper
import sys

g_char_set = " `'^*-+x<=oa!1|?0%$@#"
def convert_picture(img):
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

def show_char_picture(stdscr):
    cu.start_color()
    cu.use_default_colors()
    cu.noecho()
    cu.cbreak()
    cu.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()

    # init color pair
    for i in range(1, 16): # 16 color
        cu.init_pair(i, i, -1)
    
    stdscr.addstr('hello\n')
    cnt = 0
    line_cnt = 0
    try:
        while line_cnt < size[1]:
            line_cnt += 1
            line_char = char_img[cnt: cnt+size[0]]
            line_clr = char_img[cnt+size[0]: cnt+2*size[0]]
            cnt += size[0]*2 + 1

            col_cnt = 0
            while col_cnt < size[0]:
                char = line_char[col_cnt]
                clr_num = ord(line_clr[col_cnt])-32
                stdscr.addstr(char, cu.color_pair(clr_num))
                col_cnt += 1
            stdscr.addstr('\n')
    except:
        pass
    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    picture_path = 'cap.png'
    window_height = 38
    
    img = cv2.imread(picture_path)
    ori_height, ori_width, channel = img.shape
    size = (int(ori_width/ori_height*window_height*2), window_height)
    img = cv2.resize(img, size)
    print(size)
    print(img.shape)

    # print(img.dtype)
    # print(img.shape)

    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    char_img = convert_picture(img)

    with open('test.txt', 'w') as fp:
        fp.write(char_img)
    wrapper(show_char_picture)