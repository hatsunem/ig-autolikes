from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import gmailreceiver

INSTA_URL = "https://www.instagram.com/accounts/login/"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
TAG = "TAG"

options = Options()
# options.add_argument('--headless')
# options.binary_location = '/app/.apt/usr/bin/google-chrome'
driver = Chrome(chrome_options=options)
driver.implicitly_wait(5)


def login():
    driver.get(INSTA_URL)

    email = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    email.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    login_button = driver.find_element_by_class_name("_qv64e")
    login_button.submit()

    try:
        driver.find_element_by_class_name("_avvq0")
    except NoSuchElementException:
        print("アカウント認証")
        send_button = driver.find_element_by_class_name("_qv64e")
        send_button.submit()
        code_form = driver.find_element_by_name("security_code")
        code = gmailreceiver.get_code()
        code_form.send_keys(code)
        code_button = driver.find_element_by_class_name("_qv64e")
        code_button.submit()
    finally:
        driver.find_element_by_class_name("_avvq0")
        print("ログイン完了")


def open_article():
    driver.get("https://www.instagram.com/explore/tags/" + TAGS[0] + "/")
    articles = driver.find_elements_by_class_name("_6d3hm")
    article = articles[3].find_elements_by_class_name("_mck9w")
    actions = ActionChains(driver)
    actions.move_to_element(articles[4])
    actions.perform()
    article[0].click()


def likes_users(users):
    likes = 0
    for user in users:
        driver.get(user)
        try:
            driver.find_element_by_class_name("_mck9w").click()
            for num in range(3):
                driver.find_element_by_class_name("coreSpriteHeartOpen").click()
                likes += 1
                sleep(1)
                driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        except NoSuchElementException:
            pass

    return likes


def get_users():
    users = []
    while len(users) < 10:
        try:
            address = driver.find_element_by_class_name("_2g7d5").get_attribute('href')
            if address not in users:
                users.append(address)
            driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        except (NoSuchElementException, StaleElementReferenceException):
            open_article()

    return users
