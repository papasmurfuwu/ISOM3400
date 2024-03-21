from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

def launchBrowser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://google.com")
    input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
    input_element.send_keys("tech with tim" + Keys.ENTER)
    return driver

launchBrowser()