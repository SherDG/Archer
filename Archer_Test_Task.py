from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
import time

SELENIUM_CHROME_DRIVER_PATH = 'D:/../PATH TO YOUR CHROME DRIVER/../chromedriver.exe'
login='YOUR LOGIN'
password='YOUR PASSWORD'

class FriendsPage:
    LOGIN_URL = 'https://www.facebook.com/login.php'
    SCROLL_PAUSE_TIME = 3
    WAIT_LOADING_ELEMENTS = 20

    def __init__(self, login, password):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values.notifications': 2}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path=SELENIUM_CHROME_DRIVER_PATH, options=options)
        self.wait = WebDriverWait(self.driver, self.WAIT_LOADING_ELEMENTS)
        self.login(login, password)

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()

        # wait for the main page to load
        self.wait = WebDriverWait(self.driver, self.WAIT_LOADING_ELEMENTS)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a#findFriendsNav')))

    def navigateToFriendsPage(self):
        self.driver.find_element_by_xpath('//div[contains(@data-click, "profile_icon")]').click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@data-tab-key, "friends")]')))
        self.driver.find_element_by_xpath('//a[contains(@data-tab-key, "friends")]').click()

    def getBodyScrollHeight(self):
        return self.driver.execute_script('return document.body.scrollHeight')

    def scrollBodyTo(self, height):
        self.driver.execute_script('window.scrollTo(0, %s);' % height)

    def getNumberFriendsElemets(self):
        return len(self.driver.find_elements_by_xpath('//div[contains(@data-testid, "friend_list_item")]'))

    def getFriendsNumber(self):
        self.navigateToFriendsPage()
        # Get scroll height
        last_height = self.getBodyScrollHeight()
        while True:
            # Scroll down to bottom
            self.scrollBodyTo(last_height)

            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.getBodyScrollHeight()
            isEndOfPage = new_height == last_height
            if isEndOfPage:
                return self.getNumberFriendsElemets()
            last_height = new_height

    def closeBrowser(self):
        self.driver.close()

if __name__ == '__main__':
    crawler = FriendsPage(login, password)


    print(crawler.getFriendsNumber())
    crawler.closeBrowser()
