from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

chrome = webdriver.Chrome(options=chrome_options)

chrome.get('https://mail.ru/')
# log_button = chrome.find_element_by_id('PH_authLink')
# log_button.click()

login = chrome.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172@mail.ru')
time.sleep(1)
next_button = chrome.find_element_by_id('mailbox:submit-button')
next_button.click()
#
# passw = driver.find_element_by_id('user_password')
# passw.send_keys('Password172')
#
# passw.send_keys(Keys.ENTER)
# time.sleep(1)