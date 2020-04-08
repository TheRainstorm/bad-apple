#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <pthread.h>

#define TXTFILE_PATH "BadApple384_512_44_117.txt"
#define WIDTH 117
#define HEIGHT 44

HANDLE g_hStdOut;

void goto_XY(int x, int y) {
    COORD pos = {x, y};
    SetConsoleCursorPosition(g_hStdOut, pos); //两个参数分别是指定哪个窗体，具体位置
}

void play_audio(){
    system("ffplay -nodisp ../videos/BadApple384_512.mp4 >ffplay.log 2>&1");
}

int main(){
    pthread_t tid;
    pthread_create(&tid, NULL, play_audio, NULL);

    g_hStdOut = GetStdHandle(STD_OUTPUT_HANDLE); // 获取标准输出设备句柄

	int FRAME_NUM;  //视频总帧数
	int FPS;        //视频每秒帧数
    char frame[HEIGHT][WIDTH+1]; //存放每一帧字符数组

	FILE *fp = fopen(TXTFILE_PATH, "r");
    if(fp==NULL){
        printf("read %s failed!\n", TXTFILE_PATH);
        exit(-1);
    }

    fscanf(fp, "%d\n", &FRAME_NUM);
    fscanf(fp, "%d\n", &FPS);

    // goto_XY(0, 0);
    // printf("%d %d\n", FRAME_NUM, FPS);

    // int i;
    // for(i=0;i<44*30*10;i++){
    //     fgets(frame[0], WIDTH+1, fp);
    // }

    // for(i=0;i<44;i++){
    //     fgets(frame[0], WIDTH+1, fp);
    //     fputs(frame[0], stdout);
    // }

    // fread(frame, WIDTH*sizeof(char)+1, HEIGHT, fp);
    // fwrite(frame, WIDTH*sizeof(char)+1, HEIGHT, stdout);

    int i;
    for(i=0;i<52;i++){
        fgets(frame[0], WIDTH+1, fp);
    }
	for(i=0;i<FRAME_NUM;i++){
        clock_t start_time = clock();
        goto_XY(0, 0);
        fread(frame, WIDTH*sizeof(char)+1, HEIGHT, fp);
        fwrite(frame, WIDTH*sizeof(char)+1, HEIGHT, stdout);
        clock_t end_time = clock();
        float delta=(end_time - start_time)/CLOCKS_PER_SEC*1000;    //ms
        //printf("%f",delta);
		Sleep(1.0/FPS*1000- delta);
	}
    fclose(fp);
	return 0;
}
