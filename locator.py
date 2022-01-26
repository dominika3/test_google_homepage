from selenium.webdriver.common.by import By


class MainPageLocators(object):
    SEARCH_ELEMENT = (By.ID, 'q')


class SearchResultsPageLocators(object):
    LINK_LOCATOR = (By.CLASS_NAME, 'iUh30 qLRx3b tjvcx')