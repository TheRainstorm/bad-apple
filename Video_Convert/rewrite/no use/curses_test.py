import curses as cu
from curses import wrapper

def main(stdscr):
    cu.start_color()
    cu.use_default_colors()
    cu.noecho()
    cu.cbreak()
    cu.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()

    print(cu.COLORS)
    print(cu.COLOR_PAIRS)

    clr_list = [cu.COLOR_BLACK, cu.COLOR_RED, cu.COLOR_GREEN, cu.COLOR_YELLOW, cu.COLOR_BLUE, cu.COLOR_MAGENTA, cu.COLOR_CYAN, cu.COLOR_WHITE]
    # for i in range(1, 8):
    #     cu.init_pair(i, clr_list[i], -1)
    for i in range(1, 16):
        cu.init_pair(i, i, -1)

    for i in range(16):
        stdscr.addstr(2*i, 0, "%2d hello world\n"%(i), cu.color_pair(i))
        stdscr.addstr(2*i+1, 0, "%2d hello world\n"%(i), cu.A_REVERSE|cu.color_pair(i))

    stdscr.refresh()
    stdscr.getkey()

    # the terminal need to set $TERM=xterm-256color or it will raise error
    for clr_byte in range(256):
        # divide one byte to 3, 3, 2 as the component of r, g, b
        br, bg, bb = (clr_byte&0xe0)>>5, (clr_byte&0x1c)>>2, clr_byte&0x03
        # map to 1000
        r, g, b = int(br/8*1000), int(bg/8*1000), int(bb/4*1000)

        cu.init_color(clr_byte, r, g, b)
    
    for i in range(1, 256):
        cu.init_pair(i, i, -1)
    for i in range(256):
        stdscr.addstr(str(i), cu.color_pair(i))
    
    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    wrapper(main)