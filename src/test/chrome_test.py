from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument(r"--user-data-dir=C:\Users\lucyc\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
driver = webdriver.Chrome(options=options)

driver.get('https://www.gog.com/')

time.sleep(5)

driver.get('https://my.unimelb.edu.au/')
time.sleep(60)

# submit_button = driver.find_element(by=By.XPATH, value='//a[@href="https://canvas.lms.unimelb.edu.au/login/saml"]')
# #submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
# submit_button.click()

# # 创建新的标签页
# driver.execute_script("window.open('');")
# # 切换到新的标签页
# driver.switch_to.window(driver.window_handles[1])
# driver.get('http://www.bing.com')

# print("Bing opened")


#chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"

# # 切换回第一个标签页
# driver.switch_to.window(driver.window_handles[0])
# print("Switched back to Google")
# time.sleep(5)
# for i in range(1,999):

#     #print(driver.window_handles)

#     try:
#         ct = driver.find_element(by=By.CLASS_NAME, value='currTime')
#         print(ct.text, end=": ")
#         text = driver.find_element(by=By.CLASS_NAME, value='highlight')
#         print(text.text)
#     except:
#         print("No text found")
    
#     if i % 5 == 0:
#         try:
#             ps = driver.find_element(by=By.CSS_SELECTOR, value='.video-btn.play-btn')
#             ps.click()
#             time.sleep(1)
#             ps.click()
#         except:
#             print("No play button found")
            
#     time.sleep(1)




#cc = ChromeControl("127.0.0.1:9222", r"C:\Users\lucyc\AppData\Local\Google\Chrome\User Data", "Default")

# options = webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_argument(r"--user-data-dir=C:\Users\lucyc\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
# options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
# driver = webdriver.Chrome(options=options)

# driver.get('https://echo360.net.au/lesson/e3cf1f00-26a0-451b-be3c-1279326b8e11/classroom')
# print("Melbourne opened")


# submit_button = driver.find_element(by=By.XPATH, value='//a[@href="https://canvas.lms.unimelb.edu.au/login/saml"]')
# #submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
# submit_button.click()

# # 创建新的标签页
# driver.execute_script("window.open('');")
# # 切换到新的标签页
# driver.switch_to.window(driver.window_handles[1])
# driver.get('http://www.bing.com')

# print("Bing opened")


#chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"

# # 切换回第一个标签页
# driver.switch_to.window(driver.window_handles[0])
# print("Switched back to Google")
# time.sleep(5)
# for i in range(1,999):

#     #print(driver.window_handles)

#     try:
#         ct = driver.find_element(by=By.CLASS_NAME, value='currTime')
#         print(ct.text, end=": ")
#         text = driver.find_element(by=By.CLASS_NAME, value='highlight')
#         print(text.text)
#     except:
#         print("No text found")
    
#     if i % 5 == 0:
#         try:
#             ps = driver.find_element(by=By.CSS_SELECTOR, value='.video-btn.play-btn')
#             ps.click()
#             time.sleep(1)
#             ps.click()
#         except:
#             print("No play button found")
            
#     time.sleep(1)