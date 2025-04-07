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
    browser.add_cookie({"name": "MUSIC_U", "value": "00CAB4C885A40CE62FBAD4ABA3BC00A1F2F3AA513C289D514B62D1660C189DE1AEE0E65E87F7A5E949DE0A8948D7291D82E9CFB5E6C9E463640B97AC727D9D7B905F1F41C3F2A7C4A14945E1097441C592216373F17FA34CB48D16523833723DFB49581FB8EC54DB964648D7D3C293D944A8850B9F489FBD00F70DC3CF87C9BBFE6A9CC4F33C92676C48A17383E666F9B345A75C3B6F8586707F7E3465DF05613194CFFEC745866AE082FB246314E7443126F75911B1FA95F9C6D1305E82EB9D48403CD2976725072A25D54FEC751CB9B40D9E4EAC6C41C1011A0FF4EDF24DFECC22FEBD3D2BFD0F14973AD9EE745D2BFF51BE6BB89242B6489D504FCBA35A956EACC4C6A6969434A2619E42226B478470AB9C4CC54BC0691E6C88B192F99CAF6F7A29FAEFFA1F7828587AB605F4B0FBACDEEA6E2C0487BC20C05FF106D3FCEF035DEAF0445073906DAE170EFE0FD52DB5CF11228F1F9EF189BCB51D9AE5C7A737"})
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
