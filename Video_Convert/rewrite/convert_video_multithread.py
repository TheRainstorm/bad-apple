import cv2
import os
from queue import Queue
from threading import Thread

def read_video(frame_queue): #producer
    while True:
        success, frame = cap.read()
        if success:
            # convert to gray, dtype=uint8,maxium=255
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # resize
            gray = cv2.resize(gray, tuple(size))
            gray = gray/256*len(g_char_set) #256 rather than 255, make it's maxium is L-1
            
            frame_queue.put(gray)
        else:
            break
    cap.release()

''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
g_char_set = r" `'^*-+x<=oa!1|?0%$@#"
def convert_frame(frame_queue, cvt_frame_queue):
    while True:
        gray = frame_queue.get()
        if gray is None:
            break

        cvt_frame = ''
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                cvt_frame += g_char_set[int(gray[i][j])]
            cvt_frame += '\n'

        cvt_frame_queue.put(cvt_frame)

def write_file(cvt_frame_queue, ):
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
            fp.write(str(cnt)+'\n')

            cvt_frame = cvt_frame_queue.get()
            fp.write(cvt_frame)

if __name__ == "__main__":
    video_path = 'bad apple.mp4'
    window_height = 44

    _, video_fullname = os.path.split(video_path)
    video_name, ext = os.path.splitext(video_fullname)
    if ext not in [".mp4", ".flv"]:
        print("video format don't support")
        exit(-1)
    file_name = video_name + '.txt'
    
    # open video
    cap=cv2.VideoCapture(video_path)
    # get attribute
    total_frame=cap.get(7)#cv2.CV_CAP_PROP_FRAME_COUNT
    FPS=cap.get(5)#CV_CAP_PROP_FPS Frame rate.
    ori_width, ori_height = cap.get(3), cap.get(4)
    size = (int(ori_width/ori_height*window_height*2), window_height)

    '''cvt_num
    '''
    cvt_num = 4
    frame_queue = Queue(cvt_num*2)
    cvt_frame_queue  = Queue(cvt_num*2)

    worker_list = []
    p1 = Thread(target=read_video, args=(frame_queue, ))
    for i in range(cvt_num):
        pc = Thread(target=convert_frame, args=(frame_queue, cvt_frame_queue))
        worker_list.append(pc)
        pc.start()
    c1 = Thread(target=write_file, args=(cvt_frame_queue, ))

    p1.start()
    c1.start()

    p1.join()
    for i in range(cvt_num):
        frame_queue.put(None)
    for i in range(cvt_num):
        worker_list[i].join()
    c1.join()