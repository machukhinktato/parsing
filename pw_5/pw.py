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


# side_bar = WebDriverWait(chrome, 20).until(
#     EC.visibility_of_element_located((By.CLASS_NAME,'sidebar__menu-ico'))
# )
# side_bar.click()

inbox_element = WebDriverWait(chrome, 20).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'nav__item_active'))
    # EC.visibility_of_element_located((By.LINK_TEXT, '/inbox/'))
)


banana = chrome.find_elements_by_xpath('//a[contains(title, "Входящие")]')
# title = inbox_element.get_attribute('data-title')
print(banana)
print(type(banana))
print(dir(banana))
# html = chrome.find_element_by_tag_name('html')
# for i in range(5):
list_of_links = []
# html.send_keys(Keys.PAGE_DOWN)
# for i in range(25):
                        # banana = True
                        # while banana:
                        #     read_status_elem = WebDriverWait(chrome, 10).until(
                        #         EC.presence_of_element_located((By.CLASS_NAME, 'llc__read-status')))
                        #     actions = ActionChains(chrome)
                        #     letters = chrome.find_elements_by_class_name('js-letter-list-item')
                        #     for itm in letters:
                        #         link = itm.get_attribute('href')
                        #         list_of_links.append(link)
                        #     try:
                        #         actions.move_to_element(letters[-1])
                        #         actions.perform()
                        #     except:
                        #         banana = False
                        #         break
    # finally:
    #     break

# paginator = chrome.find_element_by_class_name('paginator-container__block')
# print(paginator)
url_list = chrome.find_elements_by_class_name('js-letter-list-item')
list_of_links = []
urls = [url.get_attribute('href') for url in url_list]
chrome.get(urls[0])
time.sleep(1)
while True:
    # down_button = chrome.find_element_by_xpath('//span[@data-title="Следующее" or @title = "Следующее"]')
    down_button = chrome.find_element_by_class_name('button2_arrow-down')
    if not down_button.get_attribute('disabled'):
        down_button.click()
    else:
        break
# button2__wrapper
# Keys.LEFT_CONTROL + Keys.PAGE_DOWN
# next_button = WebDriverWait(chrome, 20).until(
#     EC.visibility_of_element_located((By.CLASS_NAME, 'ico ico_16-arrow-down ico_size_s'))
# )
# print(next_button)
# while True:
    # next_button.send_keys(Keys.LEFT_CONTROL + Keys.PAGE_DOWN)
# next_button.click()
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
# finally:
    # chrome.close()
    # url_list = chrome.find_elements_by_class_name('js-letter-list-item')
