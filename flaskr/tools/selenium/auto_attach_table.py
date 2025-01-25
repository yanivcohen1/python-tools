from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import json
# you need first to run the chrome driver in cmd (.\chromedriver.exe)

# 1. open a driver
# driver = webdriver.Chrome(options=options)
# 2. extract to session_id and _url from driver object.
# url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
# session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
# 3. Use these two parameter to connect to your driver.
dir_path = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = dir_path + "\\session_id.txt"
# port = 1914
# my_list = ['1', port]
# with open(FILE_NAME, 'w') as file:
#     json.dump(my_list, file) # ["1", 1914]
with open(FILE_NAME, "r") as f:
    load = json.load(f)
session_id, port = load
options = Options()
options.add_experimental_option("detach", True)
url = "http://localhost:" + str(port)
driver = webdriver.Remote(command_executor=url, options=options)
# 4. And you are connected to your driver again.
new_session_id = driver.session_id
driver.session_id = session_id
try:
    driver.get("https://www.w3schools.com/html/html_tables.asp")
    print(driver.current_url)
    driver.session_id = new_session_id
    # this prevents the dummy browser
    driver.close()
    driver.session_id = session_id
except:
    driver.session_id = new_session_id
    driver.get("https://www.w3schools.com/html/html_tables.asp")
    with open(FILE_NAME, "w") as f:
        json.dump([new_session_id, port], f)
print(driver.session_id)

# testing
#   driver.maximize_window()
# driver.find_element(By.CSS_SELECTOR, "a[href='https://www.neuralnine.com/books/']").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Books").click()
table_id = driver.find_element(
    By.CSS_SELECTOR,
    "#customers",
)
# table_id = driver.find_element(By.ID, 'data_configuration_feeds_ct_fields_body0')
rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
# head = rows[0].text.split(" ")
head = True
for i, row in enumerate(rows):
    if head:
        cols = row.find_elements(By.TAG_NAME, "th")
    else:
        cols = row.find_elements(By.TAG_NAME, "td")
    for col in cols:
        print(f'{col.text:>30} ,', end=" ")  # cell string should be right-aligned (>) and take up 30 characters in width
    if head:
        print("\n----------------------------------------------------------------------------------------------------")
        head = False
    else:
        print()
