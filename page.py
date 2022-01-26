from element import BasePageElement
from locator import MainPageLocators
from locator import SearchResultsPageLocators
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
        adjust_button = self.driver.find_element(By.ID, "VnjCcb")
        adjust_button.click()
        disable_features_buttons = self.driver.find_elements(By.CLASS_NAME, "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc S82sre")

        for button in disable_features_buttons:
            button.click()

        confirm_button = self.driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc XICXwf")
        confirm_button.click()


        # search_element = self.driver.find_element(By.NAME, 'q')
        # self.driver.implicitly_wait(15)
        # search_element.click()
        # search_text_element = "site:wikipedia.org java"
        # search_element.send_keys(search_text_element)
        # search_element.send_keys(Keys.ENTER)
        # result_link = self.driver.find_element(SearchResultsPageLocators.LINK_LOCATOR)
        # assert "wikipedia.org" in result_link

