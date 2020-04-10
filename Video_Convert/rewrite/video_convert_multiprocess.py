import cv2
import os
from multiprocessing import Process, Queue, Pipe
import heapq

def read_video(frame_queue, video_path, window_height, pipe_send): #producer
    _, video_fullname = os.path.split(video_path)
    video_name, ext = os.path.splitext(video_fullname)
    if ext not in [".mp4", ".flv"]:
        print("video format don't support")
        exit(-1)

    # open video
    cap=cv2.VideoCapture(video_path)
    # get attribute
    total_frame=cap.get(7) #cv2.CV_CAP_PROP_FRAME_COUNT
    # total_frame=1 #cv2.CV_CAP_PROP_FRAME_COUNT
    FPS=cap.get(5)#CV_CAP_PROP_FPS Frame rate.
    ori_width, ori_height = cap.get(3), cap.get(4)
    size = (int(ori_width/ori_height*window_height*2), window_height)
    
    '''pipe send
    '''
    pipe_send.send([video_name, total_frame, FPS, size]) #send to write file process

    cnt = 0
    while cnt < total_frame:
        cnt += 1
        success, frame = cap.read()
        if success:
            '''put to frame queue
            '''
            frame = cv2.resize(frame, size)
            frame_queue.put((cnt, frame))
        else:
            break
    cap.release()

def convert_frame(frame_queue, cvt_frame_queue):
    ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
    char_set = r" `'^*-+x<=oa!1|?0%$@#"
    while True:
        cnt, frame = frame_queue.get()
        if frame is None:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame/256*len(char_set) #256 rather than 255, make it's maxium is L-1
        cvt_frame = ''
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                cvt_frame += char_set[int(frame[i][j])]
            cvt_frame += '\n'
        
        cvt_frame_queue.put((cnt, cvt_frame))

def convert_frame_clr(frame_queue, cvt_frame_queue):
    ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
    char_set = r" `'^*-+x<=oa!1|?0%$@#"

    # 16-color table
    clr16 = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),\
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)]

    while True:
        cnt, frame = frame_queue.get()
        if frame is None:
            break
        
        cvt_frame = ''
        for i in range(frame.shape[0]):
            line_char = ''
            line_clr = ''
            for j in range(frame.shape[1]):
                # get the RGB component
                R, G, B = frame[i][j]
                #RGB convert to gray
                gray = int(0.299*R + 0.587*G + 0.114*B)

                #find the nearest clr
                # delta_list = [(R-clr[0])**2 + (G-clr[0])**2 + (B-clr[0])**2 for clr in clr16]
                # clr_num = delta_list.index(min(delta_list))
                clr = (int(R/256*2)*255, int(G/256*2)*255, int(B/256*2)*255)
                clr_num = clr16.index(clr)
                line_clr += chr(32+clr_num) #add 32 so that it is a printable charater

                # get the character in g_char_set
                idx = int(gray/256*len(char_set))
                line_char += char_set[idx]
                
            cvt_frame += line_char + line_clr + '\n'
        cvt_frame_queue.put((cnt, cvt_frame))

def write_file(cvt_frame_queue, pipe_recv, cvt_num, have_color):
    '''pipe recv
    '''
    video_name, total_frame, FPS, size = pipe_recv.recv()

    file_name = video_name+ '.char.color.txt' if have_color else '.char.txt' 

    with open(file_name,'w') as fp:
        fp.write('total frame:%d\n'\
            'FPS:%d\n'\
            'resolution:%dx%d\n'%(total_frame, FPS, size[0], size[1])
        )

        heap = []
        internal_cnt = 0
        while internal_cnt<total_frame: 
            if internal_cnt%100==0:
                print('\rprogress %d/%d'%(internal_cnt, total_frame))
            internal_cnt+=1
            
            # need to keep ordered
            # if len(heap)>cvt_num:
            #     print('aaa',len(heap))
            while True:
                if len(heap)!=0 and heap[0][0]==internal_cnt:
                    cnt, cvt_frame = heapq.heappop(heap)
                    break
                else:
                    # for i in range(cvt_num//2+1):
                    #     cnt, cvt_frame = cvt_frame_queue.get()
                    #     if not (cvt_frame is None):
                    #         heapq.heappush(heap, (cnt, cvt_frame))
                    #     else:
                    #         break
                    cnt, cvt_frame = cvt_frame_queue.get()
                    if cvt_frame is None:
                        exit(0)
                    heapq.heappush(heap, (cnt, cvt_frame))
            fp.write(str(cnt)+'\n')
            fp.write(cvt_frame)

if __name__ == "__main__":
    # video_path = '../video/bad apple.mp4'
    video_path = '../video/RWBY-RedRose.flv'
    window_height = 44
    have_color = True

    cvt_num = 4
    frame_queue = Queue(cvt_num*2)
    cvt_frame_queue  = Queue(cvt_num*2)
    pipe_send, pipe_recv = Pipe()

    worker_list = []
    p1 = Process(target=read_video, args=(frame_queue, video_path, window_height, pipe_send))
    for i in range(cvt_num):
        pc = Process(target=(convert_frame_clr if have_color else convert_frame),\
                    args=(frame_queue, cvt_frame_queue))
        worker_list.append(pc)
        pc.start()
    c1 = Process(target=write_file, args=(cvt_frame_queue, pipe_recv, cvt_num, have_color))

    p1.start()
    c1.start()

    p1.join()
    for i in range(cvt_num):
        frame_queue.put((0, None))
    for i in range(cvt_num):
        worker_list[i].join()
    cvt_frame_queue.put((0, None))
    c1.join()