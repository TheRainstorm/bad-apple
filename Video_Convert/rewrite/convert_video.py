import cv2
import os

''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
g_char_set = r" `'^*-+x<=oa!1|?0%$@#"
def convert_frame(frame, size):
    # convert to gray, dtype=uint8,maxium=255
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # resize
    gray = cv2.resize(gray, tuple(size))

    gray = gray/256*len(g_char_set) #256 rather than 255, make it's maxium is L-1

    s = ''
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            s += g_char_set[int(gray[i][j])]
        s += '\n'
    return s

def convert(video_path, window_height):
    '''
    description:
        read video by cv2, extract every frame and write to a file in
        specific format.
        format:
            ----HEADER----
            total frame: xxx
            FPS: xxx
            WIDTH: xxx
            HEIGHT: xxx
            ---BODY----
            1
            frame
            2
            frame
            :
            .
            ------------
    input:
        video_path: str, the path of video
        window_height: int, the maxium line of terminal window
    '''
    _, video_fullname = os.path.split(video_path)
    video_name, ext = os.path.splitext(video_fullname)
    if ext not in [".mp4", ".flv"]:
        print("video format don't support")
        exit(-1)
    
    # open video
    cap=cv2.VideoCapture(video_path)
    # get attribute
    total_frame=cap.get(7)#cv2.CV_CAP_PROP_FRAME_COUNT
    FPS=cap.get(5)#CV_CAP_PROP_FPS Frame rate.
    ori_width, ori_height = cap.get(3), cap.get(4)
    size = (int(ori_width/ori_height*window_height*2), window_height)

    file_name = video_name + '.txt'

    with open(file_name,'w') as fp:
        fp.write('total frame:%d\n'\
            'FPS:%d\n'\
            'resolution:%dx%d\n'%(total_frame, FPS, size[0], size[1])
        )
        cnt = 0
        while cnt<total_frame:
            if cnt%100==0:
                print('\rprogress %d/%d'%(cnt, total_frame))
            cnt+=1
            try:
                success, frame = cap.read()
                fp.write(str(cnt)+'\n')
                fp.write(convert_frame(frame, size))
            except:
                break
        cap.release()

if __name__ == "__main__":
    convert('bad apple.mp4', 44)