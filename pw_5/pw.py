from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import re
import time
from pw_5.data import LOGIN, PSW

chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome = webdriver.Chrome(options=chrome_options)
chrome.get('https://mail.ru/')

login = WebDriverWait(chrome, 20).until(
    EC.visibility_of_element_located((By.ID, 'mailbox:login-input'))
)
login.send_keys(LOGIN)
login.send_keys(Keys.ENTER)

psw = WebDriverWait(chrome, 20).until(
    EC.visibility_of_element_located((By.ID, 'mailbox:password-input'))
)
psw.send_keys(PSW)
psw.send_keys(Keys.ENTER)

inbox_element = WebDriverWait(chrome, 20).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'nav__item_active'))
)
# print(dir(inbox_element))
# print(inbox_element.text)

url_list = chrome.find_elements_by_class_name('js-letter-list-item')

urls = [url.get_attribute('href') for url in url_list]
chrome.get(urls[0])
emails = []
while True:
    send_info = WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
    try:
        sender = send_info.find_element_by_class_name('letter-contact').text
    except:
        sender = None
    try:
        when_sended = send_info.find_element_by_class_name('letter__date').text
    except:
        when_sended = None
    header = WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h2'))).text
    try:
        body = chrome.find_element_by_class_name('letter-body').text
    except:
        body = None
    emails.append({'Sender': sender, 'When sended': when_sended, 'Header': header, 'Body': body})
    # print(email)
    # print(f"Обработана ссылка: {a}")
# except Exception as e:
# print(f'something going wrong\n {e}')

    down_button = WebDriverWait(chrome, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'button2_arrow-down'))
    )

    if not down_button.get_attribute('disabled'):
        down_button.click()
    else:
        break

print(emails)
# emails = []
# try:
#     for a in list_of_links:
#         chrome.get(a)
#         letter_author_wrapper = WebDriverWait(chrome, 20).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'letter__author'))
#         )
#
#         email = {
#             'letter_author': letter_author_wrapper.find_element_by_class_name('letter-contact').get_attribute('title'),
#             'letter_date': letter_author_wrapper.find_element_by_class_name('letter__date').text,
#             'letter_title': chrome.find_element_by_class_name('thread__subject').text,
#             'letter_body': chrome.find_element_by_class_name('letter-body').text
#         }
#         emails.append(email)
        # print(f"Обработана ссылка: {a}")
# except Exception as e:
#     print(f'something going wrong\n {e}')
# finally:
    # chrome.close()
    # url_list = chrome.find_elements_by_class_name('js-letter-list-item')
