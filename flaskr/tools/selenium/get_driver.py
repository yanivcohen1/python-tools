import socket
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# you need first to run the chrome driver in cmd (.\chromedriver.exe --port=5000)
def connect_to_driver():
    options = Options()
    options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(options=options)
    url = "http://127.0.0.1:5000" # driver.command_executor._url
    options.add_experimental_option("detach", True)
    driver = webdriver.Remote(command_executor=url, options=options)
    session_id = ""
    # 4. And you are connected to your driver again.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    FILE_NAME = dir_path + "\\session_id.txt"
    with open(FILE_NAME, "r") as f:
        session_id = f.read()
    new_session_id = driver.session_id
    driver.session_id = session_id
    try:
        # driver.get("https://www.neuralnine.com/")
        url = driver.current_url
        driver.session_id = new_session_id
        # this prevents the dummy browser
        driver.close()
        driver.session_id = session_id
    except:
        driver.session_id = new_session_id
        with open(FILE_NAME, "w") as f:
            f.write(driver.session_id)
    url = driver.current_url
    print(driver.session_id)
    return driver

if __name__ == "__main__":
    driver = connect_to_driver()
    driver.get("https://google.com/")
