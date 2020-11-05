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
url_list = chrome.find_elements_by_class_name('js-letter-list-item')
# url_set = []
# url_set.add([url.get_attribute('href') for url in url_list])
list_of_links = []
urls = [url.get_attribute('href') for url in url_list]
print(type(urls))
# for i in range(len(url_set)):

# pprint(type(url_set[i]))

# print(len(url_list))
for i in range(len(urls)):
#     read_status_elem = WebDriverWait(chrome, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'llc__read-status')))
    actions = ActionChains(chrome)
    list_of_links.append(urls[i])
# letters = chrome.find_elements_by_class_name('js-letter-list-item')
# for itm in letters:
#     link = itm.get_attribute('href')
#     list_of_links.append(link)

    actions.move_to_element(url_list[-1])
    actions.perform()
# pprint(list_of_links)

# list_tmp = []
# for link in list_of_links:
#     for elem in range(len(link)):
#         print(itm[elem])
# send_info = WebDriverWait(chrome, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
# sender = send_info.find_element_by_class_name('letter-contact').text
# when_sended = send_info.find_element_by_class_name('letter__date').text
# header = WebDriverWait(chrome, 10).until(
#     EC.presence_of_element_located((By.TAG_NAME, 'h2'))).text
# body = chrome.find_element_by_class_name('letter-body').text
# list_tmp.append({'Sender': sender, 'When sended': when_sended, 'Header': header, 'Body': body})

# collection.delete_many({})
# collection.insert_many(list_tmp)
# pprint(list_tmp)

emails = []
try:
    for a in list_of_links:
        chrome.get(a)
        letter_author_wrapper = WebDriverWait(chrome, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'letter__author'))
        )
        email = {
            'letter_author': letter_author_wrapper.find_element_by_class_name('letter-contact').get_attribute('title'),
            'letter_date': letter_author_wrapper.find_element_by_class_name('letter__date').text,
            'letter_title': chrome.find_element_by_class_name('thread__subject').text,
            'letter_body': chrome.find_element_by_class_name('letter-body').text
        }
        emails.append(email)
        print(f"Обработана ссылка: {a}")
except Exception as e:
    print(f'something going wrong\n {e}')
finally:
    chrome.close()
    # url_list = chrome.find_elements_by_class_name('js-letter-list-item')
