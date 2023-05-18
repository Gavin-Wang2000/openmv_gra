# Untitled - By: 86151 - 周三 5月 17 2023

import sensor, image, time
from pyb import UART
from pyb import LED

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)#160*120 X Y
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

# 配置颜色跟踪器
thresholds = (0, 53, -22, 3, -12, 26) # 定义阈值范围
blobs_params = {
    "threshold": 200, # 阈值
    "pixels_threshold": 100, # 像素数阈值
    "merge": True # 合并重叠区域
}
roiArea = [(0,40,30,40),[130,40,30,40]]
def findStopline(img):
    stopLinenum = [0,0]
    for area in roiArea :
        blobs = img.find_blobs([[100,250]],roi =area ,x_stride=3, y_stride=3,
                           pixels_threshold=2, area_threshold=500,
                           merge=False, margin=1)# 寻找色块
        for blob in blobs:# 对每个色块进行处理
        # 在原图上绘制矩形
            if blob.area() >= 700:
                img.draw_rectangle(blob.rect(), color = (0, 255, 0))
                stopLinenum[roiArea.index(area)] = 1
            else :
                stopLinenum[roiArea.index(area)] = 0
    return stopLinenum
# 主循环
while True:
    # 拍摄一张图像
    img = sensor.snapshot()
    # 对图像进行二值化处理
    img.binary([thresholds])
    stopLinenum = findStopline(img)
    print(stopLinenum)





