from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import unittest
import page
from selenium.webdriver.common.by import By


class GoogleHomepage(unittest.TestCase):

    def setUp(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        serv = Service(PATH)
        self.driver = webdriver.Chrome(service=serv)
        self.driver.get("https://google.com")



    # def test_search_title(self):
    #     main_page = page.MainPage(self.driver)
    #     assert main_page.is_title_google()

    def test_site_search(self):
        main_page = page.MainPage(self.driver)
        assert main_page.is_site_search_working()


    def tearDown(self):
        self.driver.quit()



if __name__ == "__main__":
    unittest.main()

