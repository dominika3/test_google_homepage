from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import unittest
import page

class GoogleHomepage(unittest.TestCase):

    def setUp(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        serv = Service(PATH)
        self.driver = webdriver.Chrome(service=serv)
        self.driver.get("https://google.com")

    def test_page_title(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_title_google()

    def test_empty_phrase_not_searched(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_empty_phrase_searched()

    def test_hover_over_text(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_tooltip_correct()

    def test_google_image_displayed(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_image_displayed()

    def test_button_displayed_if_window_resized(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_button_displayed_when_window_resized()

    def test_padding_around_search_bar(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_padding_size_correct()

    def test_filetype_search(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_searched_filetype_correct()

    def test_site_search(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_site_search_working()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

