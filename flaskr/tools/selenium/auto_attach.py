from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
# 1. open a driver
# driver = webdriver.Chrome()  #python
# options.browser_version = '92'
# options.platform_name = 'Windows 10'
# caps['version'] = '92'
# caps['build'] = my_test_build
# caps['name'] = my_test_name
# options.set_capability(caps)
# driver = webdriver.Chrome(options=options)
# 2. extract to session_id and _url from driver object.
# url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
# session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
# 3. Use these two parameter to connect to your driver.
options = Options()
options.add_experimental_option("detach", True)
url = "http://localhost:9515"
# capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote(command_executor=url, options=options)
# this prevents the dummy browser
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
    print(driver.current_url)
    driver.session_id = new_session_id
    driver.close()
    driver.session_id = session_id
except:
    driver.session_id = new_session_id
    driver.get("https://www.neuralnine.com/")
    with open(FILE_NAME, "w") as f:
        f.write(driver.session_id)
print(driver.session_id)

# testing
driver.maximize_window()
links = driver.find_elements("xpath", "//a[@href]")
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break
