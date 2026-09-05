from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
website = r"'Replace With Your Path'\STT_server.html"

driver.get(website)


def TTS():
    print("LISTENING ... ")
    driver.find_element(by=By.ID, value='start').click()
    while 1:
        if driver.find_element(by=By.ID, value='output').text != "":
            a = driver.find_element(by=By.ID, value='output').text
            driver.find_element(by=By.ID, value='end').click()
            return a
