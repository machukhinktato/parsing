from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument('start-maximized')

chrome = webdriver.Chrome(options=chrome_options)

chrome.get('https://mail.ru/')
log_button = chrome.find_element_by_id('PH_authLink')
log_button.click()
# login = driver.find_element_by_id('PH_authLink')
# login.send_keys('study.ai_172@mail.ru')
#
# passw = driver.find_element_by_id('user_password')
# passw.send_keys('Password172')
#
# passw.send_keys(Keys.ENTER)
# time.sleep(1)