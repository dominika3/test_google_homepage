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

    def search_phrase(self, phrase):
        search_box = self.driver.find_element(By.NAME, 'q')
        phrase_to_be_searched = phrase
        search_box.click()
        search_box.send_keys(phrase_to_be_searched)
        search_box.send_keys(Keys.ENTER)

    def check_if_searched_correctly(self, searched_file_type):
        result_file_types = []
        self.adjust_cookies()
        self.search_phrase("filetype:" + searched_file_type + " software testing")

        xpath_random_search_results = ['//*[@id="rso"]/div[4]/div/div/div[1]/div/div[2]/span[2]',
                                       '//*[@id="rso"]/div[8]/div/div/div[1]/div/div[2]/span[2]',
                                       '//*[@id="rso"]/div[5]/div/div/div[1]/div/div[2]/span[2]']

        for xpath in xpath_random_search_results:
            timeout = 10
            try:
                file_type = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))).text
                result_file_types.append(file_type)
            except TimeoutException:
                print("Timeout while looking for specified file type")

        searched_correctly_list = [result_type in searched_file_type for result_type in
                                   result_file_types]  # in  to match searched e.g 'docx' with found 'doc' filetype
        return all(el is True for el in searched_correctly_list)

    def is_specific_type_searched_correctly(self, file_type):
        result_file_types = []
        self.search_phrase("filetype:" + file_type + " software testing")

        xpath_random_search_results = ['//*[@id="rso"]/div[4]/div/div/div[1]/div/div[2]/span[2]',
                                       '//*[@id="rso"]/div[8]/div/div/div[1]/div/div[2]/span[2]',
                                       '//*[@id="rso"]/div[5]/div/div/div[1]/div/div[2]/span[2]']

        for xpath in xpath_random_search_results:
            timeout = 3
            try:
                file_type = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))).text
                result_file_types.append(file_type)
            except TimeoutException:
                result_file_types.append(None)
                print("Timeout while looking for specified file type")

        searched_correctly_list = [result_type == file_type for result_type in
                                   result_file_types]
        self.driver.find_element(By.NAME, 'q').clear()

        return all(el is True for el in searched_correctly_list)

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

    def is_button_displayed_when_window_resized(self):
        self.adjust_cookies()
        search_in_google_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
        is_every_res_displayed = []

        resolutions = [(1920, 1080), (1280, 720), (900, 600)]
        for resolution in resolutions:
            self.driver.set_window_size(*resolution)
            is_displayed = search_in_google_button.is_displayed()
            is_every_res_displayed.append(is_displayed)
        return all(el is True for el in is_every_res_displayed)

    def is_padding_size_correct(self):
        upper_pad = '5px'
        right_pad = '8px'
        bottom_pad = '0px'
        left_pad = '14px'
        search_bar_expected_padding = [upper_pad, right_pad, bottom_pad, left_pad]

        self.adjust_cookies()
        search_bar_actual_padding = (self.driver.find_element(By.XPATH,
                                                              '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div')
                                     .value_of_css_property("padding")).split()

        return search_bar_expected_padding == search_bar_actual_padding

    def is_searched_filetype_correct(self):

        file_types = ['pdf', 'doc', 'xlsx']
        result_for_all_types = []

        self.adjust_cookies()
        for file_type in file_types:
            result = self.is_specific_type_searched_correctly(file_type)
            if result is False:
                return False
            result_for_all_types.append(result)

        return all(el is True for el in result_for_all_types)


    def is_site_search_working(self):

        self.adjust_cookies()
        self.search_phrase("site:wikipedia.org java")

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


