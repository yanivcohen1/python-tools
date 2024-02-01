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
driver.get("https://www.neuralnine.com/")
driver.maximize_window()
# driver.find_element(By.CSS_SELECTOR, "a[href='https://www.neuralnine.com/books/']").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Books").click()
links = driver.find_elements(By.XPATH, "//a[@href]")
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break
