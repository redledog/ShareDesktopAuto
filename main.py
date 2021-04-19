import pywinauto as pwa
import time
import tkinter as tk
import winsound
import threading

# chrome_name = 'Chrome 원격 데스크톱'
chrome_name = 'Chrome'
chrome_class = '#32770'

# 메인이 작동중인지 여부 확인용
global RUN
RUN = True

# 얼마나 계속을 처리했는지 확인용
global count_done
count_done = 0

global DEBUG_MODE
DEBUG_MODE = True

app = pwa.application.Application()

root = tk.Tk()

WORK_TEXT = '작동중...'

def dprint(msg):
    if DEBUG_MODE:
        print(msg)

def dsound():
    if DEBUG_MODE:
        winsound.PlaySound("button.wav", winsound.SND_ALIAS)

def check_connect_dialog():
    if not check_main():
        return
    dsound()
    dprint(f'Find Title : {chrome_name}')
    handles = pwa.findwindows.find_windows(title_re=chrome_name)
    if len(handles) < 1:
        dprint('Not exist window')
        root.after(3000, find_threading)
    else:
        for handle in handles:
            try:
                app.connect(handle=handle)
                window = app.window(handle = handle)
                window['계속'].click()

                global count_done
                count_done += 1
                
                dprint(f'Done. count:{count_done}')
            except:
                dprint(f'Not Yet. count:{count_done}')
                continue
        root.after(3000, find_threading)

def quit_btn_onclick():
    global RUN
    RUN = False
    root.withdraw()
    dprint('메인창을 숨깁니다..')

#쓰레딩 해서 찾는 함수
def find_threading():
    if check_main():
        findThread = threading.Thread(target=check_connect_dialog)
        findThread.start()

# 종료 메서드
def check_main():
    global RUN
    if RUN:
        return RUN
    else:
        dprint('메인 종료')
        root.quit()
        return RUN

# tkinter 설정
root.title('원격데스크톱 자동 클리커')
root.geometry('320x80')
root.resizable(width=False, height=False)

lbl = tk.Label(root, text = WORK_TEXT)
lbl.pack()

lbl2 = tk.Label(root, text = f'클릭된 횟수 : {count_done}')
lbl2.pack()

quit_btn = tk.Button(root, text = '종료', command=quit_btn_onclick)
quit_btn.pack()

# x 클릭해서 창닫을때 처리
root.protocol("WM_DELETE_WINDOW", quit_btn_onclick)

# 쓰레딩 함수 실행
find_threading()

# tkinter 실행
root.mainloop()
