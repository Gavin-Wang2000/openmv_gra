# Untitled - By: 86151 - 周一 7月 17 2023
#上电可用按键读取一次指定位置阈值
#采集区域在寻迹区域中心上方
import sensor, image, time, lcd
from pyb import Pin,LED
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
#sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡
sensor.skip_frames(time = 2000)
lcd.init()

#循迹识别区块：
areas = [(30,56,14,8),(44,56,14,8), (58,56,14,8),(72,56,14,8),
         (86,56,14,8), (100,56,14,8),(114,56,14,8)]
center_Roi = (72,56-8,14,8)#中间采样区
#阈值
black_threshold = [[0],(6, 26, -12, 8, -6, 14)]
black_min = 90
black_max = 120
clock = time.clock()
#画出指定地区的框
def draw_findColorRangtanle(img):
    #img.draw_rectangle(center_Roi)
    pass

#找到指定地点的阈值
def find_thresholds(img):
    stat = img.get_statistics(roi=center_Roi)
    center_threshold = (stat.l_mean()-10,stat.l_mean()+10,#a_min(),a_max()
                        stat.a_mean()-10,stat.a_mean()+10,
                        stat.b_mean()-10,stat.b_mean()+10)
    return center_threshold

#读取文件夹阈值
def read_threshold(path):
    THRESHOLD = [0]*6
    i=0
    with open(path,'r+') as f:
        line = f.readline().strip().strip('[]').split(',')
        #print(line)
        for n in line:
            THRESHOLD[i] = int(n)
            i += 1
        f.close()
        return THRESHOLD
#写入文件夹阈值
def writr_threshold(THRESHOLD,path):
    with open(path,'w+') as f:
        THRESHOLD = str(THRESHOLD).strip('').strip('()').strip('[]')
        f.write(THRESHOLD)

#得到循迹值函数：
def getTrace(img):
    Trace = [0,0,0,0,0,0,0] #循迹值初始值
    for area in areas:                            #遍历所有识别区块
        blobs = img.find_blobs(black_threshold,roi=area, x_stride=3, y_stride=3,
                           pixels_threshold=2, area_threshold=30,
                           merge=False, margin=1)
        for blob in blobs:
            if blob.area() <= (black_max):
                Trace[areas.index(area)] = 1          #记录入循迹值
            else :
                Trace[areas.index(area)] = 0          #记录入循迹值
    return Trace

#标记函数：
def Mark(Trace):
    #【1】标记巡线：
    for i in range(len(Trace)):
        area = areas[i]                                   #得到对应区块元组
        img.draw_rectangle(area)                          #圈出识别区块
        if Trace[i]==1:
            img.draw_string(area[0]+4, area[1], "1")      #标记为1
        else: img.draw_string(area[0]+4, area[1], "0")    #标记为0
def LED_ON():
    led = LED(1)
    led.on()
    led = LED(2)
    led.on()
    led = LED(3)
    led.on()
LED_ON()


file ="./threshold.txt"
pin1 = Pin('P1', Pin.IN, Pin.PULL_UP)   ##将P1口作为阈值控制口 OUT_PP PULL_NONE
black_threshold[0] = read_threshold(file)
while(True):
    clock.tick()
    img = sensor.snapshot()
    key0 = pin1.value()      ##按键控制
    draw_findColorRangtanle(img)
    if key0 == 0:
       hous = find_thresholds(img)
       writr_threshold(hous,file)
       black_threshold[0] = hous

    print(black_threshold)
    trace = getTrace(img)
    Mark(trace)
    lcd.display(img)
