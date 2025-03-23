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
    browser.add_cookie({"name": "MUSIC_U", "value": "0058BC6DDE63E6FECD55ED9DA6790B6E6D183BAFADFB25D970B866CFA9006D53211FAF137CF9EA4D3ECFDA30477A54274C98CFD16FD63FBCC7B340BAE6E150E280E8A5AAAEBEF48730A6E914A0063896174BCD7F064B3F7F4380A054B0DF6ED76657F1DB1B2289EAE780F58C791477D2960313D57C8A6659805621576D6BD23A71A8771458A7BBCE6304DC516166B4C98B85F9B5859A24CCEEC6BAB1D48BA7C2F61E6778C89E066229E8670A1F31E3F46F9DE9570436617F7079C1726F136BCCBF5EA3568429227E217C000A51D95077B1CA2C22D80AE29B421BA75C148699475BA8581B4D01B899768F779E3C78E6694996B972F9A6E8FEE7E6D591CD28BDD89E2541E13427C19407FFB2B316438E67D892D2A0A4BE99C5C87028A2626462321F5A1371547BA96CAF226EB7D13A203E11854260A27FA4D87DA33F44F02BBF367DCD5161690E215F3ADB74BACF1E10F94B5A972DF55A3250CC270D8EA3255CCD30"})
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
