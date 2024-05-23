# Wordcloud_video

生成一个每一帧都是词云的视频.

## 依赖

1. python
2. opencv-python, pillow, jieba, worcloud, ffmpeg-python 库
3. ffmepg (没有也行, 但是只生成无声音文件)

## 使用

你需要:

1. 命名为video.mp4的绿幕文件作为轮廓图
2. 中文文档data.txt用于生成词云

## 产出

1. output.avi:一个没有声音的视频
2. combined_video.mp4:混入原视频的音频的视频
