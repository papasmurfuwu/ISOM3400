from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

def launchBrowser():
# Boilerplate code to get Chrome not shutting down
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.google.com")
    driver.find_element("class name", "gLFyf")

    search_box = driver.find_element("name", "q")
    search_box.clear()
    search_box.send_keys("us election 2020", Keys.RETURN)

launchBrowser()



