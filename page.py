from selenium.common.exceptions import TimeoutException

from element import BasePageElement
from locator import SearchPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


class SearchElement(BasePageElement):
    locator = 'q'


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def __exit__(self, driver):
        self.driver.close()


class MainPage(BasePage):
    search_text_element = SearchElement()

    def adjust_cookies(self):
        adjust_cookies_button = self.driver.find_element(*SearchPageLocators.ADJUST_COOKIES_BUTTON)
        adjust_cookies_button.click()
        personalize_search_disable = self.driver.find_element(*SearchPageLocators.PERSONALIZE_SEARCH_DISABLE_BUTTON)
        personalize_youtube_history_disable = self.driver.find_element(*SearchPageLocators.
                                                                       PERSONALIZE_YOUTUBE_DISABLE_BUTTON)
        personalize_adverts_disable = self.driver.find_element(*SearchPageLocators.PERSONALIZE_ADVERTS_DISABLE_BUTTON)
        personal_settings_confirm_button = self.driver.find_element(
            *SearchPageLocators.PERSONAL_SETTINGS_CONFIRM_BUTTON)

        cookies_buttons = [personalize_search_disable, personalize_youtube_history_disable,
                           personalize_adverts_disable, personal_settings_confirm_button]

        for button in cookies_buttons:
            button.click()

    def is_title_google(self):
        return "Google" == self.driver.title

    def is_empty_phrase_searched(self):
        not_searched = False

        self.adjust_cookies()
        search_box = self.driver.find_element(By.NAME, 'q')
        empty_phrase = "    "
        search_box.click()
        search_box.send_keys(empty_phrase)
        search_box.send_keys(Keys.ENTER)

        if self.driver.title == "Google":
            not_searched = True

        return not_searched

    def is_tooltip_correct(self):

        expected_tooltip = ['Wyszukiwanie głosowe', 'Voice search']  # should be checked against different locale
        self.adjust_cookies()
        voice_search_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[3]')
        hover = ActionChains(self.driver).move_to_element(voice_search_button).perform()
        tooltip = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]')))\
            .text
        return tooltip in expected_tooltip

    def is_image_displayed(self):
        self.adjust_cookies()
        google_image = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/img')))
        return google_image.is_displayed()

    def is_padding_size_correct(self):
        upper_pad = '5px'
        right_pad = '8px'
        bottom_pad = '0px'
        left_pad = '14px'
        search_bar_expected_padding = [upper_pad, right_pad, bottom_pad, left_pad]

        self.adjust_cookies()
        search_bar_actual_padding = (self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div').value_of_css_property("padding")).split()

        return search_bar_expected_padding == search_bar_actual_padding

    def is_site_search_working(self):

        self.adjust_cookies()
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

