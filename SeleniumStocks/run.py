from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import os
import time
# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
chrome_options.add_argument('user-agent={0}'.format(user_agent))

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# current directory
chrome_driver = os.getcwd() +"/chromedriver"
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.delete_all_cookies()
# For nasdaq
driver.get("https://www.nasdaq.com/market-activity/stocks/screener?country=United%20States&exchange=nasdaq&letter=0&render=download")
button = driver.find_elements_by_class_name("nasdaq-screener__form-button--download")
button[0].click()
print(driver.title)
time.sleep(2)
# For nyse
driver.get("https://www.nasdaq.com/market-activity/stocks/screener?country=United%20States&exchange=nyse&letter=0&render=download")
button = driver.find_elements_by_class_name("nasdaq-screener__form-button--download")
button[0].click()
time.sleep(2)
# For amex
driver.get("https://www.nasdaq.com/market-activity/stocks/screener?country=United%20States&exchange=amex&letter=0&render=download")
button = driver.find_elements_by_class_name("nasdaq-screener__form-button--download")
button[0].click()
# capture the screen
driver.get_screenshot_as_file("capture.png")
driver.close()