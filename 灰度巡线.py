# Untitled - By: 86151 - 周三 5月 17 2023

import sensor, image, time
from pyb import UART
from pyb import LED

#red
th1 =(46, 25, 4, 127, -128, 127)
th2 =(49, 12, 1, 127, -128, 127)
th3 =(50, 0, 4, 127, -128, 127)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_windowing((0,0,160,90))#主车要缩小竖向缩小窗口
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
sensor.skip_frames(time = 2000)
clock = time.clock()
uart=UART(3,9600)
uart.init(9600, bits=8, parity=None, stop=1)

def LED_ON():
    led = LED(1)
    led.on()
    led = LED(2)
    led.on()
    led = LED(3)
    led.on()


def findMyLine(img):
    lin = img.get_regression([(100,255)])
    #将(100,255)范围内的白色像素用于线性回归
    if(lin and lin.magnitude()>=3):
        rho_err = abs(lin.rho())-80#计算线与图像中央偏移的距离80 = width/2
        #if line.theta()>90:#计算线与图像中央偏移角度
            #theta_err = line.theta()-180
        #else:
            #theta_err = line.theta()
        if(rho_err>127):
            rho_err = 127
        if(rho_err<-128):
            rho_err = -128
        img.draw_line(lin.line(),color = 127)
        #uart.write(bytearray([0xb3,0xb3,1,0x5b]))
        print(int(rho_err))

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8).binary([(0,5)])
    #img.mean(1)#减少噪声
    #img.erode(1)#删除边缘像素
    #lens_corr 校准镜头
    findMyLine(img)


    #print(clock.fps())

