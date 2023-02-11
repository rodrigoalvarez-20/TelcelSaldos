from selenium import webdriver
from time import sleep
from utils.configs import get_config
import platform
import os

def select_binary():
    if platform.system() == "Windows":
        binary_path = "{}/bin/windows/chromedriver.exe".format(os.getcwd())
        return os.path.abspath(binary_path)
    elif platform.system() == "Linux":
        return "/usr/bin/chromedriver"
    elif platform.system() == "Darwin":
        return "/usr/local/bin/chromedriver"
    


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    #options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options, executable_path=select_binary())
    

def obtain_token(driver):
    WEB_URL = get_config("SALDOS", "WEB_URL")
    FRAME_URL = get_config("SALDOS", "TOKEN_FRAME")
    
    driver.get(WEB_URL)
    sleep(5)
    driver.get(FRAME_URL)
    sleep(5)

    return driver.execute_script("return sessionStorage.getItem('token')")
    

if __name__ == "__main__":
    drv = start_driver()

    print(obtain_token(drv))

