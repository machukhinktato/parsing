from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import time
from pw_5.data import LOGIN, PSW

chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome = webdriver.Chrome(options=chrome_options)
chrome.get('https://mail.ru/')

# login = chrome.find_element_by_id('mailbox:login-input')
login = WebDriverWait(chrome, 20).until(
            EC.visibility_of_element_located((By.ID, 'mailbox:login-input'))
        )
login.send_keys(LOGIN)
time.sleep(1)
login.send_keys(Keys.ENTER)
psw = chrome.find_element_by_id('mailbox:password-input')
psw.send_keys(PSW)
time.sleep(1)
psw.send_keys(Keys.ENTER)
time.sleep(5)
inbox = chrome.find_elements_by_class_name('nav__item_active')
print(inbox)
# mail = chrome.find_element_by_tag_name('href')
# print(mail)
# [mail.click() for mail in mail]
# for email in mail:
#     print(f"fuckin {email.find_element_by_tag_name('href')}")
# mail = chrome.find_elements_by_partial_link_text('/inbox/')
# pprint(i.find_element_by_partial_link_text('/inbox/') for i in mail)
# for email in mail:
#     print(f"fuckin {email.find_element_by_partial_link_text('/inbox/')}")
# print(chrome.find_element_by_xpath("//a[contains(@href, 'inbox')]"))
# pprint(mail.text)