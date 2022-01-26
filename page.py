from selenium.common.exceptions import TimeoutException

from element import BasePageElement
from locator import SearchPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class SearchElement(BasePageElement):
    locator = 'q'


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def __exit__(self, driver):
        self.driver.close()


class MainPage(BasePage):
    search_text_element = SearchElement()

    def is_title_google(self):
        return "Google" == self.driver.title

    def is_site_search_working(self):

        adjust_cookies_button = self.driver.find_element(*SearchPageLocators.ADJUST_COOKIES_BUTTON)
        adjust_cookies_button.click()
        personalize_search_disable = self.driver.find_element(*SearchPageLocators.PERSONALIZE_SEARCH_DISABLE_BUTTON)
        personalize_youtube_history_disable = self.driver.find_element(*SearchPageLocators.
                                                                       PERSONALIZE_YOUTUBE_DISABLE_BUTTON)
        personalize_adverts_disable = self.driver.find_element(*SearchPageLocators.PERSONALIZE_ADVERTS_DISABLE_BUTTON)
        personal_settings_confirm_button = self.driver.find_element(*SearchPageLocators.PERSONAL_SETTINGS_CONFIRM_BUTTON)

        cookies_buttons = [personalize_search_disable, personalize_youtube_history_disable,
                           personalize_adverts_disable, personal_settings_confirm_button]

        for button in cookies_buttons:
            button.click()

        search_box = self.driver.find_element(By.NAME, 'q')
        phrase_to_be_searched = "site:wikipedia.org java"
        search_box.click()
        search_box.send_keys(phrase_to_be_searched)
        search_box.send_keys(Keys.ENTER)

        searched_links_on_page = []
        for i in range(1, 10):
            timeout = 5
            try:
                search_result = WebDriverWait(self.driver, timeout) \
                    .until(EC.presence_of_all_elements_located((By.XPATH,
                                                                "//*[@id=\"rso\"]/div[{}]/div/div[1]/div/a".format(i))))
                links_in_search_result = [elem.get_attribute('href') for elem in search_result]
                searched_links_on_page.append(links_in_search_result)
            except TimeoutException:
                print("Timeout while looking for 'href' element")

        searched_correctly = True
        for links_in_search_result in searched_links_on_page:
            for link in links_in_search_result:
                if "wikipedia.org" not in link:
                    searched_correctly = False

        return searched_correctly

