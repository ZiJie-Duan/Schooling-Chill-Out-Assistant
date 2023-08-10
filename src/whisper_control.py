import whisper

class whisper_driver:

    def __init__(self) -> None:
        self.model = None           # 初始化模型为None
        self.result = None          # 初始化结果为None
        self.num_of_sentence = 0    # 初始化句子数量为0
        self.sentence_index = 0     # 初始化句子索引为0

    def model_load(self,model = "tiny.en"):
        self.model = whisper.load_model(model) # 加载指定模型

    def transcribe(self,file_path):
        self.result = self.model.transcribe(file_path,verbose=True) # 转录文件路径中的音频
    
    def get_result(self):
        return self.result # 返回转录结果

    def init_reader(self):
        self.num_of_sentence = len(self.result["segments"]) # 初始化句子数量
        self.sentence_index = -1 # 初始化句子索引


    def time_convert(self,time):
        # 将时间（秒）转换为时、分、秒、毫秒
        hours = time // 3600
        remain = time % 3600
        min = remain // 60
        remain = remain % 60
        sec = remain // 1
        msec = remain % 1
        msec = (msec // 0.001)
        return (int(hours),int(min),int(sec),int(msec))

    def get_sentence(self):
        self.sentence_index += 1
        if self.sentence_index < self.num_of_sentence:
            # 如果索引小于句子数量，返回当前句子的开始时间、结束时间和文本
            return (self.time_convert(self.result["segments"][self.sentence_index]["start"]),\
                    self.time_convert(self.result["segments"][self.sentence_index]["end"]),\
                    self.result["segments"][self.sentence_index]["text"])
        else:
            # 如果索引大于或等于句子数量，返回None
            return (None,None,None)

        

wd = whisper_driver()

wd.model_load()
wd.transcribe(r"C:\Users\lucyc\Desktop\05D.WAV")

wd.init_reader()
senc = None
while True:
    senc = wd.get_sentence()
    if senc != (None,None,None):
        print("[{}:{}:{},{} ----> {}:{}:{},{}] {}".format(
            senc[0][0],senc[0][1],senc[0][2],senc[0][3],\
            senc[1][0],senc[1][1],senc[1][2],senc[1][3],\
            senc[2]))
    else:
        break
        

