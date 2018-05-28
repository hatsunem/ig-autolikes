from selenium import webdriver
from funcs import *

driver = webdriver.Chrome()
driver.implicitly_wait(10)

login(driver)

# プロフィールページへ移動し、最新投稿のいいね一覧を開く
driver.find_element_by_class_name("coreSpriteDesktopNavProfile").click()
driver.find_element_by_class_name("_mck9w").click()
driver.find_element_by_class_name("_nzn1h").click()

users = driver.find_elements_by_class_name("_2g7d5")
adresses = []
for user in users:
    adresses.append(user.get_attribute('href'))

# 各ユーザのページにアクセス
for address in adresses:
    driver.get(address)
    driver.find_element_by_class_name("_mck9w").click()
    try:
        driver.find_element_by_class_name("coreSpriteHeartOpen").click()
        sleep(5)
    except NoSuchElementException:
        pass

driver.quit()