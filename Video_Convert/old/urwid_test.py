import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),]

screen = urwid.raw_display.Screen()
screen.register_palette(palette)

'''
test 24-bit mode. show 256 kinds of color with RGB hex 0xe500xx. xx can be 00~ff
'''
attr_list = []
for i in range(256):
    if i <16:
        attr_list.append(urwid.AttrSpec('#e500'+'0'+hex(i)[-1], '#000000', 2**24))
    else:
        attr_list.append(urwid.AttrSpec('#e500'+hex(i)[2:], '#000000', 2**24))

txt_list = []
for i in range(16):
    for j in range(16):
        txt_list.append((attr_list[i*16+j], hex(i*16+j)))
    txt_list.append(('', '\n'))

txt = urwid.Text(txt_list)
fill = urwid.Filler(txt, 'top')
loop = urwid.MainLoop(fill, screen=screen, unhandled_input=exit_on_q)
loop.run()