from basic_tools import *

import subprocess

class Media:
    def __init__(self, infile, cmd ,outfile=None):
        self.infile = infile              # 输入文件路径
        self.cmd = cmd                    # 命令执行对象
        self.duration = self.get_length(self.infile()) # 获取音频时长

        self.split_start = 0              # 音频分割开始时间
        self.split_duration = 0           # 音频分割时长
        self.finish_flag = -1             # 音频分割完成标志
        # finish_flag 有三种状态: -1,1,0
        # -1 表示音频已被分割但未到结束
        # 0 是临时状态
        # 1 表示音频已被分割至结束

        if outfile == None:              # 如果没有提供输出文件路径，则创建一个新路径
            outfile = FILE_PATH()
            outfile.set_path(self.infile.build_new_file("tmp.mp3"))
            self.outfile = outfile
        else:
            self.outfile = outfile       # 设置输出文件路径

    def get_length(self,filename):       # 获取音频文件时长
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)


    def splite_audio(self,start=-1,duration=-1): # 分割音频
        if start == -1 or duration == -1:
            start = self.split_start
            duration = self.split_duration
        else:
            self.split_start = start
            self.split_duration = duration

        print("splite audio")
        print("start: {}, duration: {}".format(start,duration))

        if duration == 0: # 选择全部
            duration = self.duration
            self.finish_flag = 0
        elif duration+start >= self.duration: # 选择至结束
            duration = self.duration - start
            self.finish_flag = 0

        self.cmd("ffmpeg -i {} -ss {} -t {} -aq 0 -map a {}"\
            .format(self.infile(),start,\
            duration,self.outfile()))

    
    def get_a_part_of_audio(self,duration=-1): # 获取音频的一部分
        print("get_a_part_of_audio")
        if self.finish_flag == 1:
            return None

        if duration == -1:
            self.splite_audio()
            self.split_start = self.split_start + self.split_duration
            self.split_duration = 300
        else:
            self.splite_audio()
            if self.split_start != 0:
                self.split_start = self.split_start + self.split_duration
            self.split_duration = duration

        if self.finish_flag == 0:
            self.finish_flag = 1
            return self.outfile()
        else:
            return self.outfile()

# 其他被注释掉的方法和测试代码

# if __name__ == "__main__":
#     file = PATH_CONVERT()
#     cmd = SYSTEMcmd()
#     media = MEDIA(file, cmd)
#     media.set_media(r"C:\Users\lucyc\Desktop\aaa.mp4")
#     media._timess["start"] = 0
#     media._timess["duration"] = 180
#     media.splite_audio(new_file_name="a.wav")
#     input("Press any key to exit")
