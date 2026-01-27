import time, os, sys, gc
#import time: 导入Python的time模块，用于处理时间相关的操作，例如获取当前时间、暂停程序等
#import os: 导入Python的os模块，用于与操作系统交互，例如文件/目录操作、获取环境变量等
#import sys: 导入Python的sys模块，用于访问与Python解释器相关的变量和函数，例如命令行参数、退出程序等

from media.sensor import * #导入sensor模块，使用摄像头相关接口
from media.display import * #导入display模块，使用display相关接口
from media.media import * #导入media模块，使用meida相关接口

try:
    sensor = Sensor() #构建摄像头对象
    sensor.reset() #复位sensor对象。在构造Sensor对象后，必须调用此函数以继续执行其他操作
    sensor.set_framesize(width=800,height=480) #设置指定通道的输出图像尺寸，宽度会自动对齐到16像素宽，默认通道0
    sensor.set_pixformat(Sensor.RGB565) #配置指定通道的图像传感器输出图像格式，默认通道0
    sensor.set_hmirror(0) #配置图像传感器是否进行水平镜像
    sensor.set_vflip(0) #配置图像传感器是否进行垂直翻转

    Display.init(Display.ST7701, sensor.width(), sensor.height()) #初始化Display通路，VIRT:IDE缓冲区显示；LT9611:HDMI显示；ST7701:mipi显示屏

    MediaManager.init() #初始化媒体管理器

    sensor.run() #启动图像传感器的输出，须在MediaManager.init()之后
    while True:
        os.exitpoint()
        img = sensor.snapshot() #拍摄一张图
        Display.show_image(img) #显示图片

except KeyboardInterrupt as e:
    print("user stop: ", e)
except BaseException as e:
    print(f"Exception {e}")

finally:
    if isinstance(sensor, Sensor):
        sensor.stop()               # 停止摄像头
    Display.deinit()                # 关闭显示
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)  # 允许休眠
    time.sleep_ms(100)             # 延迟一会儿，等待硬件稳定
    MediaManager.deinit()          # 释放媒体资源

