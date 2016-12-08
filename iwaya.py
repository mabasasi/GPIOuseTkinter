# -*- coding: utf-8 -*-

from Tkinter import *
import time
import RPi.GPIO as GPIO

# GPIO 初期化
GPIO.setmode(GPIO.BOARD)
TRIG = 11
ECHO = 13
WAIT = 0.1 #最小値が良い

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, GPIO.LOW) # 初期値はlow

# (1)TRIG端子を10us以上highにする(40kHzパルス8回)
# (2)受信するとECHO端子がhighになる
# (3)ECHO端子がhighになっている時間の半分を音速で割った数値が距離
# l = (hTime / 3*10^8) / 2


# trueで受信モード、falseで未受信モード
sensor = False
startTime = 0L
endTime = 0L


# 毎ループで行うGPIO処理
def reading():
    print 'reading... mode='+sensor
    global sensor
    if not sensor:
        # 未受信モードの場合、(1)を行う
        GPIO.output(TRIG, True)
        time.sleep(WAIT)
        GPIO.output(TRIG, False)
        sensor = True #センサーを受信モードへ変更
    elif startTime == 0L and GPIO.input(ECHO) == 1:
        # 受信モードで、開始時間がnilで、ECHO端子がhighなら、開始時間を記録する
        startTime = time.time()
    elif startTime != 0L and GPIO.input(ECHO) == 0:
        # 受信モードで、開始時間があって、ECHO端子がlowなら、距離を計算する
        endTime = time.time()
        t = endTime - startTime #経過時刻を計算
        d = t * 17000 #この式でl[cm]が出るらしい
        output(d)
        # 初期化
        init(None)
        root.after(WAIT, reading) #できる限り最小値で呼び出したい

# 距離が測定し終わった後の、処理関数
def output(destance):
    global outLabel
    print 'len = ' + distance + 'cm')
    outLabel.set("len = "+distance+" cm")


# 初期化関数 (イベントと使い回し)
def init(event):
    global sensor
    global startTime
    global endTime
    sensor = False
    startTime = 0L
    endTime = 0L




# Tkinter初期化
root = Tk()
root.title("GPIO Event Test.")

# バグった時の初期化用
initButton = Tkinter.Button(text=u'初期化', width=50)
initButton.bind("<Button-1>",init)
initButton.pack()

outLabel = Tkinter.Label(text=u'waiting')
outLabel.pack()

reading()
root.mainloop()