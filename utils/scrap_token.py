from selenium import webdriver
from time import sleep
from utils.configs import get_config
import platform
import os

def select_binary():
    if platform.system() == "Windows":
        binary_path = "{}/bin/windows/chromedriver.exe".format(os.getcwd())
    else:
        binary_path = "{}/bin/linux/chromedriver".format(os.getcwd())
    return os.path.abspath(binary_path)


def scrap_token():
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    #options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options, executable_path=select_binary())
    WEB_URL = get_config("SALDOS", "WEB_URL")
    FRAME_URL = get_config("SALDOS", "TOKEN_FRAME")
    driver.get(WEB_URL)
    sleep(5)
    driver.get(FRAME_URL)
    sleep(5)
    return driver.execute_script("return sessionStorage.getItem('token')")


#def validate_token_in_db(db_conn):
    

if __name__ == "__main__":
    print("Token obtenido: {}".format(scrap_token()))

