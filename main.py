import cv2
import numpy as np
from PIL import Image
import jieba
from wordcloud import WordCloud
import ffmpeg

threshold = 210 # 颜色识别阈值
new_fps = 30 # 

# 读取一个绿幕视频video.mp4的每一帧（使用OpenCV）
cap = cv2.VideoCapture("video.mp4")

fps = int(cap.get(cv2.CAP_PROP_FPS)) 
interval = fps // new_fps
interval = interval if interval else 1 # 防止输入的帧率过大

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) // interval
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'MPEG'), new_fps, (width, height))

# 读取中文文档data.txt，使用jieba库进行分词
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()
    words = " ".join(jieba.cut(text))

# 读取总帧数
print(f"总帧数:{frame_count}.")

i = 0
while True:
    i += 1
    ret, frame = cap.read()
    if i % interval != 0:
        continue

    print(f"第{i//interval}/{frame_count}帧.进度:{i//interval/frame_count:.2%}.")
    if ret:
        # 访问绿色（G）通道  
        green_channel = frame[:, :, 1]
        # 创建一个布尔数组，其中大于200的值为True  
        green_threshold = green_channel > threshold  

        # 将绿色通道大于200的像素的RGB值都设置为白色  
        frame[green_threshold, :] = [255, 255, 255]
        
        
        # 创建词云对象
        wc = WordCloud(
                font_path="simhei.ttf",
                background_color="white",
                max_words=2000,
                width=width, 
                height=height,
                mask = frame #mask数据类型:nd-array
                ) 
        
        wc.generate(words)

        # 生成词云图片
        wordcloud_image = wc.to_image() #数据类型: PIL.Image

        # 将处理后的这一帧作为轮廓图传递给wordcloud
        frame_array = np.array(wordcloud_image) 

        # 将词云的图片对于数组写入新的视频result.mp3的每一帧
        out.write(frame_array)
    else:
        break

    

# 释放资源

cap.release()
out.release()
cv2.destroyAllWindows()

# 合并音轨
input_video1 = "video.mp4"
input_video2 = "output.avi"
output_video = "combined_video.mp4"

input_stream1 = ffmpeg.input(input_video1)
input_stream2 = ffmpeg.input(input_video2)

audio1 = input_stream1.audio
audio2 = input_stream2.audio

video1 = input_stream1.video
video2 = input_stream2.video

output_stream = ffmpeg.output(audio1, video2, output_video, vcodec="copy", acodec="aac")
output_stream.run()