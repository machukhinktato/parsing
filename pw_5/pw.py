from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from pw_5.data import LOGIN, PSW

chrome_options = Options()
chrome_options.add_argument('start-maximized')

chrome = webdriver.Chrome(options=chrome_options)

chrome.get('https://mail.ru/')
# log_button = chrome.find_element_by_id('PH_authLink')
# log_button.click()

login = chrome.find_element_by_id('mailbox:login-input')
login.send_keys(LOGIN)
time.sleep(1)
next_button = chrome.find_element_by_id('mailbox:submit-button')
next_button.click()
psw = chrome.find_element_by_id('mailbox:password-input')
psw.send_keys(PSW)
time.sleep(1)
psw.send_keys(Keys.ENTER)
# time.sleep(1)