from selenium import webdriver
from funcs import *

driver = webdriver.Chrome()
driver.implicitly_wait(5)

login(driver)
driver.find_element_by_class_name("_avvq0")
open_article(driver)

driver.get(driver.find_element_by_class_name("_2g7d5").get_attribute('href'))
driver.find_elements_by_class_name("_t98z6")[1].click()

users = []
followers = driver.find_elements_by_class_name("_2g7d5")
for follower in followers:
    users.append(follower.get_attribute('href'))

likes_users(driver, users)

driver.quit()