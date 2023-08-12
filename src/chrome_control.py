from selenium import webdriver
from selenium.webdriver.common.by import By

class ChromeControl:

    def __init__(self, url, user_data_dir, profile_directory):
        self.page_dict = {} # 用于存储打开的页面

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", url)
        self.options.add_argument(r"--user-data-dir=" + user_data_dir) # 设置用户数据目录
        self.options.add_argument(r'--profile-directory=' + profile_directory) # 设置配置文件目录
        print("Chrome options set")
        self.driver = webdriver.Chrome(options=self.options) # 打开Chrome浏览器
        print("Chrome opened")

    def get_url(self, url): # 访问指定网址
        self.driver.get(url)

    def switch_page(self, name): # 切换页面
        self.driver.switch_to.window(self.page_dict[name])

    def open_page(self, name): # 打开新的页面
        self.driver.execute_script("window.open('');")
        self.page_dict[name] = self.driver.window_handles[-1]
        self.switch_page(name)

    def close_page(self, name): # 关闭指定页面
        self.driver.close(self.page_dict[name])
        del self.page_dict[name]


class Unimelb_Lecture_Rec_CC(ChromeControl):

    def __init__(self, url, user_data_dir, profile_directory):
        super().__init__(url, user_data_dir, profile_directory)

    def lock_page(self, url): # 锁定特定页面
        self.open_page("rec_page")
        self.get_url(url)

    def lock_element(self): # 锁定元素
        self.play_button = self.driver.find_element(by=By.CSS_SELECTOR, value='.video-btn.play-btn')
        self.curr_time = self.driver.find_element(by=By.CLASS_NAME, value='currTime')

    def get_subtitle(self): # 获取字幕
        try:
            subtitle = self.driver.find_element(by=By.CLASS_NAME, value='highlight')
            subtitle_text = subtitle.text
        except:
            subtitle_text = "<No-text-found>"
        
        return (self.curr_time.text, subtitle_text)

    def play_or_stop(self): # 控制播放或停止
        self.play_button.click()



#cc = ChromeControl("127.0.0.1:9222", r"C:\Users\lucyc\AppData\Local\Google\Chrome\User Data", "Default")

# if __name__ == "__main__":
#     melb_cc = Unimelb_Lecture_Rec2_CC("127.0.0.1:9222", r"C:\Users\lucyc\AppData\Local\Google\Chrome\User Data", "Default")
#     url = input("Enter URL: ")
#     melb_cc.lock_page(url)
#     while 1:
#         time.sleep(1)
#         print(melb_cc.get_subtitle())
    # melb_cc.lock_element()
    # count = 0
    # while True:
    #     count += 1
    #     time.sleep(1)
    #     print(melb_cc.get_subtitle())
    #     if count % 5 == 0:
    #         melb_cc.play_or_stop()
    #         time.sleep(1)
    #         melb_cc.play_or_stop()
