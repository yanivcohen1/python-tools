from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# testing
driver.get("https://www.w3schools.com/html/html_tables.asp")
driver.maximize_window()
# driver.find_element(By.CSS_SELECTOR, "a[href='https://www.neuralnine.com/books/']").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Books").click()
table_id = driver.find_element(
    By.CSS_SELECTOR,
    "#customers",
)
# table_id = driver.find_element(By.ID, 'data_configuration_feeds_ct_fields_body0')
rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
# head = rows[0].text.split(" ")
is_head = True
for i, row in enumerate(rows):
    if is_head:
        cols = row.find_elements(By.TAG_NAME, "th")
    else:
        cols = row.find_elements(By.TAG_NAME, "td")
    for col in cols:
        print('%30s' % col.text, ",", end=" ")  # prints text from the element
    if is_head:
        print("\n----------------------------------------------------------------------------------------------------")
        is_head = False
    else:
        print()

