import time, os, sys, gc
#import time: 导入Python的time模块，用于处理时间相关的操作，例如获取当前时间、暂停程序等
#import os: 导入Python的os模块，用于与操作系统交互，例如文件/目录操作、获取环境变量等
#import sys: 导入Python的sys模块，用于访问与Python解释器相关的变量和函数，例如命令行参数、退出程序等

from media.sensor import * #导入sensor模块，使用摄像头相关接口
from media.display import * #导入display模块，使用display相关接口
from media.media import * #导入media模块，使用meida相关接口

#设置图像采集和处理的分辨率（宽度按16对齐）
DETECT_WIDTH = ALIGN_UP(800, 16)
DETECT_HEIGHT = 480

sensor = None

#摄像头初始化函数
def camera_init():
    global sensor #声明使用全局变量sensor
    sensor = Sensor(width=DETECT_WIDTH, height=DETECT_HEIGHT) #构建传感器对象，指定采集分辨率
    sensor.reset() #复位sensor对象。在构造Sensor对象后，必须调用此函数以继续执行其他操作
    sensor.set_framesize(width=DETECT_WIDTH, height=DETECT_HEIGHT) #设置指定通道的输出图像尺寸，宽度会自动对齐到16像素宽
    sensor.set_pixformat(Sensor.RGB565) #配置指定通道的图像传感器输出图像格式
    sensor.set_hmirror(False) #配置图像传感器是否进行水平镜像
    sensor.set_vflip(True) #配置图像传感器是否进行垂直翻转
    Display.init(Display.ST7701, width=DETECT_WIDTH, height=DETECT_HEIGHT, fps=60, to_ide=True) #初始化Display通路
    MediaManager.init() #初始化媒体缓冲池管理器
    sensor.run() #启动图像传感器的输出，须在MediaManager.init()之后

#摄像头释放函数
def camera_deinit():
    global sensor #声明使用全局变量sensor
    sensor.stop() #停止图像采集
    Display.deinit() #释放显示设备
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP) #通知IDE可以进入休眠状态
    time.sleep_ms(100) #延迟一会儿，等待硬件稳定
    MediaManager.deinit() #释放媒体缓冲区资源

# 图像采集和处理主循环
def capture_picture():
    fps = time.clock()#创建FPS计时器对象

    while True:
        fps.tick()

        try:
            os.exitpoint() #IDE控制点检查，支持在IDE中点击停止运行
            global sensor #声明使用全局变量sensor

            img = sensor.snapshot()  # 拍摄一张图
            Display.show_image(img)  # 显示图片

            print(fps.fps()) #打印当前帧率

        except KeyboardInterrupt as e:
            print("用户中断运行：", e)
            break
        except BaseException as e:
            print(f"运行异常：{e}")
            break

# 主程序入口
def main():
    os.exitpoint(os.EXITPOINT_ENABLE) #启用IDE控制点（允许IDE退出控制）

    camera_is_init = False

    try:
        print("摄像头初始化")
        camera_init()
        camera_is_init = True

        print("开始图像采集与边缘检测")
        capture_picture()

    except Exception as e:
        print(f"主程序异常：{e}")

    finally:
        #程序退出前释放资源
        if camera_is_init:
            print("摄像头资源释放")
            camera_deinit()

#如果是主模块运行，则调用main()
if __name__ == "__main__":
    main()


