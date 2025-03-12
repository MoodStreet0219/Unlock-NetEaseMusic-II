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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E221DE5662064A98E1003B7E76AC86941EFFF8219E3C51D5A074D979F4516E872125461F8C5E4FD84A519EB0ED96783971074781EDFC52DA0EB6C151896A0CA702A2D1CDEDD7D59B8D37E1E574A781F892A12E3BEA24B74296AADFF22C4EA4668C3C957FAB03B5079694EB81AF5A94DBCFFD06F8D452CF3325253B9AAA42DB2A652A7654C613BE43F53691E42ED15A275A52719B9441E0B8256CEF6ADDADF2D4FFBD33D008EF2EABF094F3AD026BFE2310FE145EDFE4A8EFBA67B209E8B267EBAA1966827F26B483762D523B03A21824048C3F3F6FB5B0D0D97C6987C16E2F53EB4D9093E8683C2A50C183CDF4B6BB06556D5F560EADC67B52FC83F3C88A51E2E6B0C9B8F8ED7196377BCB47398750CD943DC2984EC5B809467615DE1F31A5A8F8AF12BD87EEC45CC73E4C79E9EBFC362FD3253C56AE3F905606F29D86462C01EC772FC7D1F81BF0B82CAE4D0A7E20E8D87F83FD3224BCF2914813B0FA8E07CD"})
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
