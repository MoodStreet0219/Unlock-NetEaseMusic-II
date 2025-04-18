# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00E4B94E3EEDF45F07E8E55C755AB69B7BB4996BE5008A3802D8C35AA2D117C4D2DEEBCD304FE5D80EC0C8478E1F8AA484AFC7078E801A960795BBA5CB7A61A3C39BFDA77C32CA662030CE45963286AE0B035450E4D2983B31D25D950284D4C5033775BC86F77BC5385B46554780F27DA2AF1F8251449F5D30C738C463375A671447E2EAA920A111643F3D31B1C6B0F74BFD9E05BC61D94512150269BCC1E7FF584CAB7161B959E29D3582F026204265FB75D5EEC526F384B6CB287B48887C68DD6222EAFF5E198A29D13A65C25BB53EBF0C848BB5381D2474781CF8841A409F2309D008E1FE7EBF438F29C175E6F9BFEB1D5A66D90FDFEC5E136AD0BFEBA3418D0D4A3C1D48BE18EE767FA40231F854952E9519D894883354A5AC240DB1CEF6C9B603DD059789E9B0251E488B6523847B07F308E0F89D4608B833C9C2DFB9935A45515543553A8596B7E693BFF48CA53539E8A86F8F9557D88FD182952E82EB62"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
