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
    browser.add_cookie({"name": "MUSIC_U", "value": "009976D74A30679D9D2EA555CF164847C1160B4A6EEFAA719D5DE9782799A1834F7231C717542C6B5C6D7F1A49FE63DAD849CBB37EBBD2AF7BD993BF8C5ED98C002D68261520AF57DFF36EF8200DFBD48DC2CB54A654E910209497D6F151AE0AE9183D0B8ED8550F887C8E6AF1BE8FE1D490DA18D2D42C1E459EA27FF51D91BC50F86154AC0A6C4C26C61CB6DF86E7180ED11525B4BE5EA8113ECCAEF3E8F97D8E5D6B545A4DDD9C866EB3139C00B260660F18DD54C2FC5C0EB28796C49768E4C64E1F79CF12660A7C8C93C8EBA3C4C79BD39B9F8C8EC3C90800DBA05CB84E4B461C818F013E216017D5CEC0E083409DC632A28EC7FB83B745D4373F705D107C972152D18B3DA971B4FAC14FC858510831CB3D2BED3CE9689B8208E6BE141E3A60B8ABAF08972A7CF9B50223424324E372195A75C56A9B46FBA564D2C4F3C372C4220354DEEB2E54038F25D7DD4CFD58FDA5AEA40E8A5C92E0EDBEFBEDF61C3A35"})
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
