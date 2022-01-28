from selenium.common.exceptions import TimeoutException
from locator import SearchPageLocators
from locator import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):

    def adjust_cookies(self):
        adjust_cookies_button = self.driver.find_element(*MainPageLocators.ADJUST_COOKIES_BUTTON)
        adjust_cookies_button.click()
        personalize_search_disable = self.driver.find_element(*MainPageLocators.PERSONALIZE_SEARCH_DISABLE_BUTTON)
        personalize_youtube_history_disable = self.driver.find_element(*MainPageLocators.
                                                                       PERSONALIZE_YOUTUBE_DISABLE_BUTTON)
        personalize_adverts_disable = self.driver.find_element(*MainPageLocators.PERSONALIZE_ADVERTS_DISABLE_BUTTON)
        personal_settings_confirm_button = self.driver.find_element(
            *SearchPageLocators.PERSONAL_SETTINGS_CONFIRM_BUTTON)

        cookies_buttons = [personalize_search_disable, personalize_youtube_history_disable,
                           personalize_adverts_disable, personal_settings_confirm_button]

        for button in cookies_buttons:
            button.click()

    def search_phrase(self, phrase):
        search_box = self.driver.find_element(By.NAME, 'q')
        phrase_to_be_searched = phrase
        search_box.click()
        search_box.send_keys(phrase_to_be_searched)
        search_box.send_keys(Keys.ENTER)

    def is_title_google(self):
        return self.driver.title == "Google"

    def is_empty_phrase_searched(self):
        not_searched = False
        self.adjust_cookies()
        self.search_phrase("    ")

        if self.driver.title == "Google":  # if page title is still "Google" search wasn't performed for empty string
            not_searched = True
        return not_searched

    def is_tooltip_correct(self):
        expected_tooltip = ["Wyszukiwanie głosowe", "Voice search"]  # should be checked against different locale
        self.adjust_cookies()
        voice_search_button = self.driver.find_element(*MainPageLocators.VOICE_SEARCH_BUTTON)
        ActionChains(self.driver).move_to_element(voice_search_button).perform()
        tooltip = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(MainPageLocators.
                                                                                      VOICE_SEARCH_TOOLTIP)).text
        return tooltip in expected_tooltip

    def is_google_image_displayed(self):
        self.adjust_cookies()
        google_image = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(MainPageLocators.
                                                                                           GOOGLE_IMAGE))
        return google_image.is_displayed()

    def is_button_displayed_when_window_resized(self):
        resolutions = [(1920, 1080), (1280, 720), (900, 600)]
        are_resolutions_displayed = []
        self.adjust_cookies()
        search_in_google_button = self.driver.find_element(*MainPageLocators.SEARCH_IN_GOOGLE_BUTTON)

        for resolution in resolutions:
            self.driver.set_window_size(*resolution)
            is_displayed = search_in_google_button.is_displayed()
            are_resolutions_displayed.append(is_displayed)
        return all(are_resolutions_displayed)

    def is_padding_size_correct(self):
        upper_pad = '5px'
        right_pad = '8px'
        bottom_pad = '0px'
        left_pad = '14px'
        search_bar_expected_padding = [upper_pad, right_pad, bottom_pad, left_pad]
        self.adjust_cookies()
        search_bar_actual_padding = (self.driver.find_element(*MainPageLocators.SEARCH_BAR_WITH_PADDING)
                                     .value_of_css_property("padding")).split()

        return search_bar_expected_padding == search_bar_actual_padding


class SearchPage(BasePage):

    def check_if_searched_correctly(self, searched_file_type):
        main_page = MainPage(self.driver)
        result_file_types = []
        main_page.adjust_cookies()
        main_page.search_phrase("filetype:" + searched_file_type + " software testing")

        xpath_random_search_results = ['//*[@id="rso"]/div[4]/div/div/div[1]/div/div[2]/span[2]',
                                       '//*[@id="rso"]/div[8]/div/div/div[1]/div/div[2]/span[2]',
                                       '//*[@id="rso"]/div[5]/div/div/div[1]/div/div[2]/span[2]']

        for xpath in xpath_random_search_results:
            timeout = 10
            try:
                file_type = WebDriverWait(self.driver, timeout).until(
                    ec.presence_of_element_located((By.XPATH, xpath))).text
                result_file_types.append(file_type)
            except TimeoutException:
                print("Timeout while looking for specified file type")

        searched_correctly_list = [result_type in searched_file_type for result_type in
                                   result_file_types]  # in  to match searched e.g 'docx' with found 'doc' filetype
        return all(el is True for el in searched_correctly_list)

    def is_specific_type_searched_correctly(self, file_type):
        main_page = MainPage(self.driver)
        result_file_types = []
        main_page.search_phrase("filetype:" + file_type + " software testing")

        xpath_random_search_results = [SearchPageLocators.FILETYPE_SEARCH_RESULT_3,
                                       SearchPageLocators.FILETYPE_SEARCH_RESULT_4,
                                       SearchPageLocators.FILETYPE_SEARCH_RESULT_6]

        for xpath in xpath_random_search_results:
            timeout = 10
            try:
                file_type = WebDriverWait(self.driver, timeout).until(
                    ec.presence_of_element_located(xpath)).text
                result_file_types.append(file_type)
            except TimeoutException:
                result_file_types.append(None)
                print("Timeout while looking for specified file type")

        searched_correctly_list = [result_type == file_type for result_type in
                                   result_file_types]

        self.driver.find_element(By.NAME, 'q').clear()  # clear to be able to search for new file type

        return all(searched_correctly_list)

    def is_searched_filetype_correct(self):
        main_page = MainPage(self.driver)
        file_types = ['pdf', 'doc', 'xlsx']
        main_page.adjust_cookies()
        for file_type in file_types:
            result = self.is_specific_type_searched_correctly(file_type)
            if result is False:
                return False
        return True

    def is_site_search_working(self):
        main_page = MainPage(self.driver)
        searched_links_on_page = []
        main_page.adjust_cookies()
        main_page.search_phrase("site:wikipedia.org java")

        for i in range(1, 10):
            timeout = 5
            try:
                search_result = WebDriverWait(self.driver, timeout) \
                    .until(ec.presence_of_element_located((By.XPATH,
                                                           "//*[@id=\"rso\"]/div[{}]/div/div[1]/div/a".format(i))))
                searched_links_on_page.append(search_result.get_attribute('href'))
            except TimeoutException:
                print("Timeout while looking for 'href' element")

        return all([True for link in searched_links_on_page if "wikipedia.org" in link])
