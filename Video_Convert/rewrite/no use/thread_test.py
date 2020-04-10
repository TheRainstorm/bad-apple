import threading as td
import multiprocessing as mt
import time

def func(L, lock):
    for i in range(10):
        with lock:
            length = len(L)
            s = 0
            for i in range(length):
                s += L[i]
        print(s)
        time.sleep(1)

def main():
    L = list(range(1000000))
    lock = td.Lock()

    td1 = td.Thread(target=func, args=(L, lock))
    td1.start()

    for i in range(10):
        with lock:
            del L[0]
        time.sleep(0.1)
    
    td1.join()


def func2(L):
    L[0] = 9

def main2():
    L = [0, 2]

    p1 = mt.Process(target=func2, args=(L, ))
    p1.start()

    print(L)

if __name__ == "__main__":
    main()