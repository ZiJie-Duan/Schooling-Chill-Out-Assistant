from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class ChromeControl:

    def __init__(self, url, user_data_dir, profile_directory):
        self.page_dict = {}

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("debuggerAddress", url)
        self.options.add_argument(r"--user-data-dir=" + user_data_dir) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        self.options.add_argument(r'--profile-directory=' + profile_directory) #e.g. Profile 3
        print("Chrome options set")
        self.driver = webdriver.Chrome(options=self.options)
        print("Chrome opened")
    
    def get_url(self, url):
        self.driver.get(url)

    def switch_page(self, name):
        self.driver.switch_to.window(self.page_dict[name])

    def open_page(self, name):
        self.driver.execute_script("window.open('');")
        self.page_dict[name] = self.driver.window_handles[-1]
        self.switch_page(name)

    def close_page(self, name):
        self.driver.close(self.page_dict[name])
        del self.page_dict[name]


class Unimelb_Lecture_Rec_CC(ChromeControl):

    def __init__(self, url, user_data_dir, profile_directory):
        super().__init__(url, user_data_dir, profile_directory)

    def lock_page(self, url):
        self.open_page("rec_page")
        self.get_url(url)
    
    def lock_element(self):
        self.play_button = self.driver.find_element(by=By.CSS_SELECTOR, value='.video-btn.play-btn')
        self.curr_time = self.driver.find_element(by=By.CLASS_NAME, value='currTime')

    def get_subtitle(self):
        try:
            subtitle = self.driver.find_element(by=By.CLASS_NAME, value='highlight')
            subtitle_text = subtitle.text
        except:
            subtitle_text = "<No-text-found>"
        
        return (self.curr_time.text, subtitle_text)

    def play_or_stop(self):
        self.play_button.click()
    


#cc = ChromeControl("127.0.0.1:9222", r"C:\Users\lucyc\AppData\Local\Google\Chrome\User Data", "Default")

# if __name__ == "__main__":
#     melb_cc = Unimelb_Lecture_Rec_CC("127.0.0.1:9222", r"C:\Users\lucyc\AppData\Local\Google\Chrome\User Data", "Default")
#     url = input("Enter URL: ")
#     melb_cc.lock_page(url)
#     melb_cc.lock_element()
#     count = 0
#     while True:
#         count += 1
#         time.sleep(1)
#         print(melb_cc.get_subtitle())
#         if count % 5 == 0:
#             melb_cc.play_or_stop()
#             time.sleep(1)
#             melb_cc.play_or_stop()
