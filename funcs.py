from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import gmailreceiver

INSTA_URL = "https://www.instagram.com/accounts/login/"


class InstaOperator:
    def __init__(self, username, password, tag):
        self.username = username
        self.password = password
        self.tag = tag

        options = Options()
        # options.add_argument('--headless')
        # options.binary_location = '/app/.apt/usr/bin/google-chrome'
        self.driver = Chrome(chrome_options=options)
        self.driver.implicitly_wait(5)

    def login(self):
        self.driver.get(INSTA_URL)
        email_form = self.driver.find_element_by_name("username")
        password_form = self.driver.find_element_by_name("password")
        email_form.send_keys(self.username)
        password_form.send_keys(self.password)

        login_button = self.driver.find_element_by_class_name("_5f5mN")
        login_button.submit()

        try:
            self.driver.find_element_by_class_name("XTCLo")
        except NoSuchElementException:
            print("アカウント認証")
            send_button = self.driver.find_element_by_class_name("_5f5mN")
            send_button.submit()
            code_form = self.driver.find_element_by_name("security_code")
            code = gmailreceiver.get_code()
            code_form.send_keys(code)
            code_button = self.driver.find_element_by_class_name("_5f5mN")
            code_button.submit()
            try:
                self.driver.find_element_by_class_name("XTCLo")
            except NoSuchElementException as e:
                print("ログイン失敗")
                print(type(e))
                print(str(e))
            else:
                print("ログイン完了")
        else:
            print("ログイン完了")

    def open_article(self):
        self.driver.get("https://www.instagram.com/explore/tags/" + self.tag + "/")
        articles = self.driver.find_elements_by_class_name("Nnq7C")
        article = articles[3].find_elements_by_class_name("v1Nh3")
        actions = ActionChains(self.driver)
        actions.move_to_element(articles[4])
        actions.perform()
        article[0].click()

    def get_users(self):
        users = []
        while len(users) < 10:
            try:
                address = self.driver.find_element_by_class_name("nJAzx").get_attribute('href')
                if address not in users:
                    users.append(address)
                self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            except (NoSuchElementException, StaleElementReferenceException):
                self.open_article()

        return users

    def likes_users(self, users):
        likes = 0
        for user in users:
            self.driver.get(user)
            try:
                self.driver.find_element_by_class_name("v1Nh3").click()
                for num in range(3):
                    self.driver.find_element_by_class_name("coreSpriteHeartOpen").click()
                    likes += 1
                    sleep(1)
                    self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            except NoSuchElementException:
                pass

        return likes
